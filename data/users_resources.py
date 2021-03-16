from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.user import User


def abort_if_user_not_found(news_id):
    session = db_session.create_session()
    news = session.query(User).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


class UserResource(Resource):
    def get(self, news_id):
        abort_if_user_not_found(news_id)
        session = db_session.create_session()
        news = session.query(User).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('id', 'surname', 'name', 'age'))})

    def delete(self, news_id):
        abort_if_user_not_found(news_id)
        session = db_session.create_session()
        news = session.query(User).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'news': [item.to_dict(
            only=('id', 'surname', 'name', 'age')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User()
        User.id = args['id'],
        User.surname = args['surname'],
        User.name = args['name'],
        User.age = args['age'],
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True)
