from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from django.utils import simplejson
from models import *
from analysis import *
from datetime import datetime
#from google.appengine.ext.webapp import template
#from google.appengine.ext.db import djangoforms

import base

class IndexHandler(base.FacebookConnectHandler):
    def connected(self):
        if not Friend.get_trainnings(self.user):
            friends = self.facebook.friends.get()
            for uid in friends:
                Friend( user = self.user, 
                        uid = uid, 
                        trainning = True).save()
        
        self.render('trainning/index.html',{'friends':Friend.get_trainnings(self.user,30),
                                            'static': get_trainning_static(),
                                            'chart_all':get_trainning_chart_all(),
                                            'chart':get_trainning_chart()})


class StatusHandler(base.FacebookConnectHandler):
    
    def connected(self,id):
        uid = Friend.get_by_id(int(id)).uid
        #uid = user.uid
        
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
        query.filter('uid = ', uid)
        
        if query.count() > 0:
            states = query.fetch(10)
        
        else:
            friend = db.get_by_id(id)
            friend.trainning = False
            friend.put()
            
            self.redirect('/trainning/index.php')
            return
                                                
        self.render('trainning/status.html',{'states':states,
                                            'uid':uid,
                                            'static': get_trainning_static(),
                                            'friends':Friend.get_trainnings(self.user,30)})
        
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
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
