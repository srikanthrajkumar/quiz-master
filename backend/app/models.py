from . import db

from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Time, Text
from sqlalchemy.orm import relationship

from datetime import datetime

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    qualification = Column(String(100))

    active = Column(Boolean, default=True)
    last_login_at = Column(DateTime)
    current_login_at = Column(DateTime)
    fs_uniquifier = Column(String(64), unique=True, nullable=False)

    roles = relationship('Role', secondary='user_roles', backref='users')
    scores = relationship('Score', backref='user', cascade="all, delete-orphan")

class Subject(db.Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)

    chapters = relationship('Chapter', backref='subject', cascade="all, delete-orphan")

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    subject_id = Column(Integer, ForeignKey('subject.id', ondelete='CASCADE'))

    quizzes = relationship('Quiz', backref='chapter', cascade="all, delete-orphan")

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    chapter_id = Column(Integer, ForeignKey('chapter.id', ondelete='CASCADE'))
    date_of_quiz = Column(DateTime, nullable=False, default=datetime.utcnow)
    time_duration = Column(Time)
    remarks = Column(Text)

    questions = relationship('Question', backref='quiz', cascade="all, delete-orphan")
    scores = relationship('Score', backref='quiz', cascade="all, delete-orphan")

class Question(db.Model):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id', ondelete='CASCADE'))
    question_statement = Column(Text, nullable=False)
    option1 = Column(String(255), nullable=False)
    option2 = Column(String(255), nullable=False)
    option3 = Column(String(255))
    option4 = Column(String(255))
    correct_option_index = Column(Integer, nullable=False)
    photoURL = Column(String(512))

class Score(db.Model):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    time_stamp_of_attempt = Column(DateTime, default=datetime.utcnow)
    total_scored = Column(Integer)
    remarks = Column(Text)