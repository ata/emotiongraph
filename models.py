from google.appengine.ext import db
from datetime import datetime
import re

class User(db.Model):
    uid = db.IntegerProperty(required=True)
    name = db.StringProperty()
    friends = db.ListProperty(long)
    tranning_queue = db.ListProperty(long)
    def save(self):
        if db.Query(User).filter('uid = ', self.uid).count() == 0:
            self.put()

class Keyword(db.Model):
    word = db.StringProperty(required = True)
    marah = db.IntegerProperty(default = 0)
    senang = db.IntegerProperty(default = 0)
    jijik = db.IntegerProperty(default = 0)
    takut = db.IntegerProperty(default = 0)
    malu = db.IntegerProperty(default = 0)
    bersalah = db.IntegerProperty(default = 0)
    sedih = db.IntegerProperty(default = 0)
    valid = db.BooleanProperty(default = True)
            
    @classmethod
    def update(cls, status):
        #keyword smiley
        custume = re.findall(r'%s' % (CustumeKeyword.get_rstring()), status.message)
        
        # Keyword string
        words = re.findall(r'\w+', status.message)
        
        keywords = words + custume
        
        for word in keywords:
            query = db.Query(Keyword).filter('word = ',word.lower())
            if query.count() == 0:
                keyword = Keyword(word = word.lower())
                exec("keyword.%s = 1" % (status.category))
                keyword.put()
                
            else:
                keyword = query.fetch(1)[0]
                exec("keyword.%s += 1" % (status.category))
                keyword.put()
                
class CustumeKeyword(db.Model):
    plain = db.StringProperty(required = True)
    escape = db.StringProperty()
    def save(self):
        if db.Query(CustumeKeyword).filter('plain = ', self.plain).count() == 0:
            self.escape = re.escape(self.plain)
            self.put()
    
    @classmethod
    def get_rstring(cls):
        rstring = ''
        for s in CustumeKeyword.all().fetch(1000):
            rstring += "(%s)" % (s.escape)
        return "[%s]+" % (rstring)
    
    @classmethod
    def add(cls, *args):
        for custume in args: 
            CustumeKeyword(plain = custume).save()

class Status(db.Model):
    user = db.ReferenceProperty(reference_class = User, collection_name = 'states')
    status_id = db.IntegerProperty()
    message = db.StringProperty(multiline=True)
    time = db.DateTimeProperty()
    uid = db.IntegerProperty()
    category = db.StringProperty(choices=('marah','senang','jijik','takut','malu',
                                        'bersalah','sedih','uncategory'))
    
    def save(self):
        if db.Query(Status).filter('status_id = ', self.status_id).count() == 0:
            self.put()
            
    def set_time(self,time):
        self.time = datetime.fromtimestamp(time)

def data_clean(*args):
    if len(args) == 0:
        data_clean(User,Keyword,Status)
    else:
        for c in args: 
            for e in c.all():
                e.delete()


def get_trainning_static():
    return {
            'total':Status.all().filter('category != ',None).count(),
            'senang':Status.all().filter('category = ','senang').count(),
            'sedih':Status.all().filter('category = ','sedih').count(),
            'marah':Status.all().filter('category = ','marah').count(),
            'malu':Status.all().filter('category = ','malu').count(),
            'bersalah':Status.all().filter('category = ','bersalah').count(),
            'jijik':Status.all().filter('category = ','jijik').count(),
            'takut':Status.all().filter('category = ','takut').count(),
            'uncategory':Status.all().filter('category = ','uncategory').count()
            }
            
def get_trainning_chart():
    base_url = 'http://chart.apis.google.com/chart?cht=p3'
    static = get_trainning_static()
    data = '&chd=t:%d,%d,%d,%d,%d,%d,%d,%d&chs=500x200' % (\
            static['senang'],static['sedih'],static['marah'],\
            static['malu'],static['bersalah'],static['jijik'],\
            static['takut'],static['uncategory'])
    label = '&chl=senang|sedih|marah|malu|bersalah|jijik|takut|uncategory'
    return base_url + data + label
    
    
