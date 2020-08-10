
from flask import Flask,request,jsonify
from flask_restful import Api
from resources.user import Users,User
from resources.account import Accounts,Account
import pymysql
import traceback
import jwt #JSON Web Token，透過user 傳來資料加上時間產出一個Token
import time
#from server import app

app = Flask(__name__) #網站初始化，把網站放在app 這個變數
api = Api(app) #轉換成這是一個API Server

api.add_resource(Users,'/users') #進了網址"/users"，執行程式Users
api.add_resource(User,'/user/<id>') #<id> 動態，看塞哪個userid
api.add_resource(Accounts,'/user/<user_id>/accounts') #netsted one user have more accounts
api.add_resource(Account,'/user/<user_id>/account/<id>')
# api.add_resource(Accounts,'/accounts')
# api.add_resource(Account,'/account/<id>')

# @app.errorhandler(Exception)
# def handle_error(error):
#     status_code = 500
#     if type(error).__name__ == 'NotFound':
#         status_code = 404
#     elif type(error).__name__ == "TypeError":
#         status_code = 500

#     return jsonify({'msg':type(error).__name__}),status_code

# @app.before_request #讀所有API前先經過任證
# def auth():
#     token = request.headers.get('auth')
#     user_id = request.get_json()['user_id'] #time是以秒為單位，使用者送出和server 接收應該是同一秒，毫秒就有落差
#     #password 模擬user secret key,user 算出和server 取user secret key 算出應該要一樣
#     valid_token = jwt.encode({'user_id':user_id,'timestamp':int(time.time())},'password',algorithm='HS256').decode('utf-8')
#     print(valid_token)
#     if token == valid_token:
#         pass
#     else:
#         return{'msg':'invalid token'}
        
@app.route('/') #裝飾子,首頁
def index():
    return 'Bello World'

@app.route('/user/<user_id>/account/<id>/deposit',methods=['POST']) #存錢
def deposit(user_id,id):
    db,cursor,account = get_account(id)
    money = request.get_json()['money'] #使用者要存入金額，型別為純字串
    balance = account['balance'] + int(money) #money 轉換型別為int
    sql = 'Update api_2.accounts Set balance = {} Where id = {} and deleted is not True'.format(balance,id)
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] = 'failed'

    db.commit()
    db.close()
    return jsonify(response)

@app.route('/user/<user_id>/account/<id>/withdraw',methods=['POST']) #領錢
def withdraw(user_id,id):
    db,cursor,account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    response = {} #response 拉到前面做防呆機制，如果領錢金額超過銀行存款，通知失敗
    if balance < 0:
        response['msg'] = "money not enough"
        return jsonify(response)
    else:
        sql = 'Update api_2.accounts Set balance = {} Where id = {} and deleted is not True'.format(balance,id)
        
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)


def get_account(id): #讀取account 物件，由account id 帶出
    db = pymysql.connect('localhost','root','$ssmi119$','api_2')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'Select * From api_2.accounts where id = "{}" and  deleted is not True'.format(id)
    cursor.execute(sql)
    return db,cursor,cursor.fetchone()

if __name__ == '__main__': #確認是不是主程式執行
    app.debug = True
    app.run(host='127.0.0.1',port=5000)

