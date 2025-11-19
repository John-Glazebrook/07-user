from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

db = SQLAlchemy()
#migrate = Migrate()

class User(db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True)
    # TODO: do we want usernames? Or is email enough?
    # username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    # TODO: add a hashed password

    articles = db.relationship(
                'Article',
                back_populates='user',
                lazy=True,
                cascade="all, delete-orphan"
            )

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get_by_email(cls, email):
        return db.session.query(cls).filter(cls.email == email).first()

    def __repr__(self):
        return f'<User {self.id} {self.email!r}>'


class Article(db.Model):
    __tablename__ = 'news'
    id      = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    title   = db.Column(db.String(200), nullable=False)
    body    = db.Column(db.Text, nullable=False)
    url     = db.Column(db.String(500))
    author  = db.Column(db.String(100))
    user_id = db.Column(
                db.Integer,
                # the FK name is needed for SQLite migrations to work
                # see PowerPoint for more details
                db.ForeignKey('users.id', name='fk_news_user_id'),
                nullable=False
            )
    user    = db.relationship('User', back_populates='articles')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Article {self.id} {self.title!r}>'

