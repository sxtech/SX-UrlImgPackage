##from url_img_package.models import User,Package
##from url_img_package import MyIni
##from peewee import *
##from url_img_package import gl
##from url_img_package import online_logging
##import logging
##import json
from requests_func import RequestsFunc
##from url_img_package import app
##from url_img_package import CleanWorker
##
def model_test():
    db = gl.DB
    db.connect()

    Package.create(timeflag=123, ip='127.0.0.1', path='my/path')
    db.close()

def conf_test():
    ini = MyIni()
    s = ini.get_sys_conf()
    print s

def log_test():
    online_logging(r'log\package.log')
    logger = logging.getLogger('root')

    logger.warn('log test')

def requests_test():
    import json
    rf = RequestsFunc()
    url = 'http://127.0.0.1:8017/v1/package'
    urls = ['http://localhost/imgareaselect/imgs/1.jpg','http://localhost/imgareaselect/imgs/2.jpg']
    data = {'key':'sx2767722','urls': urls}
    r = rf.send_post(url, json.dumps(data))
    print r.status_code
    print r.text

def flask_run_test():
    online_logging(r'log\package.log')
    #logger = logging.getLogger('root')

    #logger.warn('System start')
    ini = MyIni()
    sysini = ini.get_sys_conf()
    gl.BASEPATH = sysini['path'].replace("/", "\\")
    
    ps = CleanWorker()
    ps.main()
    app.run(host="0.0.0.0", port=sysini.get('port', 8017), threaded=True,debug=True)
    gl.IS_SYS_QUIT = True

    #logger.warn('System end')
    
    del ini
    del ps

if __name__ == '__main__':
    #model_test()
    #conf_test()
    #log_test()
    requests_test()
    #flask_run_test()
