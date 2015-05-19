# -*- coding: utf-8 -*-

import time
import logging

from flask import g
from flask import Flask
from flask import request
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Api
from flask_restful import Resource

import gl
from iniconf import MyIni
from imgdownload import Download
from clean_worker import CleanWorker
from models import User,Package

logger = logging.getLogger('root')


def version():
    """版本号"""
    return 'SX-UrlImgPackage V3.6.0'

# create a flask application - this ``app`` object will be used to handle
app = Flask(__name__)
api = Api(app)

# simple utility function to create tables
def create_tables():
    gl.DB.connect()
    try:
        gl.DB.create_tables([User,Package])
    except:
        pass


# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@app.before_request
def before_request():
    g.db = gl.DB
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response


class Index(Resource):

    def get(self):
        return {'message': "Welcome to use %s" % version()}


class TodoList(Resource):

    def post(self):
        if not request.json:
            return {'package': None, 'msg': 'Bad Request', 'code': 400}, 400
        if User.get_one(User.username == username) is None:
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

        if User.get_one(User.username == request.json['key']) is None:
            return {'status':401, 'message': 'Unauthorized access'}, 401

        gl.COUNT += 1
        timestamp = int(time.time())
        folder = str(timestamp) + '_' + str(gl.COUNT)
        filepath = os.path.join(gl.BASEPATH, folder + '.zip')

        p = Package.insert(timeflag=timestamp, ip=request.remote_addr,
                           path=filepath)
        p.execute()

        imgd = Download(folder)
        zipfile = imgd.main(request.json.get('urls', []))
        del imgd

        return {'status':201, 'message':'Created', 'package': zipfile}, 201

api.add_resource(Index, '/')
api.add_resource(TodoList, '/package')
api.add_resource(PackageListAPIV1, '/v1/package')


if __name__ == '__main__':  # pragma nocover
    init_logging(r'log\package.log')
    logger = logging.getLogger('root')

    logger.warn('System start')
    ini = MyIni()
    sysini = ini.get_sys_conf()
    gl.BASEPATH = sysini['path'].replace("/", "\\")
    
    ps = CleanWorker()
    ps.main()
    app.run(host="0.0.0.0", port=sysini.get('port', 8017), threaded=True)
    gl.IS_SYS_QUIT = True

    logger.warn('System end')
    
    del ini
    del ps


