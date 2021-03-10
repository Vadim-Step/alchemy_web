import flask
from flask import jsonify, make_response, request
from . import db_session
from .job import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/<int:job_id>')
def get_jobs(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    return jsonify(
        {
            'job':
                [jobs.to_dict()]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'title', 'tl_id', 'work_size', 'collaborators', 'finished']):
        return jsonify({'error': 'Bad request'})
    else:
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(request.json['id'])
        if job:
            return jsonify({'error': 'Id already exists'})
    db_sess = db_session.create_session()
    jobs = Jobs()
    jobs.id = request.json['id']
    jobs.job = request.json['title']
    jobs.team_leader = request.json['tl_id']
    jobs.work_size = request.json['work_size']
    jobs.collaborators = request.json['collaborators']
    jobs.is_finished = request.json['finished']
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_news(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not all(key in request.json for key in
                 ['id', 'title', 'tl_id', 'work_size', 'collaborators', 'finished']):
        return jsonify({'error': 'Bad request'})
    if jobs:
        jobs.id = request.json['id']
        jobs.job = request.json['title']
        jobs.team_leader = request.json['tl_id']
        jobs.work_size = request.json['work_size']
        jobs.collaborators = request.json['collaborators']
        jobs.is_finished = request.json['finished']
        db_sess.commit()
    else:
        return jsonify({'error': 'Not found'})
    return jsonify({'success': 'OK'})
