from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.job import Jobs


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('id', 'team_leader', 'job', 'work_size'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id', 'team_leader', 'job', 'work_size')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = Jobs()
        Jobs.id = args['id'],
        Jobs.surname = args['team_leader'],
        Jobs.name = args['job'],
        Jobs.age = args['work_size'],
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('team_leader', required=True)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True)
