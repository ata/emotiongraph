from google.appengine.ext import db
from google.appengine.tools import bulkloader
import analysis.models 

class FBUserExporter(bulkloader.Exporter):
    def __init__(self):
        bulkloader.Exporter.__init__(self, 'FBUser',
                                   [('uid', lambda x: x.decode('utf-8')),
                                    ('name', lambda x: x.decode('utf-8')),
                                    ('religion', lambda x: x.decode('utf-8')),
                                   ])

exporters = [FBUserExporter]
