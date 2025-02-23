# import all the needed packages
#import os
from flask import Flask, render_template,request,url_for,current_app
import requests as re
#import json
#import uuid
from app.ups_auth import get_ups_access_token 
from app.ups_tracking import track_ups_parcel
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
    if request.method=='POST':     
        tracking_number = request.form['num']
        data = track_ups_parcel(tracking_number)

        if 'error' in data:
            return f"Error: {data['error']}"

        track_no = json_extract(data,'trackingNumber')
        city = json_extract(data,'city')
        country = json_extract(data,'country')
        desc = json_extract(data,'description')
        received = json_extract(data,'receivedBy')
        date= json_extract(data,'date')
        time = json_extract(data,'time') 
        date = date[0]
        #date1 = data[1]
        time = time[0]
        date =date[:4] + "-"+ date[-4:-2]+"-"+date[-2:]
        date1 =date[:4] + "-"+ date[-4:-2]+"-"+date[-2:]
        time =time[:2]+":"+ time[-4:-2]+":"+time[-2:]
    return render_template('results.html',track_no=track_no,city=city,country=country,desc=desc,received=received,date=date,time=time)
    
