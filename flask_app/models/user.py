from flask_app.config.mysqlconnection import connectToMySQL ,DB
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import session , flash
import re

bcrypt= Bcrypt(app)
class User:
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DB).query_db(query)
        users =[]
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            return cls(results[0])
        return False


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            return cls(results[0])
        return False


    @classmethod
    def register(cls,data):
        encrypted_password = bcrypt.generate_password_hash(data['password'])
        new_dict = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' : encrypted_password
        }
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        result = connectToMySQL(DB).query_db(query,new_dict)
        session['user_id'] = result
        return result


    @staticmethod
    def validation_registration(user):
        is_valid = True
        user_in_db = User.get_by_email(user)

        if not user['email']:
            flash('Email is required',"register")
            is_valid=False
        if  user['email']:
            if user_in_db :
                flash("Email already exists in db","register")
                is_valid=False
            if not User.EMAIL_REGEX.match(user['email']):
                flash('invalid email',"register")
                is_valid=False
        
        if not user['first_name']:
            flash('first name is required',"register")
            is_valid=False
        if  user['first_name']:
            if len(user['first_name']) < 2 :
                flash("First name need to be longer than 2  caracters","register")
                is_valid = False

        if not user['last_name']:
            flash('last name is required',"register")
            is_valid=False
        if  user['last_name']:
            if len(user['last_name']) < 2 :
                flash("Last name need to be longer than 2   caracters","register")
                is_valid = False

        if not user['password']:
            flash('password is required',"register")
            is_valid=False
        if  user['password']:
            if len(user['password']) < 8 :
                flash("password too short","register")
                is_valid = False

        if not user['password'] == user['confirm_password']:
            flash("passwords dont match","register")
            is_valid = False

        return is_valid


    @staticmethod
    def validation_login(user):
        is_valid=True

        if not user['email']:
            flash('Email is required',"login")
            is_valid=False
        if  user['email']:
            user_in_db = User.get_by_email({'email':user['email']})
        
            if not User.EMAIL_REGEX.match(user['email']):
                flash('invalid email',"login")
                is_valid=False

        if not user['password']:
            flash('password is required',"login")
            is_valid=False
        if  user['password']:
            

            if not user_in_db:
                flash("email is not associated with an account","login")
                is_valid=False

            if user_in_db:
                if len(user['password']) < 8 :
                    flash("password too short","login")
                    is_valid = False
                if not bcrypt.check_password_hash(user_in_db.password,user['password']):
                    flash("incorrect password","login")
                    is_valid=False

        if is_valid==True:
            session['user_id'] = user_in_db.id

        return is_valid








