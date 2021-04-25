import sqlite3
from flask import jsonify, Blueprint, request
from sqlalchemy import exc
from data import db_session
from data.users import User
import datetime

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=(
                    'id', 'name', 'surname', 'age', 'email', 'hashed_password', 'created_date', 'favourite'))
                    for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=(
                'id', 'name', 'surname', 'age', 'email', 'hashed_password', 'created_date', 'favourite'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'age', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User()
    user.id = request.json["id"]
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.age = request.json['age']
    user.email = request.json['email']
    user.created_date = datetime.datetime.now()
    user.set_password(request.json["hashed_password"])
    try:
        db_sess.add(user)
        db_sess.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Id or email already exists'})
    except exc.IntegrityError:
        return jsonify({'error': 'Id or email already exists'})
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    s = request.json
    if s.get('id') is not None:
        users.id = s['id']
    if s.get('name') is not None:
        users.name = s['name']
    if s.get('surname') is not None:
        users.surname = s['surname']
    if s.get('age') is not None:
        users.age = s['age']
    if s.get('email') is not None:
        users.email = s['email']
    if s.get('created_date') is not None:
        users.created_date = s['created_date']
    if s.get('favourite') is not None:
        users.favourite = s['favourite']
    if s.get('hashed_password') is not None:
        users.set_password(s["hashed_password"])
    try:
        db_sess.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Id or email already exists'})
    except exc.IntegrityError:
        return jsonify({'error': 'Id or email already exists'})
    return jsonify({'success': 'OK'})
