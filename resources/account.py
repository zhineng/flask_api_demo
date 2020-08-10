from flask_restful import Resource, reqparse #處理使用者傳來參數
#讓class Accounts 知道它是flask_restful 的一種資源
import pymysql # 連接MySQL
from flask import jsonify #讓Python 資料結構(ex: Dictionary) 轉成JSON 格式
import traceback #吐出錯誤訊息


parser = reqparse.RequestParser() #設定白名單，使用者傳來那些欄位是API Server 可以被回應，不會全部資料都吐出來
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')


class Account(Resource): #針對單一account
    def db_init(self): #第一個參數一定是self
        db = pymysql.connect('localhost','root','$ssmi119$','api_2')
        #連接MySQL(hostname,db_account,db_password,db_name)
        cursor = db.cursor(pymysql.cursors.DictCursor) #取資料轉成Key:Value 形式，就是Dictionary
        return db,cursor
    def get(self,user_id,id): #當到'/accounts' ， 如果是使用Http method = get，執行get 程式 , id 使用者id  
        db,cursor = self.db_init()
        sql = """Select * from api_2.accounts Where id = '{}' and deleted is not True """.format(id)
        #deleted 備標註為1不撈出來
        #sql = """Select * from api_2.accounts Where id = '{}' """.format(id)
        cursor.execute(sql)
        db.commit()
        account = cursor.fetchone()#取得cursor 所有資料，只取一筆
        db.close()

        return jsonify({'data':account}) #將Python Dictionary 轉成JSON 呈現於網頁
    
    def patch(self,user_id,id):#只更新指定欄位
        db,cursor = self.db_init()
        arg = parser.parse_args() #將使用者傳給我的參數存到arg這個變數，這是Dictionary,Key:Value格式
        #Key:使用者傳來欄位名稱，Value: 使用者傳來該欄位的值
        account = {
            'balance':arg['balance'],
            'account_number':arg['account_number'],  
            'user_id':arg['user_id']
        }
        query = []
        for key,value in account.items():
            if value != None:
                query.append(key + " = " + "'{}'".format(value))
        query = "," .join(query)
        sql = """
            UPDATE `api_2`.`accounts` SET {} WHERE (`id` = '{}');
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
    #         DELETE FROM `api_2`.`accounts` WHERE (`id` = '{}');
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
    def delete(self,user_id,id):#刪除某筆資料，這是軟刪除，db 該筆資料欄位會被標示deleted
        db,cursor = self.db_init()
        sql = """
            UPDATE `api_2`.`accounts` SET deleted = True WHERE (`id` = '{}');
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

class Accounts(Resource):#針對多筆Accounts
    def db_init(self): #第一個參數一定是self
        db = pymysql.connect('localhost','root','$ssmi119$','api_2')
        #連接MySQL(hostname,db_account,db_password,db_name)
        cursor = db.cursor(pymysql.cursors.DictCursor) #取資料轉成Key:Value 形式，就是Dictionary
        return db,cursor
    def get(self,user_id): #當到'/accounts' ， 如果是使用Http method = get，執行get 程式   
        db,cursor = self.db_init()
        #sql = 'Select * from api_2.accounts'
        sql = 'Select * from api_2.accounts where user_id = "{}" and  deleted is not True'.format(user_id) #deleted 欄位杯標示為1不撈出
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()#取得cursor 所有資料
        db.close()

        return jsonify({'data':accounts}) #將Python Dictionary 轉成JSON 呈現於網頁

    def post(self,user_id):
        db,cursor = self.db_init()
        arg = parser.parse_args() #將使用者傳給我的參數存到arg這個變數，這是Dictionary,Key:Value格式
        #Key:使用者傳來欄位名稱，Value: 使用者傳來該欄位的值
        account = {
            'balance':arg['balance'],
            'account_number':arg['account_number'],  
            'user_id':arg['user_id']
        }

        sql = """
        INSERT INTO `api_2`.`accounts` (`balance`, `account_number`, `user_id`) VALUES ('{}', '{}', '{}');
        """.format(account['balance'],account['account_number'],account['user_id']) #將使用者傳來這些欄位值分別寫入DB對應欄位
        
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


