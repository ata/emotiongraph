from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from models import *
from analysis import *

import base

class IndexHander(base.FacebookConnectHandler):
    
    def connected(self):
        self.redirect('/graph/emotion/%d.php' % self.user.uid)

class CheckEmotionHandler(base.FacebookConnectHandler):
    def connected(self,uid = None):
        uid = int(uid)
        try:
            
            friends = get_fbfriends_cache(self.facebook,1000)
            states = get_fbstates_cache(self.facebook,uid)
            chart = get_chart(states)
                
            self.render('graph/emotion.html',{'states':states,
                                                'friends':friends,
                                                'user':self.user,
                                                'uid':uid,
                                                'chart':chart})
        except urlfetch.DownloadError:
            self.render('error/download.html',{'uri': self.request.uri})
    
    def post(self,uid = None):
        uid = self.request.get('uid')
        self.redirect('/graph/emotion/%s.php' % uid)

def main():
    application = webapp.WSGIApplication([
        (r'/graph/index.php',IndexHander),
        (r'/graph/emotion/(?P<uid>\d+).php',CheckEmotionHandler),
        (r'/graph/emotion.php',CheckEmotionHandler),
        ],debug=True)
        
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
