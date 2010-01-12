from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from django.utils import simplejson
from models import *
from datetime import datetime
#from google.appengine.ext.webapp import template
#from google.appengine.ext.db import djangoforms

import base

class MainTranningHandler(base.FacebookConnectHandler):
    def connected(self):
        self.render('trainning/index.html',{'friends':self.user.tranning_queue[0:20],
                                            'static': get_trainning_static(),
                                            'chart':get_trainning_chart()})


class StatusHandler(base.FacebookConnectHandler):
    
    def connected(self,uid):
        query = Status.all().filter('uid = ', uid)
        if query.count() == 0:
            
            states = self.facebook.status.get(uid)
            for s in states:
                Status( status_id = s['status_id'],
                        message = s['message'],
                        time = datetime.fromtimestamp(s['time']),
                        uid = s['uid'],
                        ).save()
        
        query = Status.all()
        query.filter('category = ', None)
        query.filter('uid = ', int(uid))
        if query.count() > 0:
            states = query.fetch(20)
        else:
            self.user.tranning_queue.remove(int(uid))
            self.user.put()
            self.redirect('/trainning/index.php')
            return
                                                
        self.render('trainning/status.html',{'states':states,
                                            'uid':uid,
                                            'static': get_trainning_static(),
                                            'friends':self.user.tranning_queue[0:20]})
        
    def post(self,uid):
        #status = Status.get(self.request.get('key'))
        keys = self.request.get_all('key')
        categories = self.request.get_all('category')
        
        for i in range(len(keys)):
            status = Status.get(keys[i])
            status.category = categories[i]
            status.put()
            if categories[i] != 'uncategory':
                Keyword.update(status)
        self.redirect(self.request.uri)
            

class AjaxStatusHandler(base.BaseRequestHandler):
    def get(self):
        pass

def main():
    application = webapp.WSGIApplication([
        ('/trainning/index.php',MainTranningHandler),
        ('/trainning/(?P<uid>\d+).php',StatusHandler),
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
