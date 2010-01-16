from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from models import *
from google.appengine.api import memcache

import base
import analysis

class CronProbsHandler(base.BaseRequestHandler):
    def get(self):
        
        last_emotion_index = memcache.get('last_cron_emotion_index')
        
        if last_emotion_index is None:
            memcache.set('last_cron_emotion_index', 0, 3600 * 24)
            last_emotion_index = 0
        
        emotion = ['senang','sedih','marah','malu',
                 'jijik','takut','bersalah']
        
        if Keyword.generate_probs_cache(emotion[last_emotion_index]):
            self.response.out.write("Ok => %s" % (emotion[last_emotion_index]))
            last_emotion_index += 1
            if last_emotion_index == 7:
                last_emotion_index = 0
            memcache.set('last_cron_emotion_index', last_emotion_index, 3600 * 24)
        
            


class CronWordsHandler(base.BaseRequestHandler):
    def get(self):
        Keyword.generate_list_cache()
        #analysis.trainning_smiley()
        self.response.out.write("Ok")

def main():
    application = webapp.WSGIApplication([
        (r'/cron-probs.php',CronProbsHandler),
        (r'/cron-words.php',CronWordsHandler)
        ],debug=True)
        
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
