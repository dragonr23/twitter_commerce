from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
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
    return render_template('index.html', products=products,title='Home')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html', title='Checkout')

@app.route('/title')
def title():
    return render_template('form.html', title='Change Title')
