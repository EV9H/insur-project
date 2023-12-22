from flask import Flask, render_template, request, redirect, session
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, IntegerField, SelectField, BooleanField
import sys


app = Flask(__name__)
app.debug = True
app.secret_key = "SECRETKEY"
# app.config['SECRET_KEY'] = 'secret'
bootstrap = Bootstrap(app)

import os
sys.path.insert(0, os.path.abspath('../'))
from backend.api import *
from backend.util.db_query import *




'''
GLOBAL VAR
'''
AccId = None
user = None

@app.route('/')
def index():
    return render_template('index.html', session = session)


class QuoteForm(Form):
    age = IntegerField('Age')
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    income = IntegerField('Income')
    health_rating = IntegerField('Health Rating')
    nChildren = IntegerField('# of Children')
    married = BooleanField('Married')
    purchased = BooleanField('Purchased Before?')
    
class RegisterForm(Form):
    AccID = StringField('* Account Name')
    password = StringField('password')
    email= StringField('email')
    ssn = StringField('SSN')
    name = StringField('Name')
    age = IntegerField('Age')
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    income = IntegerField('Income')
    health_rating = IntegerField('Health Rating')
    nChildren = IntegerField('# of Children')
    married = BooleanField('Married')
    purchased = BooleanField('Purchased Before?')
    
class PurchaseForm(Form):
    plan = SelectField('Plan', choices=[('planA', 'Plan A'), ('planB', 'Plan B'), ('planC', 'Plan C')])
    # amount = IntegerField('Purchase Value')

class LoginForm(Form):
    account = StringField("Account")
    password = StringField("Password")



########### AUTHENTICATIONS ###################
def auth(account, password, role = "Customer"):
    if account == "admin" and password == "12345":
        # global LOGGED_IN
        session["LOGGED_IN"] = True
        return True
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm(request.form)
    app.logger.debug("LOGIN SCREEN ----------------")
    msg = ""
    if "LOGGED_in" in session and session["LOGGED_IN"]: 
        return redirect("/")
    if request.method == 'POST' and loginForm.validate():
        app.logger.debug("A debug message 2 " )
        account = loginForm.account.data
        password = loginForm.password.data
        qs = QuerySender()
        query = "SELECT AccID, Password FROM Account WHERE AccID = %s AND Password = %s"
        result = qs.execute(query, params=(str(account), str(password)))
        if result:
            session["LOGGED_IN"] = True
            return redirect("/")
        else:
            msg = "Wrong credentials."
    return render_template('login.html', loginForm=loginForm, msg = msg)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("LOGGED_IN", None)
    
    return redirect("/")

# front-end for sign-up: account password email Accname Active = 1
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    account = "test2"
    password = "23456"
    email = "abc@gmail.com"
    acc_name = "Evan Huang"
    active = 1
    qs = QuerySender()
    query = "SELECT AccID FROM Account WHERE AccID = %s"
    result = qs.execute(query, params=(str(account)), auto_close=False)
    if result:
        print("AccID already exists")
    else:
        query = """
            INSERT INTO Account (AccID, Password, Email, Active, AccName)
            VALUES (%s, %s, %s, %s, %s)
        """
        result2 = qs.execute(query, (str(account), str(password), str(email), str(active), str(acc_name)))






########### QUOTE, PURCHASE #####################
@app.route('/get_quote', methods=['GET', 'POST'])
def get_quote():
    form = QuoteForm(request.form)
    quote = ''
    if request.method == 'POST' and form.validate():
        age = form.age.data
        gender = form.gender.data
        income = form.income.data
        health_rating = form.health_rating.data
        nChildren = form.nChildren.data
        married = form.married.data
        purchased = form.purchased.data

        # Calculate quote based on input fields
        def calculate_quote( age, gender, income, health_rating, nChildren, married, purchased):
            return 100 / health_rating * 5000; 

        quote = int(calculate_quote(age, gender, income, health_rating, nChildren, married, purchased))
        session['quote'] = quote
    return render_template('get_quote.html', form=form, quote = quote)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    # regForm = RegisterForm(request.form)
    quote = session['quote']
        
    # if request.method == 'POST' and regForm.validate():
    #     AccID = regForm.AccID.data
    #     password = regForm.password.data
    #     email = regForm.email.data
    #     name = regForm.name.data 
        
        
    #     age = regForm.age.data
    #     gender = regForm.gender.data
    #     income = regForm.income.data
    #     health_rating = regForm.health_rating.data
    #     nChildren = regForm.nChildren.data
    #     married = regForm.married.data
    #     purchased = regForm.purchased.data
    
    pForm = PurchaseForm(request.form)
    pForm.plan.data = 'planA'
    # PFORM
    # planSelected = pForm.plan.data 
    # if planSelected == 'planB':
    #     quote = int(quote * 1.5)
    # elif planSelected == 'planC':
    #     quote = int(quote*2)
    if request.method == 'POST' and pForm.validate():
        plan = pForm.plan.data
        # amount = pForm.amount.data
        
        
    return render_template('purchase.html', pForm = pForm, quote = quote)


########### MY PRODUCTS #####################
@app.route('/my_products', methods=['GET', 'POST'])
def my_products():
    products = []
    
    for i in range(10):
        name = "A"+str(i)
        price = str(10000+i)
        
        description = "THIS IS PRODUCT A " + str(i)
        products.append({
            'name': name,
            'price': price,
            'description': description
        })
    return render_template('my_products.html', products = products)


########### manage #####################
@app.route('/manage', methods=['GET', 'POST'])
def manage():
    
    
    return render_template('manage.html')



if __name__ == '__main__':
    app.run()
