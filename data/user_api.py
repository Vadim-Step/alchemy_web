import flask
from flask import jsonify, make_response, request
from . import db_session
from .job import Jobs
from .user import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user')
def get_users():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    if user:
        return jsonify(
            {
                'user':
                    [item.to_dict() for item in user]
            }
        )
    return jsonify({'error': 'Bad request'})


@blueprint.route('/api/user/<int:user_id>')
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if user:
        return jsonify(
            {
                'user':
                    [user.to_dict()]
            }
        )
    return jsonify({'error': 'Bad request'})


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'email', 'city']):
        return jsonify({'error': 'Bad request'})
    else:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(request.json['id'])
        if user:
            return jsonify({'error': 'Id already exists'})
    db_sess = db_session.create_session()
    user = User()
    print('gg')
    user.id = request.json['id']
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.email = request.json['email']
    user.city = request.json['city']
    db_sess.add(user)
    db_sess.commit()
    print('gggg')
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Jobs).filter(Jobs.id == user_id).first()
    if not all(key in request.json for key in
               ['id', 'surname', 'name', 'age', 'email']):
        return jsonify({'error': 'Bad request'})
    if user:
        user.id = request.json['id']
        user.surname = request.json['surname']
        user.name = request.json['name']
        user.age = request.json['age']
        user.email = request.json['email']
        db_sess.commit()
    else:
        return jsonify({'error': 'Not found'})
    return jsonify({'success': 'OK'})
