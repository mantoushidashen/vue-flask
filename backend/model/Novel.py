from common.db_config import db  # 导入db

class Novel(db.Model):
    __tablename__ = 'novel'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)