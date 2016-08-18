from img_package import app, User, Users, Package, views
from img_package import debug_logging, online_logging, CleanWorker, MyIni

if __name__ == '__main__':
    debug_logging('log\package.log')
    cw = CleanWorker()
    cw.main()
    ini = MyIni()
    sysini = ini.get_sys_conf()
    app.config['BASEPATH'] = sysini['path']
    app.run(port=sysini['port'], threaded=True)
    app.config['IS_QUIT'] = True
    del cw
