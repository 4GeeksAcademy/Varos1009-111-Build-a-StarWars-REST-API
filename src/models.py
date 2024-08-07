from flask_sqlalchemy import SQLAlchemy
 

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
   
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planets = db.relationship('FavoritePlanets', back_populates='user')
    favorite_people = db.relationship('FavoritePeople', back_populates='user')


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = 'people'  
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(30), nullable = False, unique = False )


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Planets(db.Model): 
    __tablename__ = 'planets' 
    id = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(30), nullable = False, unique = False )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        } 

class FavoritePeople(db.Model):  
    __tablename__ = 'favoritePeople'
    id = db.Column(db.Integer, primary_key=True)   
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False )
    people_id = db.Column(db.Integer,db.ForeignKey('people.id'), nullable = False)
    
    
    user = db.relationship(User)
    people = db.relationship(People)
   
    

    def serialize(self):
        return {
            "id": self.id,
            'user_id' : self.user_id,
            'people_id': self.planets_id
        } 
     
class FavoritePlanets(db.Model):  
    __tablename__ = 'favoritePlanets'
    id = db.Column(db.Integer, primary_key=True)   
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False )
    planets_id = db.Column(db.Integer,db.ForeignKey('planets.id'), nullable = False )
    
    user = db.relationship(User)
    planets = db.relationship(Planets)
    

    def serialize(self):
        return {
            "id" : self.id,
            'user_id' : self.user_id,
            'planets_id': self.planets_id
        } 
     
