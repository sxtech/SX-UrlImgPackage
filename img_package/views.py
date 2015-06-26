# -*- coding: utf-8 -*-

from flask import g, request
from flask_restful import reqparse, abort, Resource
from passlib.hash import sha256_crypt

from app import app, db, api, auth, logger
from models import User, Users
from imgdownload import Download


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@auth.verify_password
def verify_password(username, password):
    user = Users.get_one(Users.username == username,
                         Users.banned == False)
    if not user:
        return False
    return sha256_crypt.verify(password, user.password)


class Index(Resource):

    def get(self):
        return {'package_url': 'http://localhost/package',
                'package_v1_url': 'http://localhost/v1/package'}


class TodoList(Resource):

    def post(self):
        if not request.json:
            return {'package': None, 'msg': 'Bad Request', 'code': 400}, 400
        if User.get_one(User.username == request.json.get('key', None)) is None:
            return {'package': None, 'msg': 'Key Error', 'code': 105}, 401
        if 'urls' not in request.json:
            return {'package': None, 'msg': 'No "urls" key', 'code': 106}, 400

        imgd = Download(request.remote_addr)
        zipfile = imgd.main(request.json.get('urls', []))
        del imgd

        return {'package': zipfile, 'msg': 'Success', 'code': 100}, 201


class PackageListAPIV1(Resource):

    @auth.login_required
    def post(self):
        if not request.json:
            return {'message': 'Problems parsing JSON'}, 400
        if 'urls' not in request.json.keys():
            return {'message': 'Validation Failed',
                    'errors': [{'resource:': 'Package', 'field': 'urls',
                                'code': 'missing_field'}]}, 422
        if not isinstance(request.json['urls'], list):
            return {'message': 'Validation Failed',
                    'errors': [{'resource:': 'Package', 'field': 'urls',
                                'code': 'invalid'}]}, 422

        imgd = Download(request.remote_addr)
        zipfile = imgd.main(request.json['urls'])
        del imgd

        return {'package': zipfile}, 201

api.add_resource(Index, '/')
api.add_resource(TodoList, '/package')
api.add_resource(PackageListAPIV1, '/v1/package')
