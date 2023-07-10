from flask_app.config.mysqlconnection import connectToMySQL,DB
from flask import flash
import re
from flask_app.models.user import User

class Post:


    def __init__(self,data):
        self.id=data['id']
        self.content=data['content']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.users_who_favorited =[]
        self.user_ids_who_favorited = []


    @classmethod
    def create(cls,data):
        query = "INSERT INTO posts (content,user_id) VALUES (%(content)s,%(user_id)s);"
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def get_all(cls):
        #query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ;"
        
        query = """
            select * from posts join users AS creators on posts.user_id = creators.id
            left join users_has_favorited on posts.id = users_has_favorited.post_id 
            left join users as users_who_favorited on users_has_favorited.user_id = users_who_favorited.id
            ORDER BY posts.id;

        """
        results = connectToMySQL(DB).query_db(query)

        posts = []
        for row in results:

            new_post = True
            users_who_favorited_data = {
                'id':row['users_who_favorited.id'],
                'first_name':row['users_who_favorited.first_name'],
                'last_name':row['users_who_favorited.last_name'],
                'email':row['users_who_favorited.email'],
                'password':row['password'],
                'created_at':row['users_who_favorited.created_at'],
                'updated_at':row['users_who_favorited.updated_at']
            }

            number_of_posts = len(posts)
            if number_of_posts > 0 :
                last_post = posts[number_of_posts - 1]
                if last_post.id == row['id']:
                    last_post.users_who_favorited.append(User(users_who_favorited_data))
                    last_post.user_ids_who_favorited.append(users_who_favorited_data['id'])
                    new_post = False

            if new_post:
                post = cls(row)
                user_dict = {
                    'id':row['creators.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['creators.created_at'],
                    'updated_at':row['creators.updated_at']
                }
                post.user =   User(user_dict)
                if row['users_has_favorited.id']:
                    post.users_who_favorited.append(User(users_who_favorited_data))
                    post.user_ids_who_favorited.append(users_who_favorited_data['id'])
                    
                posts.append(post)

        return posts

    @classmethod
    def delete(cls,data):
        query= "DELETE FROM posts WHERE id = %(id)s ;"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod   
    def get_user_posts(cls,data):
        query = """
            SELECT * FROM posts WHERE user_id = %(user_id)s;
        """
        results = connectToMySQL(DB).query_db(query, data)
        # print(results)
        posts = []
        for row in results:
            post = cls(row)
            posts.append(post)
        return posts

    @classmethod
    def like(cls,post_id,user_id):
        query = "insert into users_has_favorited (post_id,user_id) VALUES (%(post_id)s,%(user_id)s)"
        data = {
            'post_id':post_id,
            'user_id':user_id
        }
        return connectToMySQL(DB).query_db(query,data)

    @classmethod
    def dislike(cls,post_id,user_id):
        query = """
            delete from users_has_favorited
            where post_id = %(post_id)s AND user_id =  %(user_id)s
            """
        data = {
            'post_id':post_id,
            'user_id':user_id
        }
        return connectToMySQL(DB).query_db(query,data)

    @staticmethod
    def validation_post(post):
        is_valid = True
        if post['content'] =="":
            flash('Required field',"post")
            is_valid=False
        if post['content']:
            if len(post['content'])<5:
                flash('Thought should be at least 5 characters',"post")
                is_valid=False
        return is_valid






