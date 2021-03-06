from flask import Flask, render_template
from data import db_session
from sqlalchemy import orm

from data.db_session import create_session
from data.job import Jobs
from data.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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
            print(i)
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


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
