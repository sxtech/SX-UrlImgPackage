from img_package import app
from img_package import debug_logging, online_logging
from img_package.clean_worker import CleanWorker

if __name__ == '__main__':
    cw = CleanWorker()
    cw.main()
    app.run(port=5000, threaded=True)
    app.config['IS_QUIT'] = True
    del cw
