from flask import Flask, render_template
import requests

app = Flask(__name__)

API_KEY = '719bb81181c5781c882d70f3d5372f6a'
IPINFO_API_KEY = '8f6b6f69dc726d' 

def get_ip_info():
    ipstack_url = f"http://api.ipstack.com/check?access_key={API_KEY}"

    try:
        response_ipstack = requests.get(ipstack_url)
        response_ipstack.raise_for_status() 
        data_ipstack = response_ipstack.json()

        ipv4 = data_ipstack.get('ip')
        ipv6 = data_ipstack.get('ipv6')
        location = f"{data_ipstack.get('city')}, {data_ipstack.get('region_name')}, {data_ipstack.get('country_name')}"
        isp = data_ipstack.get('isp')
        country_code = data_ipstack.get('country_code')

        proxy_type = None
        if ipv4:
            ipinfo_url = f"https://ipinfo.io/{ipv4}/json?token={IPINFO_API_KEY}"
            response_ipinfo = requests.get(ipinfo_url)
            response_ipinfo.raise_for_status() 
            data_ipinfo = response_ipinfo.json()

            if 'proxy' in data_ipinfo:
                proxy_type = data_ipinfo['proxy'].get('proxy_type')

        return {
            'ipv4': ipv4,
            'ipv6': ipv6,
            'location': location,
            'isp': isp,
            'country_code': country_code,
            'proxy_or_vpn': proxy_type
        }

    except requests.exceptions.RequestException as e:
        return None

@app.route('/')
def display_ip_info():
    result = get_ip_info()
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
