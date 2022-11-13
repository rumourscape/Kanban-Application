from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_security import Security, hash_password, auth_required
from models import db, user_datastore

app = Flask(__name__, static_url_path='', static_folder='frontend/dist')
CORS(app)

app.config['DEBUG'] = True
app.config["WTF_CSRF_ENABLED"] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['SECURITY_TOKEN_AUTHENTICATION_AGE'] = 3600
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mad.db'
app.config['SECURITY_JOIN_USER_ROLES'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret'


db.init_app(app)

# Token based authentication
security = Security(app, user_datastore)

# Admin User
@app.before_first_request
def create_user():
    db.create_all()
    if user_datastore.find_user(email='advaitjoglekar@yahoo.in') is None:
        user_datastore.create_user(email='advaitjoglekar@yahoo.in', password= hash_password('password'))
    db.session.commit()


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/get_token', methods=['POST'])
def get_token():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = user_datastore.find_user(email=email)
    if user is not None and user.verify_and_update_password(password):
        return jsonify({'token': user.get_auth_token()})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/verify-token', methods=['GET'])
@auth_required('token', 'basic')
def verify_token():
    user = get_user_from_token(request.headers.get('Authentication-Token'))
    return jsonify({'status': 'success', 'user': user.email})


# Return user from token
@app.route('/user', methods=['GET'])
@auth_required('token', 'basic')
def get_user():
    current_user = get_user_from_request(request)

    if current_user is None:
        return jsonify({'status': 'failed'})
    return jsonify({'user': current_user.id})

def get_user_from_token(token):
    data = security.remember_token_serializer.loads(token)
    return user_datastore.find_user(fs_uniquifier=data[0])

def get_user_from_request(request):
    return security.login_manager._load_user_from_request(request)

if __name__ == '__main__':
    app.run()