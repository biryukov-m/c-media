import requests
import urllib.parse

''' Begin reCAPTCHA validation '''
recaptcha_response = '1123412341234'
url = 'https://www.google.com/recaptcha/api/siteverify'
values = {
    'secret': '6LdjAlUUAAAAAF4h6YyWNIS0QN-2N2UCpi08gB-o',
    'response': recaptcha_response
}
params = urllib.parse.urlencode(values)
req = requests.get(url, params)
res = req.json()
# print(type(res))
# print(res)
print(res['success'])
''' End reCAPTCHA validation '''