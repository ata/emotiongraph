#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from facebook.webappfb import *
from models import *
from analysis import *
from google.appengine.api import memcache
from datetime import datetime
from google.appengine.api import urlfetch

import base

def get_menu(current):
    tabs = {'home':'Home','friend':'Friend Graph','invite':'Invite Friend'}
    menu = '<fb:tabs>'
    
    for k,v in tabs.items():
        selected = 'false'
        if current == k:
            selected = 'true'
            
        menu += '<fb:tab-item href="http://apps.facebook.com/emograph/canvas/%s.php" '\
                'title="%s" selected="%s"/>' % (k,v,selected)
                
    menu += '</fb:tabs>'
    
    return menu

class IndexHandler(base.BaseRequestHandler):
    def get(self):
        self.render('index.html',{})


class IndexFacebookHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    
    def get(self):
        self.redirect('/graph/index.php')
        
    def canvas(self):
        self.redirect('http://apps.facebook.com/emograph/canvas/home.php')


class IndexCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        uid = self.facebook.uid
        self.render('canvas/index.html',{'uid':uid,'menu':get_menu('home')})


class YouCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        
        uid = self.facebook.uid
        states = get_states_with_emotion(self.facebook.status.get(uid,20))
        chart = get_chart(states)
        self.render('canvas/graph.html',{'uid':uid,
                                        'chart':chart,
                                        'menu':get_menu('home'),
                                        'states':states})
                                            

class FriendCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        self.render('canvas/friend.html',{'menu':get_menu('friend'),
                                        'uid':self.facebook.uid})
        

class FriendGraphCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        
        uid = int(self.request.get('friend_sel'))
        
        states = get_states_with_emotion(self.facebook.status.get(uid,20))
        chart = get_chart(states)
        self.render('canvas/graph.html',{'uid':uid,
                                        'chart':chart,
                                        'menu':get_menu('friend'),
                                        'states':states})

class InviteCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        self.render('canvas/invite.html',{'uid':self.facebook.uid,
                                            'menu':get_menu('invite')})

class InviteSuccessCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        self.redirect('http://apps.facebook.com/emograph/canvas/invite.php')
        states = get_states_with_emotion(self.facebook.status.get(uid,20))
        chart = get_chart(states)
        self.render('canvas/you.html',{'uid':uid,
                                        'chart':chart,
                                        'menu':get_menu('home'),
                                        'states':states})




def main():
    application = webapp.WSGIApplication([
        (r'/', IndexFacebookHandler),
        (r'/canvas/home.php',IndexCanvasHandler),
        (r'/canvas/you.php',YouCanvasHandler),
        (r'/canvas/friend.php',FriendCanvasHandler),
        (r'/canvas/friend-graph.php',FriendGraphCanvasHandler),
        (r'/canvas/invite.php',InviteCanvasHandler),
        (r'/canvas/invite-success.php',InviteSuccessCanvasHandler),
        (r'/index.php',IndexHandler)
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
