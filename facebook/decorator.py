import config
from facebook import Facebook

class BaseDecorator(object):
    self.fb = Facebook(config.FB_API_KEY, config.FB_SECRET_KEY)

class FBConnect(BaseDecorator):
    def __init__(self, func):
        self.func = func
    def __call__(self):
        
        self.func(self)

