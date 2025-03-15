from flask import Flask
from flask_login import LoginManager

from routes import auth_bp, comment_bp, location_bp, user_bp
from db_queries import find_user_by_id
from model import create_db
create_db()

app = Flask(__name__)
app.secret_key = "ABCDE"
app.config['SESSION_PROTECTION'] = 'strong'
app.config['SECRET_KEY'] = 'ABCDE'
app.config['REMEMBER_COOKIE_DURATION'] = 3600
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True


login_manager = LoginManager()
login_manager.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(location_bp)
app.register_blueprint(user_bp)
create_db()

@login_manager.user_loader
def load_user(user_id):
    user = find_user_by_id(user_id)
    return user


@app.route('/')
def index():
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True)