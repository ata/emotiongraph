from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


import facebook
import config
import os
import yaml


class FacebookConnect(object):
    
    def __init__(self,func):
        self.func = func
        
    def __call__(self, *args, **kwargs):
        config = yaml.load(file('facebook.yaml', 'r'))
        self.api_key = config['api_key']
        self.secret_key = config['secret_key']
        self.facebook = facebook.Facebook(self.api_key, self.secret_key)
        
        if not self.facebook.check_session(self.request):
            self.render('fbconnect.html',{'uri':self.request.uri, 
                                        'api_key': self.api_key})
            return
        try:
            self.user = self.facebook.users.getInfo(
                        [self.facebook.uid],
                        ['uid', 'name', 'birthday', 'relationship_status'])[0]
                
        except facebook.FacebookError:
          self.render('fbconnect.html',{'uri':self.request.uri, 
                                        'api_key': self.api_key})
          return
          
        self.func(self, *args, **kwargs)


class BaseRequestHandler(webapp.RequestHandler):
    
    def get_template(self,template_name):
        return os.path.join(
                os.path.dirname(__file__),
                config.TEMPLATE_DIR,
                template_name)
                
    def render(self,template_name,template_vars={}):
        template_path = self.get_template(template_name)
        self.response.out.write(template.render(template_path, template_vars))

class FacebookConnectHandler(BaseRequestHandler):
    
    def initialize(self, request, response):
        super(FacebookConnectHandler, self).initialize(request, response)
        config = yaml.load(file('facebook.yaml', 'r'))
        self.api_key = config['api_key']
        self.secret_key = config['secret_key']
        self.facebook = facebook.Facebook(self.api_key, self.secret_key)
        
       
          
    def get(self):
        if not self.facebook.check_session(self.request):
            self.render('fbconnect.html',{'uri':self.request.uri, 
                                        'api_key': self.api_key})
            return
        try:
            self.fbuser = self.facebook.users.getInfo(
                        [self.facebook.uid],
                        ['uid', 'name', 'birthday', 'relationship_status'])[0]
                
        except facebook.FacebookError:
          self.render('fbconnect.html',{'uri':self.request.uri, 
                                        'api_key': self.api_key})
          return
          
        self.connected()
        
