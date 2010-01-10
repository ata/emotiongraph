from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util

import base

class MainTranningHandler(base.FacebookConnectHandler):
    def connected(self):
        friends = self.facebook.friends.get()
        self.render('trainning.html',{'friends':friends})

def main():
    application = webapp.WSGIApplication([
        ('/trainning.php',MainTranningHandler),
        ],debug=True)
        
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
