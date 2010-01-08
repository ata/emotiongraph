class Ibu(object):
    def makan(self):
        print 'pakai sendok'
        print self.name

class Ayah(object):
    def makan(self):
        print 'pakai mulut'
        
class Anak(Ibu,Ayah):
    name = 'Ata'
    def makan(self):
        super(Ibu,self).makan()

Anak().makan()
