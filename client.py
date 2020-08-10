import requests,json,jwt,time

url = "http://127.0.0.1:5000/users"

payload = "{\"user_id\":\"888\"}"
valid_token = jwt.encode({'user_id':"888",'timestamp':int(time.time())},'password',algorithm='HS256').decode('utf-8')
headers = {
    'Content-Type': 'application/json',
    'auth': valid_token
}
#測試帳號隨便，時間/密碼/演算法/加解密 須和server 相同
response = requests.request("GET", url, headers=headers, data = payload)

print(response.text)