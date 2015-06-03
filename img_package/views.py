# -*- coding: utf-8 -*-

import os
import time
import logging

from flask import g, request
from flask_restful import reqparse, abort, Resource

from app import app, db, api
from models import User, Package
import gl
from imgdownload import Download
from models import User, Package


logger = logging.getLogger('root')


# Request handlers -- these two hooks are provided by flask and we will use
# them to create and tear down a database connection on each request.
@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


class Index(Resource):

    def get(self):
        return {'package_url': 'http://localhost/package',
                'package_url': 'http://localhost/v1/package'}


class TodoList(Resource):

    def post(self):
        if not request.json:
            return {'package': None, 'msg': 'Bad Request', 'code': 400}, 400
        if User.get_one(User.username == request.json.get('key', None)) is None:
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
        parser.add_argument('urls', type=list, required=True,
                            help='urls json array is require', location='json')
        args = parser.parse_args()

        if User.get_one(User.username == request.json['key']) is None:
            return {'status': 401, 'message': 'Unauthorized access'}, 401

        gl.COUNT += 1
        timestamp = int(time.time())
        folder = '%s_%s' % (str(timestamp), str(gl.COUNT))
        filepath = os.path.join(app.config['BASEPATH'], folder + '.zip')

        p = Package.insert(timeflag=timestamp, ip=request.remote_addr,
                           path=filepath)
        p.execute()

        imgd = Download(app.config['BASEPATH'], folder)
        zipfile = imgd.main(request.json.get('urls', []))
        del imgd

        return {'status': 201, 'message': 'Created', 'package': zipfile}, 201

api.add_resource(Index, '/')
api.add_resource(TodoList, '/package')
api.add_resource(PackageListAPIV1, '/v1/package')
