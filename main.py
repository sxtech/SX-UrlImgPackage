from package import app, User, views

if __name__ == '__main__':
    #User.create_table(True)
    #app.run()
    u = User.get_one(User.username == '123')
    print u
