from google.appengine.ext import db

class EmotionPattern(db.Model):
    jijik = db.TextProperty()
    sedih = db.TextProperty()
    senang = db.TextProperty()
    marah = db.TextProperty()
    takut = db.TextProperty()
    malu = db.TextProperty()
    bersalah = db.TextProperty()
    
    @classmethod
    def get_jijik(cls):
        return '(%s)'% (db.Query(EmotionPattern).fetch(1)[0].jijik)
        
    @classmethod
    def add_jijik(cls,keywords):
        emo = db.Query(EmotionPattern).fetch(1)[0]
        for k in keywords.split(','):
            emo.jijik += k.strip()
        emo.put()
        
        
    @classmethod
    def get_sedih(cls):
        return '(%s)' % db.Query(EmotionPattern).fetch(1)[0].sedih
    @classmethod
    def add_jijik(cls,keywords):
        emo = db.Query(EmotionPattern).fetch(1)[0]
        for k in keywords.split(','):
            emo.jijik += k.strip()
        emo.put()
    
    
    @classmethod
    def get_senang(cls):
        return db.Query(EmotionPattern).fetch(1)[0].senang
    @classmethod
    def get_marah(cls):
        return db.Query(EmotionPattern).fetch(1)[0].marah
    @classmethod
    def get_takut(cls):
        return db.Query(EmotionPattern).fetch(1)[0].takut
    @classmethod
    def get_malu(cls):
        return db.Query(EmotionPattern).fetch(1)[0].malu
    @classmethod
    def get_bersalah(cls):
        return db.Query(EmotionPattern).fetch(1)[0].bersalah
