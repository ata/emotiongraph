from google.appengine.ext import db
from datetime import datetime
import re

class User(db.Model):
    uid = db.IntegerProperty(required=True);
    name = db.StringProperty()
    friends = db.ListProperty(long)
    tranning_queue = db.ListProperty(long)
    def save(self):
        if db.Query(User).filter('uid = ', self.uid).count() == 0:
            self.put()

class Smiley(db.Model):
    plain = db.StringProperty(required = True)
    escape = db.StringProperty()
    
    @classmethod
    get_rstring(cls):
        rstring = ''
        for s in Smiley.all():
            rstring += "(%s)" % (s.escape)
        return "r[%s]" % (rstring)
    def save(self):
        if Smiley.all().filter('plain = ', self.plain).count() == 0:
            self.escape = re.escape(self.plain)
            self.put()

class Keyword(db.Model):
    word = db.StringProperty(required = True)
    type = db.StringProperty(choice = ('smiley','word'), default = 'word')
    marah = db.IntegerProperty(default = 0)
    senang = db.IntegerProperty(default = 0)
    jijik = db.IntegerProperty(default = 0)
    takut = db.IntegerProperty(default = 0)
    malu = db.IntegerProperty(default = 0)
    bersalah = db.IntegerProperty(default = 0)
    sedih = db.IntegerProperty(default = 0)
            
    @classmethod
    def update(cls, status, emotion):
        #keyword smiley
        smiles = re.findall(r'%s' % (Smiley.get_rstring()), status)
        
        # Keyword string
        words = re.findall(r'\w+', status)
        for word in words:
            query = db.Query(Keyword).filter('word = ',word)
            if query.count() == 0:
                Keyword(word = word)
                exec("self.%s = 1" % (emotion))
            else:
                keyword = query.fetch(1)[0]
                keyword.count = keyword.count + 1
                keyword.put()

class Status(db.Model):
    
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
