from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup
from common.response_code import ResponseCode
from model.Novel import NovelChapter, NovelChapterContent
from common.db_config import db

blueprint = Blueprint('novel', __name__)
api = Api(blueprint)

base_url = "https://www.20xs.org"
novel_url = "https://www.20xs.org/55983/"
class NovelChapters(Resource):
    def get(self):
        try:
            chapters_info = NovelChapter.query.order_by(NovelChapter.id).all()
            if len(chapters_info) == 0:  # 如果数据库中没有章节，从网站抓取
                response = requests.get(novel_url)
                response.encoding = 'utf-8'
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    list_element = soup.find(id='list')
                    if list_element:
                        chapters = list_element.find_all('a')
                        for chapter in chapters:
                            chapter_title = chapter.text.strip()
                            chapter_url = base_url + chapter.get('href')
                            if "章" in chapter_title:  # 过滤有效章节
                                new_chapter = NovelChapter(title=chapter_title, url=chapter_url)
                                db.session.add(new_chapter)
                        db.session.commit()
                        chapters_info = NovelChapter.query.order_by(NovelChapter.id).all()
                else:
                    return ResponseCode.response(
                        False, ResponseCode.SERVER_ERROR, message="Failed to fetch chapters from remote site"
                    )
            chapters_data = [{'title': chapter.title, 'url': chapter.url} for chapter in chapters_info]
            return ResponseCode.response(True, ResponseCode.SUCCESS, chapters_data)
        except Exception as e:
            return ResponseCode.response(False, ResponseCode.SERVER_ERROR, message=str(e))

# NovelContent 资源类
class NovelContent(Resource):
    def get(self, chapter_url):
        try:
            chapter = NovelChapterContent.query.filter_by(url=chapter_url).first()
            if not chapter:  # 如果数据库中没有该章节内容
                response = requests.get(chapter_url)
                response.encoding = 'utf-8'
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text_content = soup.find(id='content')
                    next_page_element = soup.find(id='A3')
                    if text_content:
                        contents = text_content.find_all('p')
                        chapter_text = "\n".join(content.text for content in contents[:-1])
                        # 判断并获取下一页
                        next_page_url = None
                        if next_page_element and next_page_element.text == '下一页':
                            next_page_href = next_page_element.get('href')
                            next_page_url = base_url + next_page_href if next_page_href else None
                        
                        # 存储章节内容和下一页URL至数据库
                        new_chapter = NovelChapterContent(url=chapter_url, content=chapter_text, next_page=next_page_url)
                        db.session.add(new_chapter)
                        db.session.commit()
                        chapter = new_chapter  # 使用新创建的章节对象
                    else:
                        return ResponseCode.response(False, ResponseCode.SERVER_ERROR, message="Chapter content not found")
                else:
                    return ResponseCode.response(False, ResponseCode.SERVER_ERROR, message="Failed to fetch chapter content")
            
            chapter_data = {
                'content': chapter.content,
                'next_page': chapter.next_page,  # 使用数据库中的next_page字段
                'url': chapter_url
            }
            return ResponseCode.response(True, ResponseCode.SUCCESS, chapter_data)
        except Exception as e:
            return ResponseCode.response(False, ResponseCode.SERVER_ERROR, message=str(e))

api.add_resource(NovelChapters, '/api/novel/chapters')
api.add_resource(NovelContent, '/api/novel/content/<path:chapter_url>')