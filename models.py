from google.appengine.ext import db
from datetime import datetime
import re

class User(db.Model):
    uid = db.IntegerProperty(required=True);
    name = db.StringProperty()
    

class FBUser(db.Model):
    
    uid = db.IntegerProperty(required=True);
    name = db.StringProperty()
    def save(self):
        if db.Query(User).filter('uid = ', self.uid).count() == 0:
            self.put()

class Keyword(db.Model):
    word = db.StringProperty()
    count = db.IntegerProperty()
            
    @classmethod
    def update(cls, status):
        words = re.findall('\w+',status)
        for word in words:
            query = db.Query(Keyword).filter('word = ',word)
            if query.count() == 0:
                Keyword(word = word, count = 1).put()
            else:
                keyword = query.fetch(1)[0]
                keyword.count = keyword.count + 1
                keyword.put()

class FBStatus(db.Model):
    
    user = db.ReferenceProperty(reference_class=FBUser,required=True,
                                collection_name = 'states')
    status_id = db.IntegerProperty();
    message = db.StringProperty(multiline=True)
    time = db.DateTimeProperty()
    emotion = db.StringProperty(choices=('marah','senang','jijik','takut','malu',
                                        'bersalah','sedih'))
    
    def save(self):
        if db.Query(Status).filter('status_id = ', self.status_id).count() == 0:
            self.put()
            
    def set_time(self,time):
        self.time = datetime.fromtimestamp(time)
