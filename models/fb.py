from google.appengine.ext import db
from datetime import datetime

class User(db.Model):
    
    uid = db.IntegerProperty(required=True);
    name = db.StringProperty()
    
    def save(self):
        if db.Query(User).filter('uid = ', self.uid).count() == 0:
            self.put()
        

class Status(db.Model):
    
    user = db.ReferenceProperty(reference_class=User,required=True,
                                collection_name = 'states')
    status_id = db.IntegerProperty();
    message = db.StringProperty(multiline=True)
    time = db.DateTimeProperty()
    
    def save(self):
        if db.Query(Status).filter('status_id = ', self.status_id).count() == 0:
            self.put()
            
    def set_time(self,time):
        self.time = datetime.fromtimestamp(time)
