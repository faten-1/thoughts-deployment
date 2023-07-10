from flask import render_template, request, session, redirect
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User

@app.route('/thoughts')
def dashboard():
    #create post
    if 'user_id' in session :
        logged_user = User.get_by_id({'id' : session['user_id']})
        posts=Post.get_all()
        return render_template('dashboard.html', posts=posts,logged_user = logged_user)
    return render_template('/')




@app.route('/posts/new', methods = ['POST'])
def create():
    if not 'user_id' in session:
        redirect('/thoughts')
    if not Post.validation_post(request.form):
        return redirect('/thoughts')


    data = {
        'content': request.form['content'],
        'user_id': session['user_id']

    }
    result = Post.create(data)
    return redirect('/thoughts')


@app.route('/posts/<int:id>/delete')
def delete(id):
    result=Post.delete({"id":id})
    return redirect ('/thoughts')


@app.route('/posts/<int:user_id>')
def user_posts(user_id):
    if 'user_id' in session :
        logged_user = User.get_by_id({'id' : session['user_id']})

        user = User.get_by_id({'id' : user_id})
        if user : 
            user_posts = Post.get_user_posts({'user_id': user_id})
            return render_template('user_posts.html',user=user,user_posts=user_posts,logged_user=logged_user)
        else :
            return redirect('/thoughts')
    
    return redirect('/')

@app.route('/posts/<int:post_id>/like')
def like(post_id):
    Post.like(post_id,session['user_id'])
    return redirect('/thoughts')


@app.route('/posts/<int:post_id>/dislike')
def dislike(post_id):
    Post.dislike(post_id,session['user_id'])
    return redirect('/thoughts')