from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from base import BaseRequestHandler
from django.utils import simplejson

class Article(db.Model):
    title = db.StringProperty()
    content = db.StringProperty(multiline=True)
    
class ArticleListHandler(BaseRequestHandler):
    def get(self,key):
        if key != None:
            db.delete(key)
        
        self.render('latihan.html',{'articles':Article.all()})
        
    def post(self,key):
        Article(title=self.request.get('title'),
                content=self.request.get('content')).put()
        self.get(key)

def main():
    application = webapp.WSGIApplication([
        ('/latihan/?(?P<key>\w+)?\.php',ArticleListHandler),
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
        
