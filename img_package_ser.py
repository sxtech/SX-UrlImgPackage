# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers

from flask import Flask
from flask import request
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Api
from flask_restful import Resource

import gl
from iniconf import MyIni
from imgdownload import Download
from package_work import PackageWorker


def init_logging(log_file_name):
    """Init for logging"""
    path = os.path.split(log_file_name)
    if os.path.isdir(path[0]):
        pass
    else:
        os.makedirs(path[0])
    logger = logging.getLogger('root')

    rthandler = logging.handlers.RotatingFileHandler(
        log_file_name, maxBytes=20 * 1024 * 1024, backupCount=5)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s[line:%(lineno)d] \
        [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    rthandler.setFormatter(formatter)
    logger.addHandler(rthandler)


def version():
    """版本号"""
    return 'SX-UrlImgPackage V3.5.0'


app = Flask(__name__)
api = Api(app)


class Index(Resource):

    def get(self):
        return {'message': "Welcome to use %s" % version()}


class TodoList(Resource):

    def post(self):
        if not request.json:
            return {'package': None, 'msg': 'Bad Request', 'code': 400}, 400
        if request.json.get('key', None) not in gl.KEYSDICT:
            return {'package': None, 'msg': 'Key Error', 'code': 105}, 401
        if 'urls' not in request.json:
            return {'package': None, 'msg': 'No "urls" key', 'code': 106}, 400

        gl.COUNT += 1
        imgd = Download(request.remote_addr)
        zipfile = imgd.main(request.json.get('urls', []))
        del imgd

        return {'package': zipfile, 'msg': 'Success', 'code': 100}, 201


class PackageListAPIV1(Resource):

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('key', type=unicode, required=True,
                            help='A key value is require', location='json')
        parser.add_argument('urls', type=list,required=True,
                            help='urls json array is require', location='json')
        args = parser.parse_args()

        if request.json.get('key', None) not in gl.KEYSDICT:
            return {'status':401, 'message': 'Unauthorized access'}, 401

        gl.COUNT += 1
        imgd = Download(request.remote_addr)
        zipfile = imgd.main(request.json.get('urls', []))
        del imgd

        return {'status':201, 'message':'Created', 'package': zipfile}, 201

api.add_resource(Index, '/')
api.add_resource(TodoList, '/package')
api.add_resource(PackageListAPIV1, '/v1/package')


if __name__ == '__main__':  # pragma nocover
    init_logging(r'log\package.log')
    logger = logging.getLogger('root')
    
    ini = MyIni()
    sysini = ini.get_sys_conf()
    ps = PackageWorker()
    ps.main()
    app.run(host="0.0.0.0", port=sysini.get('port', 8017), threaded=True)
    gl.IS_SYS_QUIT = True
    
    del ini
    del ps


