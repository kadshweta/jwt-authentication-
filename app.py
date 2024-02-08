from flask import Flask,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from flask_jwt_extended import create_access_token,JWTManager

app=Flask(__name__)


app.config['SECRET_KEY']='SUPER-SECRET-KEY'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database1.db'

db=SQLAlchemy(app)
api=Api(app)
jwt=JWTManager(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    password=db.Column(db.String(200))

# db.create_all() 


class User_register(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']

        password=data['password']

        if not username or not password:
            return {'msg':'missing username or password '},400
        
        if User.query.filter_by(username=username).first():
            return {'msg':'user already taken'},400
        
        new_user=User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'msg':'user created succesfully '},200

class user_login(Resource):
     def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        
        user=User.query.filter_by(username=username).first()
            
        if user and user.password == password:
            access_token=create_access_token(identity=user.id)
           
            return {'access_token':access_token},200
        
        return {'msg':'okay'},200
    
api.add_resource(User_register,'/register')
api.add_resource(user_login,'/login')

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)




    





# Flask JWT Token-Based Authentication | Building a Secure RESTful API with Flask-JWT-Extended | HINDI