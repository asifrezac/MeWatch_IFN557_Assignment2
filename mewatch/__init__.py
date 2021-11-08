# package constructor making the folder a package and it runs first.
#import necessary modules
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


#initiating the database with SQLAlchemy
db = SQLAlchemy()

#module calling this app
app= Flask(__name__)


#web application function
def create_app():
    app.debug=True
    app.secret_key = 'mewatch1234'

    #app config data
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mewatch.sqlite'

    #initializing db with flask
    db.init_app(app)

    bootstrap = Bootstrap(app)

    #adding blueprint
    from . import views
    app.register_blueprint(views.bp)
    # from . import admin
    # app.register_blueprint(admin.bp)

    return app

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

#for server issues
@app.errorhandler(505)
def internal_error(e):
    return render_template("505.html")
