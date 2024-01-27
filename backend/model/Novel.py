from common.db_config import db  # 导入db

class NovelChapter(db.Model):
    __tablename__ = 'novel_chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), unique=True, nullable=False)
    # content = db.relationship('NovelChapterContent', backref='novel_chapter', lazy='dynamic')

    def __repr__(self):
        return f'<NovelChapter {self.title}>'

class NovelChapterContent(db.Model):
    __tablename__ = 'novel_chapter_contents'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    next_page = db.Column(db.String(255), nullable=True)  # 添加了next_page字段，允许为NULL

    def __repr__(self):
        return f'<NovelChapterContent {self.url}>'