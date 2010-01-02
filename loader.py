from google.appengine.ext import db
from google.appengine.tools import bulkloader
import analysis.models 

class FBUserLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'FBUser',
                                   [('uid', lambda x: x.decode('utf-8')),
                                    ('name', lambda x: x.decode('utf-8')),
                                    ('religion', lambda x: x.decode('utf-8')),
                                   ])

loaders = [FBUserLoader]
