from app import app, db
from flask import render_template, url_for, redirect, flash, jsonify, request
from app.forms import TitleForm, ContactForm, LoginForm, RegisterForm, PostForm
from app.models import Post, Contact, User
from flask_login import current_user, login_user, logout_user, login_required
import requests


@app.route('/')
@app.route('/index')
@app.route('/index/<header>', methods=['GET'])
def index(header=''):
    products = [
    {
    'id': 1001,
    'title': 'Soap',
    'price': '3.98',
    'desc': 'Very clean soapy soap. Has soapness.',
    },
    {
    'id': 666,
    'title': 'Puppy',
    'price': '4000.00',
    'desc': 'Fill the void until it\'s a dog.'
    },
    {
    'id': 1800,
    'title': 'Yeti Water Bottle',
    'price': '150.00',
    'desc': 'Fit in. Just like everyone else.'
    },
    {
    'id': 9,
    'title': 'Parental Love',
    'price': '50.00',
    'desc': 'The selfish kind.'
    }

    ]
    return render_template('index.html', products=products,title='Home',header=header)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html', title='Checkout')

@app.route('/title', methods=['GET', 'POST'])
def title():
    #create and instance of the form
    form = TitleForm()

    #write a conditional that checks if form was submitted properly, then do something with the DataRequired

    if form.validate_on_submit():
        # print(f'{form.title.data}') #name of form . name of input . data
        return redirect(url_for('index', header=form.title.data))
    return render_template('form.html', form=form, title='Change Title')

@app.route('/login', methods=['GET', 'POST'])
def login():


    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))


    form = LoginForm()

    if form.validate_on_submit():

        #query the database for the user trying to login

        user = User.query.filter_by(email=form.email.data).first()

        #if user doesn't exist, reload page and flash message

        if user is None or not user.check_password(form.password.data):
            flash('Credentials are incorrect')
            return redirect(url_for('login'))

        #if user does exist and the credentials are correct, log them in and send them to their profile page

        login_user(user, remember=form.remember_me.data)

        flash("You are logged in.")
        return redirect(url_for('profile',username=current_user.username))

    return render_template('form.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():


    #check if user is already logged in

    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))

    form = RegisterForm()



    if form.validate_on_submit():

        user =User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            url = form.url.data,
            age = form.age.data,
            bio = form.bio.data
        )

        #set the password password_hash

        user.set_password(form.password.data)

        #add to stage and commit

        db.session.add(user)
        db.session.commit()

        flash("Thanks for registering.")
        return redirect(url_for('login'))

    return render_template('form.html', form=form, title='Register')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        #create instance of db model
        contact = Contact(
            name = form.name.data,
            email = form.email.data,
            message = form.message.data

        )


        #add record
        db.session.add(contact)

        #commit

        db.session.commit()

        flash("Thanks for contacting us, we will be in touch soon.")

        return redirect(url_for('contact'))
    contacts = Contact.query.all()

    return render_template('form.html', form=form, contacts=contacts, title='Contact Us')

# temporary variable for testing. Generally dont declare variables here.

# posts = [
#     {
#         'post_id': 1,
#         'tweet': 'My favorite suit is spades',
#         'date_posted': '6/22/2019'
#     },
#     {
#         'post_id': 2,
#         'tweet': 'Lexi likes wine',
#         'date_posted': '7/16/2019'
#     },
#     {
#         'post_id': 3,
#         'tweet': 'So just a thought...',
#         'date_posted': '7/17/2019'
#     }
# ]
@login_required
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    form = PostForm()

    if form.validate_on_submit():
        #step 1: Create an instance of the db model
        post = Post(
            tweet = form.tweet.data,
            user_id = current_user.id
        )
        #add record
        db.session.add(post)
        #like git commit - adds to the database
        db.session.commit()


        return redirect(url_for('profile',username=username))

    #retrieve all posts and pass in to view

    #pass in user via the username taken in

    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', form=form,user=user, title='Profile')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# /*
# ================================================================================
# # API'S
# ================================================================================
#     */

@app.route('/api/posts/retrieve', methods=['GET'])
def getPosts():
    try:
        username = request.args.get('username')

        #queery the database for the  tweets by a user

        user=User.query.filter_by(username=username).first()

        #traverse through user posts and into new list, the user.posts attribute is actually a class

        data = []

        for post in user.posts:
            data.append(
                {
                'post_id': post.post_id,
                'user_id': post.user_id,
                'tweet': post.tweet,
                'date_posted': post.date_posted
                }
            )


        return jsonify({ 'sucess' : f'Query successful for {username}',
                        'username': username,
                         'posts': data
        })

    except:
        return jsonify({'error' : 'Error #001: invalid parameters' })

@app.route('/api/posts/save', methods=['POST'])
def savePost():
    #grab parameters for posing

    username = request.args.get('username')
    tweet = request.args.get('tweet')

    #query the user table, if user doesnt exist return Error

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error' : 'Error #002: Invalid Parameters'})

    post = Post(user_id=user.id, tweet=tweet)

    db.session.add(post)
    db.session.commit()

    return jsonify({
        'success': 'Tweet posted.',
        'username': user.username,
        'post_data': {
            'post_id': post.post_id,
            'user_id': post.user_id,
            'tweet': post.tweet,
            'date_posted': post.date_posted

        }
    })
