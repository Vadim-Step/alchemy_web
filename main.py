from flask import Flask, render_template
from flask_login import login_user
from werkzeug.utils import redirect
from flask_login import LoginManager
from data import db_session
from data.db_session import create_session
from data.job import Jobs
from data.job_form import JobForm
from data.log_form import LoginForm
from data.reg_form import RegForm
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
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
        lst.append(row)
    return render_template('index.html', lst=lst)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session.global_init('db/blogs.db')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(form.password.data)
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
    return render_template('job.html', form=form)


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
        db_sess.add(user)
        db_sess.commit()
        return redirect("/tab1")
    return render_template('reg.html', form=form)


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
