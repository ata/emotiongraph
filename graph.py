from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from models import *
from analysis import *

import base

class IndexHander(base.FacebookConnectHandler):
    
    def connected(self):
        if not Friend.get_trainnings(self.user):
            friends = self.facebook.friends.get()
            for uid in friends:
                Friend( user = self.user, 
                        uid = uid, 
                        trainning = True).save()
        
        friends = Friend.all().filter('user = ', self.user).fetch(20)
        self.render('graph/index.html',{'friends':friends})
    

class CheckEmotionHandler(base.FacebookConnectHandler):
    def connected(self,key):
        uid = db.get(key).uid
        friends = Friend.all().filter('user = ', self.user).fetch(20)
        states = get_states_with_emotion(self.facebook.status.get(uid,20))
        chart = get_chart(states)
        
        self.render('graph/emotion.html',{'states':states,
                                            'uid':uid,
                                            'friends':friends,
                                            'chart':chart})

def main():
    application = webapp.WSGIApplication([
        (r'/graph/index.php',IndexHander),
        (r'/graph/emotion/(?P<key>\w+).php',CheckEmotionHandler),
        ],debug=True)
        
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
