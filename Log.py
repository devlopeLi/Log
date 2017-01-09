# -*- coding: utf-8 -*-

from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request
import os



UPLOAD_FOLDER = '/Users/jyunhuali/PyCharm/Log'
#UPLOAD_FOLDER = '/opt/mobile-log'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

path = '/Users/jyunhuali/Desktop/'
#path = '/opt/mobile-log/'


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 用于测试上传，稍后用到
@app.route('/test/upload')
def upload_test():
    return render_template('upload.html')


# 上传文件
@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    print f
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        print f
        # 将文件名分割（用户id，server，time）
        list = fname.split('-', 2)
        print list
        server = list[1]
        serverPath = path + server
        if (list[1] == server):
            new_filename = list[2]
            if os.path.isdir(serverPath):
                os.chdir(serverPath)
                if os.path.isdir(serverPath + '/' + list[0]):
                    os.chdir(list[0])
                    f.save(os.path.join(os.path.abspath('.'), new_filename))  # 保存文件到upload目录
                else:
                    os.mkdir(list[0])
                    os.chdir(list[0])
                    f.save(os.path.join(os.path.abspath('.'), new_filename))  # 保存文件到upload目录
            else:
                os.chdir(path)
                os.mkdir(server)
                os.chdir(serverPath)
                if os.path.isdir(list[0]):
                    os.chdir(list[0])
                    f.save(os.path.join(os.path.abspath('.'), new_filename))  # 保存文件到upload目录
                else:
                    os.mkdir(list[0])
                    os.chdir(list[0])
                    f.save(os.path.join(os.path.abspath('.'), new_filename))  # 保存文件到upload目录

        return jsonify({"code": "0", "statu": "success"})
    else:
        return jsonify({"code": "50000", "statu": "fail"})


if __name__ == '__main__':
    app.run(port=8080)
