from flask import Flask
from flask_mail import Mail

mail = Mail() 
def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'C00kie'
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Flask-Mail settings
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = "luckyfoot028@gmail.com"
    app.config['MAIL_PASSWORD'] = "exrr zunn jaxl kwja"

    # Initialize Flask-Mail
    mail = Mail(app)
    return app
