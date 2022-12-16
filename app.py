from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_security import Security, hash_password, auth_required
from datetime import datetime
import redis
import ast

from models import db, user_datastore, KanbanList, KanbanCard
from util import export_to_csv
import workers

app = Flask(__name__, static_url_path='', static_folder='static/dist')
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
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'


db.init_app(app)

# Token based authentication
security = Security(app, user_datastore)

rc = redis.Redis(host="localhost", port=6379, db=0)

celery = workers.celery
celery.conf.broker_url = 'redis://localhost:6379/1'
celery.conf.result_backend = 'redis://localhost:6379/2'
celery.Task = workers.ContextTask

app.app_context().push()

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
    user = get_user_from_token(request.headers.get('AUTHENTICATION-TOKEN'))
    return jsonify({'status': 'success', 'user': user.email})


# Return user from token
@app.route('/user', methods=['GET'])
@auth_required('token', 'basic')
def get_user():
    current_user = get_user_from_request(request)

    if current_user is None:
        return jsonify({'status': 'failed'})
    return jsonify({'user': current_user.id})


@app.route('/create/list', methods=['POST'])
@auth_required('token', 'basic')
def create_list():
    data = request.get_json()
    user = get_user_from_request(request)

    #Check if list already exists
    if KanbanList.query.filter_by(title=data['title'], user_id=user.id).first() is not None:
        return jsonify({'status': 'failed', 'error': 'List already exists'}), 400
    
    list = KanbanList(title=data['title'], user_id=user.id)
    db.session.add(list)
    db.session.commit()
    return jsonify({'status': 'success', 'id': list.id})

@app.route('/create/card', methods=['POST'])
@auth_required('token', 'basic')
def create_card():
    data = request.get_json()
    user = get_user_from_request(request)

    #Get list_id from list title
    list_id = KanbanList.query.filter_by(title=data['list'], user_id=user.id).first().id

    date = datetime.strptime(data['deadline'], '%Y-%m-%d')
    
    # Check if card already exists
    if KanbanCard.query.filter_by(title=data['title'], list_id=list_id).first() is not None:
        return jsonify({'status': 'failed', 'error': 'Card already exists'}), 400
    
    card = KanbanCard(title=data['title'], content= data['content'], deadline= date, list_id=list_id)
    db.session.add(card)
    
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'id': card.id})
    except:
        return jsonify({'status': 'failed', 'error': 'Card could not be created'}), 400

@app.route('/edit/list', methods=['POST'])
@auth_required('token', 'basic')
def edit_list():
    data = request.get_json()
    user = get_user_from_request(request)

    #Check if list already exists
    if KanbanList.query.filter_by(title=data['title'], user_id=user.id).first() is not None:
        return jsonify({'status': 'failed', 'error': 'List already exists'}), 400

    #Get list_id from list title
    list_id = KanbanList.query.filter_by(title=data['list'], user_id=user.id).first().id

    #Get list from list_id
    list = KanbanList.query.filter_by(id=list_id).first()
    list.title = data['title']
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/edit/card', methods=['POST'])
@auth_required('token', 'basic')
def edit_card():
    data = request.get_json()
    user = get_user_from_request(request)

    print(data['completed'])

    card_id = data['id']
    card: KanbanCard = KanbanCard.query.filter_by(id=card_id).first()

    # Check if card doesn't exists
    if card is None:
        return jsonify({'status': 'failed', 'error': "Card does not exists"}), 400
    
    og_list = KanbanList.query.filter_by(id=card.list_id).first()
    if og_list.user_id != user.id:
        return jsonify({'status': 'failed', 'error': "You do not have permission to edit this card"}), 401 

    list_id = KanbanList.query.filter_by(title=data['list'], user_id=user.id).first().id
    if list_id is None:
        return jsonify({'status': 'failed', 'error': "List does not exists"}), 400

    
    card.title = data['title']
    card.content = data['content']
    card.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d')
    card.list_id = list_id
    card.completed = data['completed']
    
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/delete/list', methods=['POST'])
@auth_required('token', 'basic')
def delete_list():
    data = request.get_json()
    user = get_user_from_request(request)

    #Check if list exists
    if KanbanList.query.filter_by(title=data['title'], user_id=user.id).first() is None:
        return jsonify({'status': 'failed', 'error': 'List does not exist'}), 400
    
    list = KanbanList.query.filter_by(title=data['title'], user_id=user.id).first()
    cards = KanbanCard.query.filter_by(list_id=list.id).all()
    db.session.delete(list)
    for card in cards:
        db.session.delete(card)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/delete/card', methods=['POST'])
@auth_required('token', 'basic')
def delete_card():
    data = request.get_json()
    user = get_user_from_request(request)

    #Get list_id from list title
    list_id = KanbanList.query.filter_by(title=data['list'], user_id=user.id).first().id
    
    # Check if card exists
    if KanbanCard.query.filter_by(title=data['title'], list_id=list_id).first() is None:
        return jsonify({'status': 'failed', 'error': 'Card does not exist'}), 400
    
    card = KanbanCard.query.filter_by(title=data['title'], list_id=list_id).first()
    db.session.delete(card)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/get/lists', methods=['GET'])
@auth_required('token', 'basic')
def get_lists():
    user = get_user_from_request(request)

    lists = rc.get(f'lists{user.id}')

    if lists is None:
        lists = []
        data = KanbanList.query.filter_by(user_id=user.id).all()
        for l in data:
            lists.append(str(l))
        
        rc.set(f'lists{user.id}', str(lists), ex=600)
    else:
        lists = ast.literal_eval(lists.decode())
    
    return jsonify({'lists': lists})

@app.route('/get/cards', methods=['GET'])
@auth_required('token', 'basic')
def get_cards():
    user = get_user_from_request(request)
    list_name = request.args.get('list')
    list_id = KanbanList.query.filter_by(title=list_name, user_id=user.id).first().id
    data: list[KanbanCard] = KanbanCard.query.filter_by(list_id=list_id).all()
    cards = []
    for c in data:
        cards.append(c.toJson())
    return jsonify({'cards': cards})

@app.route('/export', methods=['GET'])
@auth_required('token', 'basic')
def export():
    user = get_user_from_request(request)
    list_name = request.args.get('list')
    list_id = KanbanList.query.filter_by(title=list_name, user_id=user.id).first().id

    if list_id is None:
        return jsonify({'status': 'failed', 'error': "List does not exists"}), 400
    
    data: list[KanbanCard] = KanbanCard.query.filter_by(list_id=list_id).all()

    for i in range(len(data)):
        data[i] = data[i].toJson()

    file_name=export_to_csv(data, list_name)

    return send_file(file_name, as_attachment=True)


def get_user_from_token(token):
    data = security.remember_token_serializer.loads(token)
    return user_datastore.find_user(fs_uniquifier=data[0])

def get_user_from_request(request):
    return security.login_manager._load_user_from_request(request)

if __name__ == '__main__':
    app.run()