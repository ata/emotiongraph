class Mahasiswa:
    
    @classmethod
    def m1(cls):
        cls.m2()
    @classmethod
    def m2(cls):
        print 'm2'
        
Mahasiswa.m1()
