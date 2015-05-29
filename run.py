from img_package import app, User, Package, views
from img_package import debug_logging, online_logging, CleanWorker, MyIni

if __name__ == '__main__':
    User.create_table(True)
    Package.create_table(True)
    debug_logging('log\package.log')
    cw = CleanWorker()
    cw.main()
    ini = MyIni()
    sysini = ini.get_sys_conf()
    app.config['BASEPATH'] = sysini['path']
    app.run(host='0.0.0.0', port=sysini['port'], threaded=True)
    cw.is_quit = True
    del cw
