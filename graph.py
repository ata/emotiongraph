from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from models import *
from analysis import *

import base

class IndexHander(base.BaseRequestHandler):
    def get(self):
        self.render('graph/index.html',{'static':get_trainning_static(),
                                        'chart':get_trainning_chart()})


def main():
    application = webapp.WSGIApplication([
        (r'/graph/index.php',IndexHander),
        ],debug=True)
        
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
