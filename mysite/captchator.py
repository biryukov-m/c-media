import requests
import urllib.parse

''' Begin reCAPTCHA validation '''
recaptcha_response = request.POST.get('g-recaptcha-response')
url = 'https://www.google.com/recaptcha/api/siteverify'
values = {
    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
    'response': recaptcha_response
}
req = requests.post(url, data=values)
res = req.json()
# print(type(res))
# print(res)
print(res['success'])
''' End reCAPTCHA validation '''