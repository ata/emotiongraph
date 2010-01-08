#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from facebook import webappfb
from models import *
from base import BaseRequestHandler
from datetime import datetime


class MainHandler(BaseRequestHandler):
    def get(self):
        #self.response.out.write('Hello')
        self.render('index.html',{})


class FacebookHandler(webappfb.FacebookCanvasHandler,BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    
    
    def get(self):
        
        self.redirect('index.php')
        #self.canvas()
    
    def canvas(self):
        
        #users = fb.User.all().fetch(10)
        #for user in users: 
        #    #print user.uid
        #    states = self.facebook.status.get(user.uid,10)
        #    for status in states:
        #        fb.Status(  user=user, 
        #                    status_id = status['status_id'],
        #                    message = status['message'],
        #                    time = datetime.fromtimestamp(status['time'])).save()
        status = self.facebook.status.get('700560419',10)
        self.response.out.write(status[0]['message'])
        
        #users = fb.User.fetch_empty_name()
        #for user in users:
        #    info = self.facebook.users.getInfo([user.uid],['name'])[0]
        #    user.name = info['name']
        #    user.put()
        #self.response.out.write('saved!')
        #self.render('index.fbml',{})


def main():
    application = webapp.WSGIApplication([
        ('/', FacebookHandler),
        ('/index\.php',MainHandler),
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
