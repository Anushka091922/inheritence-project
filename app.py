from flask import Flask, request, redirect, render_template, url_for, flash, jsonify, make_response, json
from sqlalchemy.dialects.postgresql import JSON
from COI import laws
import string
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import Length, InputRequired, ValidationError, DataRequired
from sqlalchemy import Column, Integer, String, Float, ARRAY
from flask_bcrypt import Bcrypt
import os
from pathlib import Path
from text_summary import text_summary

from flask import Flask, render_template, request
import requests

ID = 0

app = Flask(__name__)
app.secret_key = 'cb5b93ad8f1b4eceb0db22fa6105df83'
# app = Flask(__name__)
bcrypt = Bcrypt(app)


# app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'Thisissecret'

db = SQLAlchemy(app)
Law = SQLAlchemy(app)


@app.route('/index')
def index():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=7e1737d3191d4fe894fc579df01b7bde"
    r = requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('index.html', cases=case)


@app.route('/sports')
def sports():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=7e1737d3191d4fe894fc579df01b7bde"
    r = requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('sports.html', cases=case)


@app.route('/business')
def business():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=7e1737d3191d4fe894fc579df01b7bde"
    r = requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('business.html', cases=case)


@app.route('/technology')
def technology():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=7e1737d3191d4fe894fc579df01b7bde"
    r = requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('tech.html', cases=case)


@app.route('/science')
def science():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=7e1737d3191d4fe894fc579df01b7bde"
    r = requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('science.html', cases=case)


@app.route('/health')
def health():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=7e1737d3191d4fe894fc579df01b7bde"
    r = requests.get(url).json()
    case = {
        'articles': r['articles']
    }
    return render_template('health.html', cases=case)


# if __name__ == '__main__':
#     app.run(debug=True)


# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"


# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))


@app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
def dashboard():
    return render_template('dashboard.html')


# @app.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

@app.route('/community', methods=['GET', 'POST'])
# @login_required
def community():
    return render_template('community.html')


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')


@app.cli.command('db_seed')
def db_seed():
    test_user = Review(
        username='Peter',
        # last_name='Galilei',
        # email='george@test.com',
        Review="This is amazing website",
        Rating="4.6")

    db.session.add(test_user)
    # db.session.add(test_law)
    db.session.commit()
    print('Database seeded')


# @app.cli.command('db_seed_all')
# def db_seed_all():
#     for i in range(35):
#         new_law = "("
#         object = jsonify(laws[0][i])
#         for key in object:
#             new_law.append(object.keys())
#             new_law.append("=")


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')


@app.route('/')
def hello_world():
    global ID
    obj = Review.query.all()
    last_obj = obj[-1]
    ID = last_obj.id
    user1 = Review.query.filter_by(id=ID-5).first()
    user2 = Review.query.filter_by(id=ID-4).first()
    user3 = Review.query.filter_by(id=ID-3).first()
    user4 = Review.query.filter_by(id=ID-2).first()
    user5 = Review.query.filter_by(id=ID-1).first()
    user6 = Review.query.filter_by(id=ID).first()
    # return render_template('main.html')
    return render_template('main.html', user1=user1, user2=user2, user3=user3, user4=user4, user5=user5, user6=user6)
    # return render_template('newkanun.html')


@app.route('/super_simple')
def super_simple():
    return 'Hello World, its super simple!!'


@app.route('/not_found')
def not_found():
    return 'Not found', 404


@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')


@app.route('/Emer')
def Emer():
    return render_template('emergency.html')


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return 'You are not allowed', 404
    else:
        return 'You are welcomed', 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                # login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=request.form['username']).first()
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 # login_user(user)
#                 return redirect(url_for('dashboard'))
#     return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/search')
def search():
    return render_template('Search.html')


@app.route('/laws', methods=['POST'])
def laws():
    obj = request.form['Key1']
    return obj


# @app.route('/data', methods=['GET', 'POST'])
# def data():
#     str = ""
#     nl = "<html > <body > <br > </body > </html >"
#     if request.method == 'POST':
#         obj = request.form['keyword']
#         with open("C:\\Users\\Bhoomika\\KANUN_Inheritance\\COI.json", encoding='utf-8') as JsonFile:
#             data = json.load(JsonFile)
#             jsonData = data["laws"]
#             for i in range(35):
#                 if obj in jsonData[i]['Name']:
#                     if "ArtDesc" in jsonData[i]:
#                         str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>"+ \
#                             jsonData[i]['ArtNo']+nl + \
#                             "<html><body><b>ArtDesc : </b></body></html>": "+jsonData[i]['ArtDesc']
#                     else:
#                         str = str+nl+nl+nl+"<html><body><b>ArtNo : </b></body></html>" : "+jsonData[i]['ArtNo']
#                         if "Clauses" in jsonData[i]:
#                             clause = jsonData[i]["Clauses"]
#                             for l in clause:
#                                 str = str+nl+nl+"ClauseNo: "+l['ClauseNo']
#                                 if "SubClauses" in l:
#                                     SubClauses = l['SubClauses']
#                                     for j in SubClauses:
#                                         str = str + nl+"SubClauseNo : " + \
#                                             j['SubClauseNo']+nl+"SubClauseDesc : " + \
#                                             j['SubClauseDesc']+nl
#                                 else:
#                                     str = str+nl+"ClauseDesc: " + \
#                                         l['ClauseDesc']
#             return str
#     return 'Not found'

@app.route('/data', methods=['GET', 'POST'])
def data():
    str = ""
    summary = ""
    nl = "<html > <body > <br > </body > </html >"
    if request.method == 'POST':
        # form = SearchForm()
        obj = request.form['keyword']
        # obj = form.keyword.data
        with open("C:\\Users\\Bhoomika\\KANUN_Inheritance\\COI.json", encoding='utf-8') as JsonFile:
            data = json.load(JsonFile)
            jsonData = data["laws"]
            for i in range(35):
                if obj in jsonData[i]['Name']:
                    if "ArtDesc" in jsonData[i]:
                        if text_summary(jsonData[i]['ArtDesc']) != "":
                            str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                jsonData[i]['ArtNo']+nl + \
                                "<html><body><b>ArtDesc : </b></body></html>" + \
                                text_summary(jsonData[i]['ArtDesc'])
                        else:
                            str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                jsonData[i]['ArtNo']+nl + \
                                "<html><body><b>ArtDesc : </b></body></html>" + \
                                (jsonData[i]['ArtDesc'])
                    else:
                        str = str+nl+nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                            jsonData[i]['ArtNo']
                        str1 = ""
                        if "Clauses" in jsonData[i]:
                            clause = jsonData[i]["Clauses"]
                            for l in clause:
                                # str = str+nl+nl+"ClauseNo: "+l['ClauseNo']
                                if "SubClauses" in l:
                                    SubClauses = l['SubClauses']
                                    for j in SubClauses:
                                        str1 = str1 + j['SubClauseDesc']
                                else:
                                    str1 = str1+l['ClauseDesc']
                        # str1 = text_summary(str1)
                        if text_summary(str1) != "":
                            str = str+nl+"<html><body><b>ArtDesc : </b></body></html>" + \
                                text_summary(str1)+nl
                        else:
                            str = str+nl + \
                                "<html><body><b>ArtDesc : </b></body></html>" + \
                                (str1)+nl
            # str1 = "<html><body><i>"+str+"</i></body></html>"
            str = nl+"""<html><body style = "background-image: url('/static/law1.jpg');background-repeat:no-repeat;background-size:cover;"><h1 style=" width: 100%;margin-top:-25px;margin-left:-7px;margin-bottom: 10px;border-radius:32px;background:black;padding: 10px;border-radius: 4px;color:white;">Summary Of Relevant Laws</h1><p style="color:white;background-color:black;opacity:0.5;"><b>""" + \
                str + \
                """</b > </p > <a href = more"""+obj + \
                """ > """+nl+"""More </a></body > </html >"""
            return (str)
    return 'Not found'


@app.route('/property', methods=['GET', 'POST'])
def property():
    str = ""
    summary = ""
    nl = "<html > <body > <br > </body > </html >"
    if request.method == 'POST':
        # form = SearchForm()
        obj = request.form['keyword']
        # obj = form.keyword.data
        with open("C:\\Users\\Bhoomika\\KANUN_Inheritance\\COI.json", encoding='utf-8') as JsonFile:
            data = json.load(JsonFile)
            jsonData = data["laws"]
            for i in range(35):
                if jsonData[i]['Category'] == 'Property Law':
                    if obj in jsonData[i]['Name']:
                        if "ArtDesc" in jsonData[i]:
                            if text_summary(jsonData[i]['ArtDesc']) != "":
                                str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                    jsonData[i]['ArtNo']+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    text_summary(jsonData[i]['ArtDesc'])
                            else:
                                str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                    jsonData[i]['ArtNo']+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    (jsonData[i]['ArtDesc'])
                        else:
                            str = str+nl+nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                jsonData[i]['ArtNo']
                            str1 = ""
                            if "Clauses" in jsonData[i]:
                                clause = jsonData[i]["Clauses"]
                                for l in clause:
                                    # str = str+nl+nl+"ClauseNo: "+l['ClauseNo']
                                    if "SubClauses" in l:
                                        SubClauses = l['SubClauses']
                                        for j in SubClauses:
                                            str1 = str1 + j['SubClauseDesc']
                                    else:
                                        str1 = str1+l['ClauseDesc']
                            # str1 = text_summary(str1)
                            if text_summary(str1) != "":
                                str = str+nl+"<html><body><b>ArtDesc : </b></body></html>" + \
                                    text_summary(str1)+nl
                            else:
                                str = str+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    (str1)+nl
                        str = nl+"""<html><body style = "background-image: url('/static/law1.jpg');background-repeat:no-repeat;background-size:cover;"><h1 style=" width: 100%;margin-top:-25px;margin-left:-7px;margin-bottom: 10px;border-radius:32px;background:black;padding: 10px;border-radius: 4px;color:white;">Summary Of Relevant Laws</h1><p style="color:white;background-color:black;opacity:0.5;"><b>""" + \
                            str + \
                            """</b > </p > <a href = more"""+obj + \
                            """ > """+nl+"""More </a></body > </html >"""
                        return (str)
        return 'Not found'


@app.route('/citizenship', methods=['GET', 'POST'])
def citizenship():
    str = ""
    summary = ""
    nl = "<html > <body > <br > </body > </html >"
    if request.method == 'POST':
        # form = SearchForm()
        obj = request.form['keyword']
        # obj = form.keyword.data
        with open("C:\\Users\\Bhoomika\\KANUN_Inheritance\\COI.json", encoding='utf-8') as JsonFile:
            data = json.load(JsonFile)
            jsonData = data["laws"]
            for i in range(35):
                if jsonData[i]['Category'] == 'Citizenship Law':
                    if obj in jsonData[i]['Name']:
                        if "ArtDesc" in jsonData[i]:
                            if text_summary(jsonData[i]['ArtDesc']) != "":
                                str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                    jsonData[i]['ArtNo']+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    text_summary(jsonData[i]['ArtDesc'])
                            else:
                                str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                    jsonData[i]['ArtNo']+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    (jsonData[i]['ArtDesc'])
                        else:
                            str = str+nl+nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                jsonData[i]['ArtNo']
                            str1 = ""
                            if "Clauses" in jsonData[i]:
                                clause = jsonData[i]["Clauses"]
                                for l in clause:
                                    # str = str+nl+nl+"ClauseNo: "+l['ClauseNo']
                                    if "SubClauses" in l:
                                        SubClauses = l['SubClauses']
                                        for j in SubClauses:
                                            str1 = str1 + j['SubClauseDesc']
                                    else:
                                        str1 = str1+l['ClauseDesc']
                            # str1 = text_summary(str1)
                            if text_summary(str1) != "":
                                str = str+nl+"<html><body><b>ArtDesc : </b></body></html>" + \
                                    text_summary(str1)+nl
                            else:
                                str = str+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    (str1)+nl
                    str = nl+"""<html><body style = "background-image: url('/static/law1.jpg');background-repeat:no-repeat;background-size:cover;"><h1 style=" width: 100%;margin-top:-25px;margin-left:-7px;margin-bottom: 10px;border-radius:32px;background:black;padding: 10px;border-radius: 4px;color:white;">Summary Of Relevant Laws</h1><p style="color:white;background-color:black;opacity:0.5;"><b>""" + \
                        str + \
                        """</b > </p > <a href = more"""+obj + \
                        """ > """+nl+"""More </a></body > </html >"""
                    return (str)
        return 'Not found'


@app.route('/criminal', methods=['GET', 'POST'])
def criminal():
    str = ""
    summary = ""
    nl = "<html > <body > <br > </body > </html >"
    if request.method == 'POST':
        # form = SearchForm()
        obj = request.form['keyword']
        # obj = form.keyword.data
        with open("C:\\Users\\Bhoomika\\KANUN_Inheritance\\COI.json", encoding='utf-8') as JsonFile:
            data = json.load(JsonFile)
            jsonData = data["laws"]
            for i in range(35):
                if jsonData[i]['Category'] == 'Criminal Law':
                    if obj in jsonData[i]['Name']:
                        if "ArtDesc" in jsonData[i]:
                            if text_summary(jsonData[i]['ArtDesc']) != "":
                                str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                    jsonData[i]['ArtNo']+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    text_summary(jsonData[i]['ArtDesc'])
                            else:
                                str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                    jsonData[i]['ArtNo']+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    (jsonData[i]['ArtDesc'])
                        else:
                            str = str+nl+nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                jsonData[i]['ArtNo']
                            str1 = ""
                            if "Clauses" in jsonData[i]:
                                clause = jsonData[i]["Clauses"]
                                for l in clause:
                                    # str = str+nl+nl+"ClauseNo: "+l['ClauseNo']
                                    if "SubClauses" in l:
                                        SubClauses = l['SubClauses']
                                        for j in SubClauses:
                                            str1 = str1 + j['SubClauseDesc']
                                    else:
                                        str1 = str1+l['ClauseDesc']
                            # str1 = text_summary(str1)
                            if text_summary(str1) != "":
                                str = str+nl+"<html><body><b>ArtDesc : </b></body></html>" + \
                                    text_summary(str1)+nl
                            else:
                                str = str+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    (str1)+nl
                    str = nl+"""<html><body style = "background-image: url('/static/law1.jpg');background-repeat:no-repeat;background-size:cover;"><h1 style=" width: 100%;margin-top:-25px;margin-left:-7px;margin-bottom: 10px;border-radius:32px;background:black;padding: 10px;border-radius: 4px;color:white;">Summary Of Relevant Laws</h1><p style="color:white;background-color:black;opacity:0.5;"><b>""" + \
                        str + \
                        """</b > </p > <a href = more"""+obj + \
                        """ > """+nl+"""More </a></body > </html >"""
                    return (str)
        return 'Not found'


@app.route('/civil', methods=['GET', 'POST'])
def civil():
    str = ""
    str2 = ""
    summary = ""
    nl = "<html > <body > <br > </body > </html >"
    if request.method == 'POST':
        # form = SearchForm()
        obj = request.form['keyword']
        # obj = form.keyword.data
        with open("C:\\Users\\Bhoomika\\KANUN_Inheritance\\COI.json", encoding='utf-8') as JsonFile:
            data = json.load(JsonFile)
            jsonData = data["laws"]
            for i in range(35):
                if jsonData[i]['Category'] == 'Civil Law':
                    if obj in jsonData[i]['Name']:
                        if "ArtDesc" in jsonData[i]:
                            if text_summary(jsonData[i]['ArtDesc']) != "":
                                str = str + nl + nl+nl+"<html><body><b>ArtNo :</b><br></body></html>" + \
                                    jsonData[i]['ArtNo']+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    text_summary(jsonData[i]['ArtDesc'])
                            else:
                                str = str + nl + nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                    jsonData[i]['ArtNo']+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    (jsonData[i]['ArtDesc'])
                        else:
                            str = str+nl+nl+nl+"<html><body><b>ArtNo : </b></body></html>" + \
                                jsonData[i]['ArtNo']
                            str1 = ""
                            if "Clauses" in jsonData[i]:
                                clause = jsonData[i]["Clauses"]
                                for l in clause:
                                    # str = str+nl+nl+"ClauseNo: "+l['ClauseNo']
                                    if "SubClauses" in l:
                                        SubClauses = l['SubClauses']
                                        for j in SubClauses:
                                            str1 = str1 + j['SubClauseDesc']
                                    else:
                                        str1 = str1+l['ClauseDesc']
                            # str1 = text_summary(str1)
                            if text_summary(str1) != "":
                                str = str+nl+"<html><body><b>ArtDesc : </b></body></html>" + \
                                    text_summary(str1)+nl
                            else:
                                str = str+nl + \
                                    "<html><body><b>ArtDesc : </b></body></html>" + \
                                    (str1)+nl
                    str = nl+"""<html><body style = "background-image: url('/static/law1.jpg');background-repeat:no-repeat;background-size:cover;"><h1 style=" width: 100%;margin-top:-25px;margin-left:-7px;margin-bottom: 10px;border-radius:32px;background:black;padding: 10px;border-radius: 4px;color:white;">Summary Of Relevant Laws</h1><p style="color:white;background-color:black;opacity:0.5;"><b>""" + \
                        str + \
                        """</b > </p > <a href = more"""+obj + \
                        """ > """+nl+"""More </a></body > </html >"""
                    return (str)
        return 'Not found'


@app.route('/more<obj>')
def more(obj):
    # nl = "<html > <body > <br > </body > </html >"
    lis = []
    with open("C:\\Users\\Bhoomika\\KANUN_Inheritance\\COI.json", encoding='utf-8') as JsonFile:
        data = json.load(JsonFile)
        jsonData = data["laws"]
        for i in range(35):
            if obj in jsonData[i]['Name']:
                lis.append(jsonData[i])
        # str = """<html><body style = "background-image: url('/static/law1.jpg');background-repeat:no-repeat;background-size:cover;"><h1 style=" width: 100%;margin-top:-25px;margin-left:-7px;margin-bottom: 10px;border-radius:32px;background:black;padding: 10px;border-radius: 4px;color:white;">Summary Of Relevant Laws</h1><p style="color:white;background-color:black;opacity:0.5;"><b>""" + \
        #     str + \
        #     """</b > </p ></body></html>"""

        return render_template('ArtDesc.html', ArtDesc=lis)


# @app.route('/search', methods=['POST', 'GET'])
# def search():
#     form = SearchForm()
    # if form.validate_on_submit():
    # keyword = form.keyword.data
    # return render_template('ArtDesc.html', ArtDesc=keyword)
    # return '0'
    # with open("C:\\Users\\Bhoomika\\KANUN_Inheritance\\COI.json", encoding='utf-8') as JsonFile:
    #     data = json.load(JsonFile)
    #     jsonData = data["laws"]
    #     for i in range(35):
    #         if obj in jsonData[i]['Name']:
    #             return render_template('ArtDesc.html', ArtDesc=jsonData[i]['ArtDesc'])
    #     return jsonData[i]
    # header = x.keys()
    # values = x.values()
    # print(header, values)

    # Database models

@app.route('/review', methods=['GET', 'POST'])
def review():
    form1 = ReviewForm()
    if form1.validate_on_submit():
        username = form1.username.data
        user = Review.query.filter_by(username=username).first()
        if not user:
            new_review = Review(username=form1.username.data,
                                Review=form1.Review.data, Rating=form1.Rating.data)
            db.session.add(new_review)
            db.session.commit()
            global ID
            obj = Review.query.all()
            last_obj = obj[-1]
            ID = last_obj.id
            user1 = Review.query.filter_by(id=ID-5).first()
            user2 = Review.query.filter_by(id=ID-4).first()
            user3 = Review.query.filter_by(id=ID-3).first()
            user4 = Review.query.filter_by(id=ID-2).first()
            user5 = Review.query.filter_by(id=ID-1).first()
            user6 = Review.query.filter_by(id=ID).first()
            return render_template('main.html', user1=user1, user2=user2, user3=user3, user4=user4, user5=user5, user6=user6)
        else:
            return render_template('Review.html')
    return render_template('review_form.html', form=form1)


@app.route('/view')
def view():
    # Reviews = Review.objects.all()
    name = 'Peter'
    table = Review.query.filter_by(id=2).first()
    return render_template('Review.html', user=table)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    # last_name = Column(String)
    # email = Column(String)
    password = Column(String)


class Law_table(db.Model):
    __tablename__ = 'Laws'
    id = Column(Integer, primary_key=True)
    ArtNo = Column(String)
    Name = Column(String)
    SubHeading = Column(String)
    Status = Column(String)
    Explanations = Column(JSON)
    ArtDesc = Column(String)
    Clauses = Column(JSON)


class Review(db.Model):
    __tablename__ = "Reviews"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    Review = Column(String)
    Rating = Column(Integer)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_name = User.query.filter_by(
            username=username.data).first()
        if existing_user_name:
            raise ValidationError(
                "That username already exists. Please choose a different one"
            )


class SearchForm(FlaskForm):
    keyword = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "keyword"})
    submit = SubmitField("submit")


class ReviewForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=5, max=200)], render_kw={"placeholder": "Username"})
    Review = StringField(validators=[InputRequired(), Length(
        min=5, max=200)], render_kw={"placeholder": "Enter Review Here"})
    Rating = FloatField(validators=[InputRequired()], render_kw={
                        "placeholder": "Rating"})
    Submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


if __name__ == '__main__':
    app.run(debug=True)
