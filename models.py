from server import db
class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(45))
    gender = db.Column(db.Integer)
    birth = db.Column(db.DateTime)
    note = db.Column(db.Text)
    deleted = db.Column(db.Boolean)

    def __init__(self,name,gender,birth,note,deleted = None): #使用者傳來資料填入
        self.name = name
        self.gender = gender
        self.birth = birth
        self.note = note
        self.deleted = deleted

    def serialize(self):
        return {
            "name":self.name,
            "gender":self.gender,
            "birth":self.birth,
            "note":self.note,
            "deleted":self.deleted
        }