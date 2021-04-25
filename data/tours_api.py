import sqlite3
from flask import jsonify, Blueprint, request
from sqlalchemy import exc
from data import db_session
from data.tours import Tour
import datetime

blueprint = Blueprint(
    'tours_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/tours')
def get_tours():
    db_sess = db_session.create_session()
    tours = db_sess.query(Tour).all()
    return jsonify(
        {
            'tours':
                [item.to_dict(only=(
                    'id', 'name', 'about', 'places', 'cost', 'date', 'user'))
                    for item in tours]
        }
    )


@blueprint.route('/api/tours/<int:tour_id>')
def get_tour(tour_id):
    db_sess = db_session.create_session()
    tours = db_sess.query(Tour).get(tour_id)
    if not tours:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'tours': tours.to_dict(only=(
                'id', 'name', 'about', 'places', 'cost', 'date', 'user'))
        }
    )


@blueprint.route('/api/tours', methods=['POST'])
def create_tour():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'places', 'cost', 'date', 'user']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    tour = Tour()
    tour.id = request.json["id"]
    tour.name = request.json['name']
    if request.json.get("about"):
        tour.about = request.json['about']
    tour.places = request.json['places']
    tour.cost = request.json['cost']
    tour.date = datetime.datetime.strptime(request.json['date'], "%Y-%m-%d")
    tour.user = request.json['user']
    try:
        db_sess.add(tour)
        db_sess.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Id already exists'})
    except exc.IntegrityError:
        return jsonify({'error': 'Id already exists'})
    return jsonify({'success': 'OK'})


@blueprint.route('/api/tours/<int:tours_id>', methods=['DELETE'])
def delete_tours(tours_id):
    db_sess = db_session.create_session()
    tours = db_sess.query(Tour).get(tours_id)
    if not tours:
        return jsonify({'error': 'Not found'})
    db_sess.delete(tours)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/tours/<int:tour_id>', methods=['PUT'])
def put_tour(tour_id):
    db_sess = db_session.create_session()
    tours = db_sess.query(Tour).get(tour_id)
    if not tours:
        return jsonify({'error': 'Not found'})
    s = request.json
    if s.get('id') is not None:
        tours.id = s['id']
    if s.get('name') is not None:
        tours.name = s['name']
    if s.get('about') is not None:
        tours.about = s['about']
    if s.get('places') is not None:
        tours.places = s['places']
    if s.get('cost') is not None:
        tours.cost = s['cost']
    if s.get('date') is not None:
        tours.date = s['date']
    if s.get('user') is not None:
        tours.user = s['user']
    try:
        db_sess.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Id or email already exists'})
    except exc.IntegrityError:
        return jsonify({'error': 'Id or email already exists'})
    return jsonify({'success': 'OK'})
