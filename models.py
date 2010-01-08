from google.appengine.ext import db
from datetime import datetime

class FBUser(db.Model):
    
    uid = db.IntegerProperty(required=True);
    name = db.StringProperty()
    complete = db.StringProperty()
    emotion = db.StringProperty(choices=('marah','senang','jijik','takut','malu',
                                        'bersalah','sedih'))
    def save(self):
        if db.Query(User).filter('uid = ', self.uid).count() == 0:
            self.put()

class Keyword(db.Model):
    type = db.StringProperty()
    word = db.StringProperty()
    count = db.IntegerProperty()
    
    def save(self):
        self.word = self.word.strip()
        if db.Query(Keyword).filter('word = ', self.word).count() == 0:
            self.put()
    @classmethod
    def get_type(self,type,count = 1000):
        pass

class FBStatus(db.Model):
    
    user = db.ReferenceProperty(reference_class=FBUser,required=True,
                                collection_name = 'states')
    status_id = db.IntegerProperty();
    message = db.StringProperty(multiline=True)
    time = db.DateTimeProperty()
    
    def save(self):
        if db.Query(Status).filter('status_id = ', self.status_id).count() == 0:
            self.put()
            
    def set_time(self,time):
        self.time = datetime.fromtimestamp(time)
