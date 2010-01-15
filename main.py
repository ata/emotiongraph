#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from facebook.webappfb import *
from models import *
from analysis import *
from google.appengine.api import memcache
from datetime import datetime

import base


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
        self.redirect('http://apps.facebook.com/emograph/canvas/index.php')


class IndexCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        uid = self.facebook.uid
        self.render('canvas/index.html',{'uid':uid})


class YouCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        uid = self.facebook.uid
        states = get_states_with_emotion(self.facebook.status.get(uid,20))
        chart = get_chart(states)
        self.render('canvas/you.html',{'uid':uid,'chart':chart,'states':states})
    

class FriendCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        self.render('canvas/friend.html',)

class InviteCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        self.render('canvas/invite.html',{'uid':self.facebook.uid})

class InviteSuccessCanvasHandler(FacebookCanvasHandler,base.BaseRequestHandler):
    requires_login = True
    require_app = True
    need_session = True
    check_session = True
    def canvas(self):
        self.redirect('http://apps.facebook.com/emograph/canvas/invite.php')



class CronProbsHandler(base.BaseRequestHandler):
    def get(self):
        
        last_emotion_index = memcache.get('last_cron_emotion_index')
        
        if last_emotion_index is None:
            memcache.set('last_cron_emotion_index', 0, 3600 * 24)
            last_emotion_index = 0
        
        emotion = ['senang','sedih','marah','malu',
                 'jijik','takut','bersalah']
        
        if Keyword.generate_probs_cache(emotion[last_emotion_index]):
            self.response.out.write("Ok => %s" % (emotion[last_emotion_index]))
            last_emotion_index += 1
            if last_emotion_index == 7:
                last_emotion_index = 0
            memcache.set('last_cron_emotion_index', last_emotion_index, 3600 * 24)
        #for e in emotion:
            


class CronWordsHandler(base.BaseRequestHandler):
    def get(self):
        Keyword.generate_list_cache()
        self.response.out.write("Ok")


def main():
    application = webapp.WSGIApplication([
        (r'/', IndexFacebookHandler),
        (r'/canvas/index.php',IndexCanvasHandler),
        (r'/canvas/you.php',YouCanvasHandler),
        (r'/canvas/friend.php',FriendCanvasHandler),
        (r'/canvas/invite.php',InviteCanvasHandler),
        (r'/canvas/invite-success.php',InviteSuccessCanvasHandler),
        (r'/index.php',IndexHandler),
        (r'/cron-probs.php',CronProbsHandler),
        (r'/cron-words.php',CronWordsHandler)
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
