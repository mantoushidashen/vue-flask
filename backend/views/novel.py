from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
import requests
from bs4 import BeautifulSoup

blueprint = Blueprint('novel', __name__)
api = Api(blueprint)

base_url = "https://www.20xs.org"
url = "https://www.20xs.org/55983/"
class NovelChapters(Resource):
    def get(self):
        response = requests.get(url)
        response.encoding = 'utf-8'
        chapters_info = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            list_element = soup.find(id='list')
            if list_element:
                chapters = list_element.find_all('a')
                for chapter in chapters:
                    chapter_title = chapter.text
                    chapter_url = chapter.get('href')
                    if "章" in chapter_title:
                        chapters_info.append({
                            'title': chapter_title,
                            'url': base_url + chapter_url
                        })
            return {"code": 20000, "data": chapters_info}
        else:
            return {'message': 'Failed to fetch chapters'}, 500

class NovelContent(Resource):
    def get(self, chapter_url):
        response = requests.get(chapter_url)
        response.encoding = 'utf-8'
        chapter_data = {
            'content': '',
            'next_page': None,
            'url': chapter_url
        }

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.find(id='content')
            next_page_element = soup.find(id='A3')

            if text_content:
                contents = text_content.find_all('p')
                chapter_text = "\n".join(content.text for content in contents[:-1])
                chapter_data['content'] = chapter_text

            if next_page_element and next_page_element.text == '下一页':
                next_page_url = next_page_element.get('href')
                chapter_data['next_page'] = base_url + next_page_url
            
        else:
            return {'message': 'Failed to fetch chapter content'}, 500
        return {"code": 20000, "data": chapter_data}

api.add_resource(NovelChapters, '/api/novel/chapters')
api.add_resource(NovelContent, '/api/novel/content/<path:chapter_url>')