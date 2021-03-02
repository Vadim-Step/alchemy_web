from flask import Flask
from data.user import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    # app.run()


if __name__ == '__main__':
    main()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    user = User()
    user.surname = "Pupkin"
    user.name = "Vasily"
    user.age = 19
    user.position = "captain assistant"
    user.speciality = "python developer"
    user.address = "module_1"
    user.email = "pup_vas@mars.org"
    db_sess.add(user)
    db_sess.commit()
    user = User()
    user.surname = "Petrov"
    user.name = "Aleksandr"
    user.age = 22
    user.position = "doctor"
    user.speciality = "surgeon"
    user.address = "module_2"
    user.email = "pet_alek@mars.org"
    db_sess.add(user)
    db_sess.commit()
    user = User()
    user.surname = "Sidorov"
    user.name = "Kirill"
    user.age = 23
    user.position = "html developer"
    user.speciality = "flight engineer"
    user.address = "module_2"
    user.email = "sid_kir@mars.org"
    db_sess.add(user)
    db_sess.commit()

