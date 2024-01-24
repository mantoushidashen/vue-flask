import os
from flask import Blueprint, request, Response
from flask_restful import reqparse, Resource, Api
from werkzeug.datastructures import FileStorage
from utils.custom_excel import MyExcel

blueprint = Blueprint('upload',__name__)
api = Api(blueprint)

# 设置请求参数
# parser = reqparse.RequestParser()
# parser.add_argument('username',type=str)
# parser.add_argument('password',type=str)

class Upload(Resource):
  def post(self):
    # 获取分析之后需要返回的文件名称
    analysis_file_name =  request.form.get('date')
    sysrs_file_name , crs_file_name = '', ''
    sysrs_file_path , crs_file_path = '', ''
    filedata = request.files
    # 设置保存文件的地址
    file_dir = os.path.join(os.getcwd(), 'static')


    for file in filedata.getlist('file'):
      if 'SysRS' in file.filename:
        # 保存文件
        sysrs_file_name = file.filename
        sysrs_file_path = os.path.join(file_dir, sysrs_file_name)
        file.save(sysrs_file_path)
      elif 'CRS' in file.filename:
        crs_file_name = file.filename
        crs_file_path = os.path.join(file_dir, crs_file_name)
        file.save(crs_file_path)
      else:
        return {"code": 405, "message": "请确认文件名中是否带有SysRS和CRS"}

    # 判断文件名称前半段是否相同
    if sysrs_file_name.split('_')[1] == crs_file_name.split('_')[1]:
      pass
    else:
      os.remove(sysrs_file_path)
      os.remove(crs_file_path)
      return {"code": 405, "message": "请确认是否为相同项目的文件"}

    excel = MyExcel(analysis_file_name, sysrs_file_path, crs_file_path)
    data = excel.merge_crs_sysrs()
    return {"code": 20000, "msg": "xxxxxxxxxxxxxx", "data": data}


api.add_resource(Upload,'/api/upload')