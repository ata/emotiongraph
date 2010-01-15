from google.appengine.ext import db
from google.appengine.api import memcache
from datetime import datetime
import re
    

class User(db.Model):
    uid = db.IntegerProperty()
    name = db.StringProperty()
    login = db.UserProperty(auto_current_user_add = True)
    def save(self):
        if User.all().filter('uid = ', self.uid).count() == 0:
            self.put()

class Friend(db.Model):
    user = db.ReferenceProperty(reference_class = User, collection_name = 'friends')
    uid = uid = db.IntegerProperty(required=True)
    trainning = db.BooleanProperty()
    
    def save(self):
        if Friend.all().filter('uid = ', self.uid).count() == 0:
            self.put()
    
    @classmethod
    def get_trainnings(cls,user, count = 20, offset = 0):
        query = Friend.all().filter('user = ',user).filter('trainning = ',True)
        if query.count() == 0:
            return False
        else:
            return query.fetch(count, offset)

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
        #custume = re.findall(r'%s' % (CustumeKeyword.get_rstring()), status.message)
        
        # Keyword string
        words = re.findall(r'\w+', status.message)
        
        keywords = words #+ custume
        
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
    
    @classmethod
    def get_regex(cls,category):
        regex = ''
        query = Keyword.all()
        query.filter('%s > ' %(category),0)
        query.filter('valid = ',True)
        query.order('-%s' % (category))
        for k in query.fetch(1000):
            regex += "%s|" % (k.word)
        return (regex.strip('|'))
    
    @classmethod
    def generate_cache(cls):
        pass
    
    
    @classmethod
    def generate_probs_cache(cls, category):
        
        words = cls.get_list_cache(category)
        for word in words:
            cls.get_prob(category,word)
            
        return True
        
    @classmethod
    def generate_list_cache(cls):
        emotion = ['senang','sedih','marah','malu',
                 'jijik','takut','bersalah']
        for e in emotion:
            cls.get_list_cache(e)
        
        return True
    
    @classmethod 
    def get_regex_cache(cls,category):
        data = memcache.get(category)
        if data is not None:
            return data
        else:
            data = cls.get_regex(category)
            memcache.add(category,data,3600)
            return data
    
    @classmethod
    def count_all(cls,filter = None,filter_value = None):
        """
        Count *all* of the rows (without maxing out at 1000)
        """
        count = 0
        query = cls.all().filter('valid = ',True)
        
        if filter != None:
            query.filter(filter,filter_value)
        
        query.order('__key__')

        while count % 1000 == 0:
            current_count = query.count()
            count += current_count

            if current_count == 1000:
                last_key = query.fetch(1, 999)[0].key()
                query = query.filter('__key__ > ', last_key)

        return count
        
    @classmethod
    def get_all(cls,filter = None,filter_value = None):
        """
        Count *all* of the rows (without maxing out at 1000)
        """
        count = 0
        result = []
        query = cls.all().order('__key__')
        query.filter('valid = ', True)
        
        if filter != None:
            query.filter(filter,filter_value)

        while count % 1000 == 0:
            current_count = query.count()
            count += current_count
            result += query.fetch(1000)
            
            if current_count == 1000:
                last_key = query.fetch(1, 999)[0].key()
                query = query.filter('__key__ > ', last_key)

        return result
    
    
    @classmethod
    def get_list_cache(cls,category):
        data = memcache.get('keyword_list_%s' % (category))
        if data is not None:
            return data
        else:
            words = []
            query = cls.all()
            query.filter('%s > ' %(category),0)
            query.filter('valid = ',True)
            query.order('-%s' % (category))
            for word in query.fetch(1000):
                words.append(word.word)
            
            memcache.add('keyword_list_%s' % (category),words,3600)
            return words
            
        
    @classmethod
    def get_prob(cls,category,word):
        word = word.lower()
        data = memcache.get('prob_%s_%s' % (category, word))
        if data is not None:
            return data
        else:
            word_in_category = cls.get_word_in_category(category)
            keyword = cls.all().filter('word = ',word).get()
            word_count = 0
            exec('word_count = keyword.%s' % (category))
            data = float(word_count) /  float(word_in_category)
            memcache.add('prob_%s_%s' % (category, word), data, 3600)
            return data
            
    @classmethod
    def get_word_in_category(cls,category):
        
        data = memcache.get('word_count_%s' % (category))
        if data is not None:
            return data
        else:
            count = 0
            query = cls.all()
            query.filter('%s > ' %(category),0)
            query.filter('valid = ',True)
            query.order('-%s' % (category))
            for word in query.fetch(1000):
                exec('count += word.%s' % (category))
            
            memcache.add('word_count_%s' % (category),count,3600)
            
            return count
    
    
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
    
    
    @classmethod
    def count_all(cls):
        """
        Count *all* of the rows (without maxing out at 1000)
        """
        count = 0
        query = cls.all().order('__key__')

        while count % 1000 == 0:
            current_count = query.count()
            count += current_count

            if current_count == 1000:
                last_key = query.fetch(1, 999)[0].key()
                query = query.filter('__key__ > ', last_key)

        return count
    
    @classmethod
    def get_probs(cls,message):
        
        words = re.findall(r'\w+',message)
        probs = {'senang':0.0,'sedih':0.0,'marah':0.0,'malu':0.0,
                 'jijik':0.0,'takut':0.0,'bersalah':0.0}
        
        for category in probs.keys():
            valids = Keyword.get_list_cache(category)
            for word in words:
                if word in valids:
                    probs[category] += Keyword.get_prob(category,word)
        
        return probs
    
    @classmethod
    def check_emotion(cls,message):
        probs = cls.get_probs(message)
        hight = 'senang'
        
        for category in probs:
            if probs[category] > probs[hight]:
                hight = category
        
        return hight

#def data_clean(*args):
#    if len(args) == 0:
#        data_clean(User,Keyword,Status)
#    else:
#        for c in args: 
#            for e in c.all():
#                e.delete()



    
