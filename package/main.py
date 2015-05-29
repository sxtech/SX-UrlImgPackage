# main.py
from app import app
from models import User
import views

if __name__ == '__main__':
    User.create_table(True)
    app.run(host='0.0.0.0', port=8017, threaded=True)
