import time

from img_package import app
from img_package.clean_worker import CleanWorker

def test_clean_worker():
    cw = CleanWorker()
    cw.main()
    time.sleep(10)
    app.config['IS_QUIT']

if __name__ == "__main__":
    test_clean_worker()

    
