from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from django.utils import simplejson
from models import *
from analysis import *
from datetime import datetime
#from google.appengine.ext.webapp import template
#from google.appengine.ext.db import djangoforms

import base

class IndexHandler(base.FacebookConnectHandler):
    def connected(self):
        try:
            friends = get_fbfriends_cache(self.facebook,1000)
            
            self.render('trainning/index.html',{'friends':friends,
                                                'static': get_trainning_static(),
                                                'user':self.user,
                                                'uid':self.user.uid,
                                                'chart_all':get_trainning_chart_all(),
                                                'chart':get_trainning_chart()})
        
        except urlfetch.DownloadError:
            self.render('error/download.html',{'uri': self.request.uri})
            
class StatusHandler(base.FacebookConnectHandler):
    
    def connected(self,uid):
        try:
            uid = int(uid)
            
            selected = ""
            
            if self.user.uid == uid:
                selected = 'selected="selected"'
            
            friends = get_fbfriends_cache(self.facebook,1000)
            query = Status.all()
            query.filter('category = ', None)
            query.filter('uid = ', uid)
            if query.count() == 0:
                states = self.facebook.status.get(uid)
                for s in states:
                    Status( status_id = s['status_id'],
                            message = s['message'],
                            time = datetime.fromtimestamp(s['time']),
                            uid = s['uid'],
                            ).save()
            states = query.fetch(10)
            self.render('trainning/status.html',{'states':states,
                                                'uid':uid,
                                                'user':self.user,
                                                'selected':selected,
                                                'static': get_trainning_static(),
                                                'friends':friends})
        except urlfetch.DownloadError:
            self.render('error/download.html',{'uri': self.request.uri})
        
    def post(self,id):
        #status = Status.get(self.request.get('key'))
        keys = self.request.get_all('key')
        categories = self.request.get_all('category')
        
        for i in range(len(keys)):
            status = Status.get(keys[i])
            status.category = categories[i]
            status.put()
            if categories[i] != 'uncategory':
                Keyword.update(status)
                Keyword.update_custome(status)
        self.redirect(self.request.uri)
            

class FriendHandler(base.BaseRequestHandler):
    def post(self):
        uid = self.request.get('uid')
        self.redirect('/trainning/status/%s.php' % uid)

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
        
        offset = int(count) * (int(page) -1)
        keywords = query.fetch(int(count), offset)
        
        current = "%d - %d" % (offset + 1, len(keywords) +offset)
        
        if(len(keywords)) < int(count):
            last = True 
        
        self.render('trainning/keyword.html',{'keywords':keywords,'show':show,
                                                'order':order,'count':int(count),
                                                'page':int(page),'current':current,
                                                'next_page':int(page) + 1,
                                                'last':last,
                                                'first':first,
                                                'prev_page':int(page) - 1,
                                                'uri':self.request.uri})

class SwitchKeyword(base.BaseRequestHandler):
    
    def get(self, id = None):
        keyword = Keyword.get_by_id(int(id))
        
        if keyword.valid:
            keyword.valid = False
        else:
            keyword.valid = True
        keyword.put()
        
        self.redirect(self.request.get('uri'))
    
    def post(self, id = None):
        ids = self.request.get_all('id')
        for id in ids:
            keyword = Keyword.get_by_id(int(id))
            if keyword.valid:
                keyword.valid = False
            else:
                keyword.valid = True
            keyword.put()
        
        self.redirect(self.request.get('uri'))

class SmileyHandler(base.BaseRequestHandler):
    
    def get(self):
        smiles = Keyword.all().filter('custome = ',True).fetch(1000)
        self.render('trainning/smiley.html',{'smiles':smiles})
        
    def post(self):
        smiles = self.request.get_all('smiley')
        for smiley in smiles:
            if len(smiley.strip()) != 0:
                Keyword(word = smiley).save_custome()
                
        self.redirect('/trainning/smiley.php')
        
class SmileyDeleteHandler(base.BaseRequestHandler):
    def get(self,id):
        Keyword.get_by_id(int(id)).delete()
        self.redirect('/trainning/smiley.php')
        

def main():
    application = webapp.WSGIApplication([
        (r'/trainning/index.php',IndexHandler),
        (r'/trainning/keyword/show-(?P<show>\w+)/order-(?P<order>\S+)/count-(?P<count>\d+)/page-(?P<page>\d+).php',KeywordHandler),
        (r'/trainning/keyword/show-(?P<show>\w+)/order-(?P<order>\S+)/count-(?P<count>\d+).php',KeywordHandler),
        (r'/trainning/keyword/show-(?P<show>\w+)/order-(?P<order>\S+).php',KeywordHandler),
        (r'/trainning/keyword/show-(?P<show>\w+).php',KeywordHandler),
        (r'/trainning/keyword.php',KeywordHandler),
        (r'/trainning/keyword-switch/(?P<id>\d+).php',SwitchKeyword),
        (r'/trainning/keyword-switch.php',SwitchKeyword),
        (r'/trainning/smiley.php',SmileyHandler),
        (r'/trainning/smiley/delete/(?P<id>\d+).php',SmileyDeleteHandler),
        (r'/trainning/status/(?P<id>\d+).php',StatusHandler),
        (r'/trainning/friend.php',FriendHandler)
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
