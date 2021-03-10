import requests
from flask import Flask, render_template, request, make_response, jsonify, url_for
from flask_login import login_user, login_required
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from flask_login import LoginManager, current_user
from data.db_session import create_session
from data.dep_form import DepForm
from data.departments import Departments
from data.job import Jobs
from data.job_form import JobForm
from data.log_form import LoginForm
from data.reg_form import RegForm
from data.user import User
from data import db_session, user_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(user_api.blueprint)
    app.run()


@app.route('/tab1')
def table():
    db_session.global_init('db/blogs.db')
    db_sess = create_session()
    lst = []
    for job in db_sess.query(Jobs).all():
        row = [job.job]
        for i in db_sess.query(User).all():
            if i.id == job.team_leader:
                row.append(f'{i.name} {i.surname}')
        row.append(job.work_size)
        row.append(job.collaborators)
        if job.is_finished:
            row.append('Is finished')
        else:
            row.append('Is not finished')
        row.append(job.team_leader)
        row.append(job.id)
        lst.append(row)
    return render_template('index.html', lst=lst)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init('db/blogs.db')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/tab1")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_session.global_init('db/blogs.db')
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = int(form.tl_id.data)
        job.work_size = int(form.work_size.data)
        job.collaborators = form.collaborators.data
        job.is_finished = form.finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect("/tab1")
    return render_template('job.html', title='Add a job', form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        db_session.global_init('db/blogs.db')
        db_sess = db_session.create_session()
        user = User()
        user.id = int(form.id.data)
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = int(form.age.data)
        user.email = form.email.data
        user.hashed_password = form.password.data
        login_user(user)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/tab1")
    return render_template('reg.html', form=form)


@app.route('/tab1/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = JobForm()
    db_session.global_init('db/blogs.db')
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id, (Jobs.team_leader == current_user.id) | (
                current_user.id == 1)).first()
        if jobs:
            form.title.data = jobs.job
            form.tl_id.data = jobs.team_leader
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id
                                          ).first()
        if jobs:
            jobs.title = form.title.data
            jobs.team_leader = form.tl_id.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.finished.data
            db_sess.commit()
            return redirect('/tab1')
        else:
            abort(404)
    return render_template('job.html', title='Edit a job', form=form)


@app.route('/tab1_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    if current_user.id == 1:
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    else:
        job = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)

    return redirect('/tab1')


@app.route('/dep')
def departments():
    db_session.global_init('db/blogs.db')
    db_sess = create_session()
    lst = []
    for dep in db_sess.query(Departments).all():
        row = [dep.title]
        for i in db_sess.query(User).all():
            if i.id == dep.chief:
                row.append(f'{i.name} {i.surname}')
        row.append(dep.members)
        row.append(dep.email)
        row.append(dep.id)
        row.append(dep.chief)
        lst.append(row)
    return render_template('departments.html', lst=lst)


@app.route('/add_dep', methods=['GET', 'POST'])
def add_dep():
    form = DepForm()
    if form.validate_on_submit():
        db_session.global_init('db/blogs.db')
        db_sess = db_session.create_session()
        dep = Departments()
        dep.title = form.title.data
        dep.chief = int(form.chief.data)
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.add(dep)
        db_sess.commit()
        return redirect("/dep")
    return render_template('add_dep.html', title='Add a dep', form=form)


@app.route('/dep/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = DepForm()
    db_session.global_init('db/blogs.db')
    if request.method == "GET":
        db_sess = db_session.create_session()
        deps = db_sess.query(Departments).filter(Departments.id == id,
                                                 (Departments.chief == current_user.id) | (
                                                         current_user.id == 1)).first()
        if deps:
            form.title.data = deps.title
            form.chief.data = deps.chief
            form.members.data = deps.members
            form.email.data = deps.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        deps = db_sess.query(Departments).filter(Departments.id == id).first()
        if deps:
            deps.title = form.title.data
            deps.chief = form.chief.data
            deps.members = form.members.data
            deps.email = form.email.data
            db_sess.commit()
            return redirect('/dep')
        else:
            abort(404)
    return render_template('add_dep.html', title='Edit a dep', form=form)


@app.route('/dep_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dep_delete(id):
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    if current_user.id == 1:
        dep = db_sess.query(Departments).filter(Departments.id == id).first()
    else:
        dep = db_sess.query(Departments).filter(Departments.id == id,
                                                Departments.chief == current_user.id).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/dep')


@app.route('/users_show/<int:user_id>', methods=['GET', 'POST'])
def users_show(user_id):
    try:
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={user_api.get_user(user_id).json['user'][0]['city']}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(toponym_coodrinates.split())}&spn=0.1,0.1&l=map"
            response = requests.get(map_request)
            map_file = "static/map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            return render_template('nostalgy.html', name=user_api.get_user(user_id).json['user'][0]['name'],
                                   image=url_for('static', filename='map.png'))
    except Exception:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
