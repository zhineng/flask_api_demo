from flask_restful import Resource, reqparse #處理使用者傳來參數
#讓class Users 知道它是flask_restful 的一種資源
import pymysql # 連接MySQL
from flask import jsonify,make_response #讓Python 資料結構(ex: Dictionary) 轉成JSON 格式
import traceback #吐出錯誤訊息
#from server import db
#from models import UserModel
from dotenv import load_dotenv
import os
load_dotenv()


parser = reqparse.RequestParser() #設定白名單，使用者傳來那些欄位是API Server 可以被回應，不會全部資料都吐出來
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource): #針對單一user
    def db_init(self): #第一個參數一定是self
        db = pymysql.connect(os.getenv('DB_HOST'),os.getenv('DB_USER'),os.getenv('DB_PASSWORD'),os.getenv('DB_SCHEMA'))
        #db = pymysql.connect('localhost','root','$ssmi119$','api_2')
        #連接MySQL(hostname,db_account,db_password,db_name)
        cursor = db.cursor(pymysql.cursors.DictCursor) #取資料轉成Key:Value 形式，就是Dictionary
        return db,cursor
    def get(self,id): #當到'/users' ， 如果是使用Http method = get，執行get 程式 , id 使用者id  
        db,cursor = self.db_init()
        sql = """Select * from api_2.users Where id = '{}' and deleted is not True """.format(id)
        #deleted 備標註為1不撈出來
        #sql = """Select * from api_2.users Where id = '{}' """.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()#取得cursor 所有資料，只取一筆
        db.close()

        return jsonify({'data':user}) #將Python Dictionary 轉成JSON 呈現於網頁
    
    def patch(self,id):#只更新指定欄位
        db,cursor = self.db_init()
        arg = parser.parse_args() #將使用者傳給我的參數存到arg這個變數，這是Dictionary,Key:Value格式
        #Key:使用者傳來欄位名稱，Value: 使用者傳來該欄位的值
        user = {
            'name':arg['name'],
            'gender':arg['gender'],  
            'birth':arg['birth'] , 
            'note':arg['note']
        }
        query = []
        for key,value in user.items():
            if value != None:
                query.append(key + " = " + "'{}'".format(value))
        query = "," .join(query)
        sql = """
            UPDATE `api_2`.`users` SET {} WHERE (`id` = '{}');
        """.format(query,id)

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except :
            traceback.print_exc() #印出錯誤訊息
            response['msg'] = 'failed'
        
        db.commit()
        db.close()
        return jsonify(response)#將Python Dictionary 轉成JSON 呈現於網頁

    # def delete(self,id):#刪除某筆資料 ,這是硬刪除，直接刪除
    #     db,cursor = self.db_init()
    #     sql = """
    #         DELETE FROM `api_2`.`users` WHERE (`id` = '{}');
    #     """.format(id)

    #     response = {}
    #     try:
    #         cursor.execute(sql)
    #         response['msg'] = 'success'
    #     except :
    #         traceback.print_exc() #印出錯誤訊息
    #         response['msg'] = 'failed'
        
    #     db.commit()
    #     db.close()
    #     return jsonify(response)#將Python Dictionary 轉成JSON 呈現於網頁
    def delete(self,id):#刪除某筆資料，這是軟刪除，db 該筆資料欄位會被標示deleted
        db,cursor = self.db_init()
        sql = """
            UPDATE `api_2`.`users` SET deleted = True WHERE (`id` = '{}');
        """.format(id)
        

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except :
            traceback.print_exc() #印出錯誤訊息
            response['msg'] = 'failed'
        
        db.commit()
        db.close()
        return jsonify(response)#將Python Dictionary 轉成JSON 呈現於網頁

class Users(Resource):#針對多筆Users
    def db_init(self): #第一個參數一定是self
        db = pymysql.connect('localhost','root','$ssmi119$','api_2')
        #連接MySQL(hostname,db_account,db_password,db_name)
        cursor = db.cursor(pymysql.cursors.DictCursor) #取資料轉成Key:Value 形式，就是Dictionary
        return db,cursor
    def get(self): #當到'/users' ， 如果是使用Http method = get，執行get 程式   
        db,cursor = self.db_init()
        arg = parser.parse_args() #做篩選欄位用
        #sql = 'Select * from api_2.users'
        sql = 'Select * from api_2.users where deleted is not True' #deleted 欄位杯標示為1不撈出
        if arg['gender'] != None:
            sql += ' and gender = "{}"'.format(arg['gender'])
        
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()#取得cursor 所有資料
        db.close()
        return make_response(jsonify({'data':users}),888)#自定義Response Code
        #users  = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        #return jsonify({'data':list(map(lambda user:user.serialize(),users))})
        return jsonify({'data':users}) #將Python Dictionary 轉成JSON 呈現於網頁

    def post(self):
        db,cursor = self.db_init()
        arg = parser.parse_args() #將使用者傳給我的參數存到arg這個變數，這是Dictionary,Key:Value格式
        #Key:使用者傳來欄位名稱，Value: 使用者傳來該欄位的值
        user = {
            'name':arg['name'],
            'gender':arg['gender'] or 0, #db欄位為數字格式需有值不接Null，如果前端沒給值，給預設值0
            'birth':arg['birth'] or '1900-01-01', #db欄位為日期格式需有值不接Null，如果前端沒給值，給預設日期
            'note':arg['note']
        }

        sql = """
        INSERT INTO `api_2`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        """.format(user['name'],user['gender'],user['birth'],user['note']) #將使用者傳來這些欄位值分別寫入DB對應欄位
        
        response = {}
        status_code = 200
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except :
            status_code = 400
            traceback.print_exc() #印出錯誤訊息
            response['msg'] = 'failed'
        
        db.commit()
        db.close()
        #return jsonify(response)#將Python Dictionary 轉成JSON 呈現於網頁
        return make_response(jsonify(response),status_code)

