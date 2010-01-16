from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import *

import facebook
import config
import os
import yaml

class BaseRequestHandler(webapp.RequestHandler):
    
    def get_template(self,template_name):
        return os.path.join(
                os.path.dirname(__file__),
                config.TEMPLATE_DIR,
                template_name)
                
    def render(self,template_name,template_vars={}):
        user = users.get_current_user()
        if user == None:
            template_vars.update({'login_url': users.create_login_url(self.request.uri),
                                    'login_label':'login'})
        else:
            template_vars.update({'login_url': users.create_logout_url(self.request.uri),
                                    'login_label':'logout',
                                    'nickname':user.nickname()})
        
        template_path = self.get_template(template_name)
        self.response.out.write(template.render(template_path, template_vars))

class FacebookConnectHandler(BaseRequestHandler):
    
    def initialize(self, request, response):
        
        super(FacebookConnectHandler, self).initialize(request, response)
        config = yaml.load(file('facebook.yaml', 'r'))
        self.api_key = config['api_key']
        self.secret_key = config['secret_key']
        self.facebook = facebook.Facebook(self.api_key, self.secret_key)
        if User.all().filter('login = ', users.get_current_user()).get() == None:
            User().put()
        self.user = User.all().filter('login = ', users.get_current_user()).get()
        
    def connected(self, *args, **kwargs):
        raise NotImplementedError()
          
    def get(self,*args, **kwargs):
        if not self.facebook.check_session(self.request):
            self.render('fbconnect.html',{'uri':self.request.uri, 
                                        'api_key': self.api_key})
            return
        try:            
            if self.user.uid is None:
                
                fbuser = self.facebook.users.getInfo(
                                [self.facebook.uid],
                                ['uid','name','pic','pic_square'])[0]
                
                self.user.uid = fbuser['uid']
                self.user.name = fbuser['name']
                self.user.pic = fbuser['pic']
                self.user.pic_square = fbuser['pic_square']
                self.user.put()
                
        except facebook.FacebookError:
            self.render('fbconnect.html',{'uri':self.request.uri, 
                                        'api_key': self.api_key})
            return
            
        self.connected(*args, **kwargs)
        
