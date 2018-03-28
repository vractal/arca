from arca import app, models
models.Database.initdb()
models.User.register("admin","admin","emailadmin")
if __name__ == "__main__":
    app.run()


