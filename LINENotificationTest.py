import requests

token = 'rcfbWycKZu71qZKynhsoR86mCjNEbog425U9uIbZPhY'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + token
}

message = 'วันเริ่มต้น : 2 มิ.ย. 2565\nวันสิ้นสุด : 3 มิ.ย. 2565 '
requests.post(url = 'https://notify-api.line.me/api/notify', data={'message':message}, headers=headers)