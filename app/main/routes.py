# import all the needed packages
import os
from flask import Flask, render_template,request,url_for,current_app,redirect
import requests as re
import json
from io import TextIOWrapper
import csv
from . import main
from app.model import User, Task
from app import db
from flask_login import login_required,current_user,login_user,logout_user
from app.extract import json_extract


@main.route('/', methods=['GET', 'POST'])
@main.route('/index',methods=['GET','POST'])
def index():
    #form = TrackForm()
    return render_template('track.html')#,form=form)


@main.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.upload'))
    
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(request.form['passwd']):
            login_user(user)
            return redirect(url_for('main.upload'))
    return render_template("login.html")


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/results', methods=['GET','POST'])
def results():
    
    headers = { 
        'AccessLicenseNumber' : os.environ.get('AccessLicenseNumber'),
        'Username' : os.environ.get('Username'),
        'Password' : os.environ.get('Password')} 

    if request.method=='POST':   
        num = request.form['name']
        #url = "https://onlinetools.ups.com/track/v1/details/{}".format(num)
        # for testing use this link below
        url = "https://wwwcie.ups.com/track/v1/details/{}".format(num)
        r = re.get(url,headers=headers)
        data = json.loads(r.text)
        if 'trackResponse' not in data:
            return " Your maximum try per hour has exceeded, Try again an hour later!!!"
    #with open('res.json') as f:
    #    data = json.load(f)

        track_no = json_extract(data,'trackingNumber')
        city = json_extract(data,'city')
        country = json_extract(data,'country')
        desc = json_extract(data,'description')
        dates= json_extract(data,'date')
        times = json_extract(data,'time') 
        dates = dates[0]
        times = times[0]
        dates = dates[:4] + "-"+ dates[-4:-2]+"-"+dates[-2:]
        times = times[:2]+":"+ times[-4:-2]+":"+times[-2:]
    return render_template('results.html',track_no=track_no,city=city,country=country,desc=desc,date=dates,time=times)



@main.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'POST':
        csv_file = request.files['file']
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            tasks = Task(track_no=row[0], city=row[1],country=row[2],description=row[3],dates=row[4],times=row[5],received_by=row[6])
            db.session.add(tasks)
            db.session.commit()
        return redirect(url_for('main.upload'))
    else:
         tasks = Task.query.order_by(Task.upload_date)
    # add a load here
    return render_template('upload.html',tasks=tasks) 