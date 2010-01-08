from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


import config
import os

class BaseRequestHandler(webapp.RequestHandler):
    
    def get_template(self,template_name):
        return os.path.join(
                os.path.dirname(__file__),
                config.TEMPLATE_DIR,
                template_name)
                
    def render(self,template_name,template_vars={}):
        template_path = self.get_template(template_name)
        self.response.out.write(template.render(template_path, template_vars))
