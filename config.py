import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    #x_merchant_id = os.environ.get('x-merchant-id')