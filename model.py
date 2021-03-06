'''Models for MN Coffee Roasters App'''

# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_login import LoginManager




# app = Flask(__name__)
db = SQLAlchemy()

class User(db.Model):
    '''A user'''

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.first_name} {self.last_name}>'


    # backref='lists'

class Roaster(db.Model):
    '''A Coffee Roaster'''

    __tablename__ = 'roasters'

    roaster_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    hours = db.Column(db.String(300))
    website = db.Column(db.String(100))
    place_id = db.Column(db.String(50))
    avg_user_rating = db.Column(db.Float)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    
    def __repr__(self):
        return f'<Roaster roaster_ID={self.roaster_id} name={self.name}>'

    # backref='entries'


class List(db.Model):
    '''List for user to add entries to
    
    Consider creating sub-class for each type of list'''

    __tablename__ = 'lists'

    list_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    list_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', backref='lists')
    entries = db.relationship('Entry')    
 

    def __repr__(self):
        return f'<List list_ID={self.list_id} list_name={self.list_name}>'


class Entry(db.Model):
    '''Entry onto list (includes rating and review for roaster)'''

    __tablename__ = 'entries'

    entry_id = db.Column(db.Integer, 
                        primary_key=True,
                        autoincrement=True
                        )
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'), nullable=False)
    roaster_id = db.Column(db.Integer, db.ForeignKey('roasters.roaster_id'), nullable=False)
    score = db.Column(db.Float)
    note = db.Column(db.Text)

    entry_list = db.relationship('List')
    roaster = db.relationship('Roaster', backref='entries')    
 

    def __repr__(self):
        return f'<Entry entry_id={self.entry_id} score={self.score} roaster={self.roaster.name} list={self.entry_list.list_name} author={self.entry_list.user_id}>'


class LoginForm(FlaskForm):
    '''Flask-WTForms class for logging in user'''

    email = StringField('email')
    password = PasswordField('password')

class NewUserForm(FlaskForm):
    fname = StringField('first')
    lname = StringField('last')
    email = StringField('email')
    password = PasswordField('password')


def example_data():
    '''Create sample data and database for testing'''

    Roaster.query.delete()
    User.query.delete()
    List.query.delete()
    Entry.query.delete()

    # Add sample data
    fake_roaster = Roaster(name='City Girl Coffee Test', 
                                    address='1330 E Superior St, Duluth, MN 55805, USA', 
                                    phone_number='(800) 438-9228',
                                    hours='Unavailable',
                                    place_id='ChIJAQDAwtZSrlIRBDSDAdzoufI', 
                                    website='http://www.citygirlcoffee.com/', 
                                    avg_user_rating=3.5, 
                                    lat=46.7998429, 
                                    lng=-92.0807345)
                    
    fake_user = User(first_name='Admin', 
                                last_name='Admin', 
                                email='admin@admin.com', 
                                password='admin')
    db.session.add(fake_roaster)
    db.session.add(fake_user)
    
    fake_list1 = List(list_name='My Favorites', user=fake_user)
    db.session.add(fake_list1)
    fake_list2 = List(list_name='My Roasters', user=fake_user)
    db.session.add(fake_list2)
    
    fake_entry1 = Entry(entry_list=fake_list1,
                                    roaster=fake_roaster, 
                                    score=5.0, 
                                    note='lovely')
    db.session.add(fake_entry1)

    db.session.commit()



'''Copied from model.py in ratings app that connects to the database'''

def connect_to_db(flask_app, db_uri='postgresql:///MNroasters', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)

