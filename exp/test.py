class Decorate(object):
    def __init__(self,func):
        self.func = func
    def __call__(self, *args, **kwargs):
        print 'before'
        self.nama = "Ata"
        self.func(self, *args, **kwargs)
    
class Ibu(object):
   
    @Decorate
    def makan(self,s = 'sesuatu'):
        print 'pakai sendok %s' % (s)
        print self.nama

Ibu().makan('nnn')
