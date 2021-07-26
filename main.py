from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import String, Integer, DateTime
import datetime
import json

with open('config.json', 'r') as config:
    databasePARA = json.load(config)['databasePARA']
with open('timetable.json', 'r') as timetable:
    fitnessClass = json.load(timetable)['fitness_class']
with open('timetable.json', 'r') as timetable:
    muscleClass = json.load(timetable)['muscle_class']
with open('timetable.json', 'r') as timetable:
    bodyBuilding = json.load(timetable)['body_building']
with open('timetable.json', 'r') as timetable:
    yogaTraining = json.load(timetable)['yoga_training']
with open('timetable.json', 'r') as timetable:
    advanceTraining = json.load(timetable)['advance_training']

app = Flask(__name__)
engine = create_engine(databasePARA.get('URI'))
Base = declarative_base()
Session = sessionmaker(bind=engine)
db = Session()


class query(Base):
    __tablename__ = 'query'
    Q_ID = Column(Integer, primary_key=True)
    Q_DATE = Column(DateTime)
    Q_NAME = Column(String(20))
    Q_EMAIL = Column(String(50))
    Q_SUBJECT = Column(String(20))
    Q_MESSAGE = Column(String(100))


class day(Base):
    __tablename__ = 'day'
    dayID = Column(Integer, primary_key=True)
    day = Column(String)


class timing(Base):
    __tablename__ = 'timing'
    timeID = Column(Integer, primary_key=True)
    timing = Column(String)


class classes(Base):
    __tablename__ = 'classes'
    classID = Column(Integer, primary_key=True)
    className = Column(String)


class trainer_data(Base):
    __tablename__ = 'trainer_data'
    trainerID = Column(Integer, primary_key=True)
    trainerName = Column(String)
    trainerType = Column(String)
    trainerBio = Column(String)


class timetable(Base):
    __tablename__ = 'timetable'
    id = Column(Integer, primary_key=True)
    day = Column(String)
    classes = Column(String)
    time = Column(String)
    trainer = Column(String)


class courcedata(Base):
    __tablename__ = 'courcedata'
    courceID = Column(Integer, primary_key=True)
    courceName = Column(String)
    courceData = Column(String)


class ourclasses(Base):
    __tablename__ = 'ourclasses'
    classesID = Column(Integer, primary_key=True)
    classesNumber = Column(String)
    classesData = Column(String)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = query(Q_DATE=datetime.datetime.now(), Q_NAME=name,
                      Q_EMAIL=email, Q_SUBJECT=subject, Q_MESSAGE=message)
        db.add(entry)
        db.commit()
    courcedetails = db.query(courcedata).all()
    classesdetails = db.query(ourclasses).all()
    return render_template('index.html', fitnessClass=fitnessClass, muscleClass=muscleClass, bodyBuilding=bodyBuilding, yogaTraining=yogaTraining, advanceTraining=advanceTraining, courcedetails=courcedetails, classesdetails=classesdetails)


@app.route('/hello')
def hello():
    return "<h1>hello</h1>"


if __name__ == '__main__':
    app.run(debug=True)
