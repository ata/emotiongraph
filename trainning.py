from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from django.utils import simplejson
from models import *
from datetime import datetime
#from google.appengine.ext.webapp import template
#from google.appengine.ext.db import djangoforms

import base

class IndexHandler(base.FacebookConnectHandler):
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

class KeywordHandler(base.BaseRequestHandler):
    
    def get(self, show = 'valid', order = 'word', count = '50' ,page = '1'):
        query = Keyword.all()
        first = False
        last = False
        if int(page) == 1:
            first = True
        if(show == 'valid'):
            query.filter('valid = ',True)
        else:
            query.filter('valid = ',False)
            
        query.order(order)
        offset = int(count) * int(page)
        current = "%d - %d" % (offset + 1, offset + int(count))
        if query.count() < int(count):
            last = True
        keywords = query.fetch(int(count), offset)
        self.render('trainning/keyword.html',{'keywords':keywords,'show':show,
                                                'order':order,'count':int(count),
                                                'page':int(page),'current':current,
                                                'next_page':int(page) + 1,
                                                'prev_page':int(page) - 1,
                                                'uri':self.request.uri})

class SwitchKeyword(base.BaseRequestHandler):
    
    def get(self, valid, key):
        keyword = Keyword.get(key)
        uri = self.request.get('uri')
        
        if valid == 'invalid':
            keyword.valid = False
        else:
            keyword.valid = True
        keyword.put()
        
        self.redirect(uri)
        

def main():
    application = webapp.WSGIApplication([
        (r'/trainning/index.php',IndexHandler),
        (r'/trainning/keyword/(?P<show>\w+)/(?P<order>\S+)/(?P<count>\d+)/(?P<page>\d+).php',KeywordHandler),
        (r'/trainning/keyword/(?P<show>\w+)/(?P<order>\S+)/(?P<count>\d+).php',KeywordHandler),
        (r'/trainning/keyword/(?P<show>\w+)/(?P<order>\S+).php',KeywordHandler),
        (r'/trainning/keyword/(?P<show>\w+).php',KeywordHandler),
        (r'/trainning/keyword.php',KeywordHandler),
        (r'/trainning/keyword/switch/(?P<valid>\w+)/(?P<key>\w+).php',SwitchKeyword),
        (r'/trainning/(?P<uid>\d+).php',StatusHandler),
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
