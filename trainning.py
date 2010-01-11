from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from django.utils import simplejson
from models import *

import base

class MainTranningHandler(base.FacebookConnectHandler):
    def connected(self):
        self.render('trainning.html',{'friends':self.user.tranning_queue[0:50]})

class StatusHandler(base.FacebookConnectHandler):
    def connected(self,uid):
        pass
    def post(self):
        """
        menyimpan status kedalam store engine, 
        melebelnya dengan:
        'marah','senang','jijik','takut','malu','bersalah','sedih'
        """
        

def main():
    application = webapp.WSGIApplication([
        ('/trainning/index.php',MainTranningHandler),
        ('/trainning/uid/(?P<uid>\d+).php',MainTranningHandler),
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
