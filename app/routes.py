from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import TitleForm, ContactForm, LoginForm, RegisterForm, PostForm
from app.models import Post, Contact


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
    form = LoginForm()

    if form.validate_on_submit():

        flash("You are logged in.")
        return redirect(url_for('profile'))

    return render_template('form.html', form=form, title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

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
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = PostForm()

    if form.validate_on_submit():
        #step 1: Create an instance of the db model
        post = Post(
            tweet = form.tweet.data
        )
        #add record
        db.session.add(post)
        #like git commit - adds to the database
        db.session.commit()


        return redirect(url_for('profile'))

    #retrieve all posts and pass in to view

    posts = Post.query.all()
    return render_template('profile.html', form=form,posts=posts, title='Profile')
