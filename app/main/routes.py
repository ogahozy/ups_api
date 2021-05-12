# import all the needed packages
import os
from flask import Flask, render_template,request,url_for,current_app
import requests as re
import json
from . import main
from app.main.forms import TrackForm
from app.extract import json_extract


@main.route('/', methods=['GET', 'POST'])
@main.route('/index',methods=['GET','POST'])
def index():
    form = TrackForm()
    return render_template('track.html',form=form)


@main.route('/results', methods=['GET','POST'])
def results():

    headers={
    'AccessLicenseNumber': os.environ.get('AccessLicenseNumber'),
    'Username' : os.environ.get('Username'),
    'Password':  os.environ.get('Password'),
    }

    if request.method=='POST':   
        num = request.form['num']
        url = "https://onlinetools.ups.com/track/v1/details/{}".format(num)
        #url = "https://wwwcie.ups.com/track/v1/details/{}".format(num)
        r = re.get(url,headers=headers)
        data = json.loads(r.text)
        if 'trackResponse' not in data:
            return " Your maximum try per hour has exceeded, Try again an hour later!!!"
    #with open('res.json') as f:
    #   data = json.load(f)

        track_no = json_extract(data,'trackingNumber')
        city = json_extract(data,'city')
        country = json_extract(data,'country')
        desc = json_extract(data,'description')
        date= json_extract(data,'date')
        time = json_extract(data,'time') 
        date = date[0]
        time = time[0]
        date =date[:4] + "-"+ date[-4:-2]+"-"+date[-2:]
        time =time[:2]+":"+ time[-4:-2]+":"+time[-2:]
    return render_template('results.html',track_no=track_no,city=city,country=country,desc=desc,date=date,time=time)
