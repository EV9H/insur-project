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
from backend.ml.ml import *
from backend.ml.ml2 import *


'''
GLOBAL VAR
'''
AccId = None
user = None

@app.route('/')
def index():
    return render_template('index.html', session = session)


class QuoteForm(Form):
    age = IntegerField('Age (1-100)')
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    income = IntegerField('Annual Income (20,000$-200,000$)')
    health_rating = IntegerField('Health Rating (1-100)')
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

class SignupForm(Form):
    accountID = StringField("AccountID")
    name = StringField("Name")
    password = StringField("Password")
    email = StringField("Email")
    ssn = StringField("Ssn")

class AssessmentForm(Form):
    age = StringField("Age (1-100)")
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    income = IntegerField('Income (20000-200000)')
    health_rating = IntegerField('Health Rating(1-100)')
    married = BooleanField('Married')
    purchased = BooleanField('Purchased Before?')

class CustomerIDForm(Form):
    AccID = StringField("Account ID")

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
            session['AccID'] = account
            return redirect("/")
        else:
            msg = "Wrong credentials."
    return render_template('login.html', loginForm=loginForm, msg = msg)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("LOGGED_IN", None)
    session.pop("AccID", None)
    return redirect("/")

# front-end for sign-up: account password email Accname Active = 1
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    signupForm = SignupForm(request.form)
    if request.method == 'POST' and signupForm.validate():
        account = signupForm.accountID.data
        password = signupForm.password.data
        name = signupForm.name.data 
        email = signupForm.email.data
        ssn = signupForm.ssn.data
        active = 1
        qs = QuerySender()
        query = "SELECT AccID, Password FROM Account WHERE AccID = %s AND Password = %s"
        result = qs.execute(query, params=(str(account), str(password)), auto_close = False)
        if result:
            msg = "Account already Exists!"
        else:     
            query = """
                INSERT INTO Account (AccID, Password, Email, Active, AccName)
                VALUES (%s, %s, %s, %s, %s)
            """
            result2 = qs.execute(query, (str(account), str(password), str(email), str(active), str(name)), auto_close=False)
            
            qs.execute("""INSERT INTO Customer(Fname, Ssn) VALUES(%s,%s)""", params=(name, ssn), auto_close=False)
            qs.execute("""INSERT INTO Account_owner(Ssn, AccID) VALUES(%s,%s)""", params=(ssn, account))
            qs.close()
            
            # RETRAIN 
            
            
            session["LOGGED_IN"] = False
            return redirect("/login")
        
    # qs = QuerySender()
    # query = "SELECT AccID FROM Account WHERE AccID = %s"
    # result = qs.execute(query, params=(str(account)), auto_close=False)
    # if result:
    #     print("AccID already exists")
    # else:
    #     query = """
    #         INSERT INTO Account (AccID, Password, Email, Active, AccName)
    #         VALUES (%s, %s, %s, %s, %s)
    #     """
    #     result2 = qs.execute(query, (str(account), str(password), str(email), str(active), str(acc_name)))

    return render_template('signup.html', form=signupForm, msg = msg)




########### QUOTE, PURCHASE #####################
@app.route('/get_quote', methods=['GET', 'POST'])
def get_quote():
    form = QuoteForm(request.form)
    quote = ''
    if request.method == 'POST' and form.validate():
        age = form.age.data
        pre_gender = form.gender.data
        gender = 0
        if pre_gender == "male":
            gender = 1
        income = form.income.data
        health_rating = form.health_rating.data
        nChildren = form.nChildren.data
        married = form.married.data
        purchased = form.purchased.data

        # Calculate quote based on input fields
        def calculate_premium(age, gender, income, health_rating, married):
            model = get_reg()
            new_x = [(int(age), int(gender), float(income), float(health_rating), int(married))]
            p = model.predict_proba(new_x)[:, 1][0]
            r = p * 100000
            return r

        quote = int(calculate_premium(age, gender, income, health_rating, married)/12)
        session['quote_info'] = [age, gender, income, health_rating, married, purchased]
        session['quote'] = quote
    return render_template('get_quote.html', form=form, quote = quote)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    quote_info = session['quote_info']
    quote = session['quote']
    pForm = PurchaseForm(request.form)
    # pForm.plan.data = 'planA'
    msg = ''
    if request.method == 'POST' and pForm.validate():
        plan = pForm.plan.data
        planname = ""
        if plan == "planA":
            planname = "Plan A"
        elif plan == "planB":
            planname = "Plan B"
        else:
            planname = "Plan C"
        userID = session['AccID']
        quote_info.append(userID)


       
        db = pymysql.connect(
            host='insurance-database.cdcuzzna0mo5.us-east-2.rds.amazonaws.com',
            user='admin',
            password='12345678',
            port = 3306,
            database="insdb"
        )
        cursor = db.cursor()
        q = """
            UPDATE Customer
            SET Age = %s,Gender = %s, Income= %s, Health_rating= %s, Married= %s, Purchased = %s
            WHERE Customer.Ssn = (
                SELECT Account_owner.Ssn FROM Account_owner
                WHERE Account_owner.AccID = %s
            )
        """
        cursor.execute(q, quote_info)
        cursor.execute("""SELECT MAX(CAST(CID AS UNSIGNED))  FROM Contract""")
        CID = str(int(cursor.fetchall()[0][0])+ 1)
        # app.logger.debug(CID)
        q = """
            INSERT INTO Contract(CID, Amount, Status, Assc_Ssn, Plan_Name, AccID)
            VALUES(%s, %s,%s,%s,%s,%s)
        """
        cursor.execute(q, [CID, quote, 1, '111-11-1111', planname, userID])
        
        
        cursor.close()
        db.commit()
        db.close()
        msg = "Purchase successful! You can see your order in My Products page."
    return render_template('purchase.html', pForm = pForm, quote = quote, quote_info = quote_info, msg = msg)


########### MY PRODUCTS #####################
@app.route('/my_products', methods=['GET', 'POST'])
def my_products():
    products = []
    if session['AccID']:    
        userID = session['AccID']
        qs = QuerySender()
        q = '''SELECT CID, Plan_Name, Status, Amount, Assc_Ssn FROM Contract 
            INNER JOIN Account ON Account.AccID = Contract.AccID
            WHERE Contract.AccID = %s
        '''
        data = qs.execute(q, params=(userID))
        
        print(data)
        for i in range(len(data)):
            CID = data[i][0]
            name = data[i][1]
            status = data[i][2]
            amount = data[i][3]
            assc = data[i][4]
                        
            products.append({
                'CID': CID,
                'name': name,
                'payment': amount,
                'status':status,
                'assc': assc
            })
        return render_template('my_products.html', products = products)
    else: 
        return redirect('/login')

@app.route('/get_contract', methods=['GET', 'POST'])
def get_contract():
    products = []
    msg = ""
    form = CustomerIDForm(request.form)
    if request.method == 'POST' and form.validate():
        
        userID = form.AccID.data
        qs = QuerySender()
        q = '''SELECT CID, Plan_Name, Status, Amount, Assc_Ssn FROM Contract 
            INNER JOIN Account ON Account.AccID = Contract.AccID
            WHERE Contract.AccID = %s
        '''
        data = qs.execute(q, params=(userID))
        
        if data:
            for i in range(len(data)):
                CID = data[i][0]
                name = data[i][1]
                status = data[i][2]
                amount = data[i][3]
                assc = data[i][4]
                            
                products.append({
                    'CID': CID,
                    'name': name,
                    'payment': amount,
                    'status':status,
                    'assc': assc
                })
        else: 
            msg = "No account/Contract in database"
    return render_template('get_contract.html', form = form, products = products,msg = msg)



# frontend required
@app.route('/assess', methods=['GET', 'POST'])
def assess():
    train_knn()
    form = AssessmentForm(request.form)
    
    msg = 'Fill all related customer info and wait for Result ...'
    if request.method == 'POST' and form.validate():
        
        # age = 55
        # gender = 1
        # income = 123123
        # health_rating = 20
        # married = 0

        age = form.age.data
        gender = form.gender.data
        income = form.income.data
        health_rating = form.health_rating.data
        married = form.married.data
        gender = 1 if gender == 'male' else 0
        def get_appr(age1, gender1, income1, health_rating1, married1):
            new_x = [(int(age1), int(gender1), float(income1), float(health_rating1), int(married1))]
            model = get_knn()
            result1 = model.predict(new_x)
            return result1

        result = get_appr(age, gender, income, health_rating, married)[0]
        if result == 1:
            msg = "Potential customer"
        else: 
            msg = "Not a potential customer"
        
    
    return render_template('assess.html', msg = msg, form = form)





if __name__ == '__main__':
    app.run()
