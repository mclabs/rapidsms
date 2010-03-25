import rapidsms
import re
from rapidsms.parsers.keyworder import Keyworder
from apps.reporters.models import Reporter
from apps.girlchild.models import *


class HandlerFailed (Exception):
    pass


def registered(func):

    def wrapper(self, message, *args):
        if message.persistant_connection.reporter:
            return func(self, message, *args)
        else:
            message.respond("Sorry, only registered users "
                               "can access this program.")
            return True
    return wrapper

class App (rapidsms.app.App):
    keyword=Keyworder()
    handled=False
    	
    def start (self):
        """Configure your app in the start phase."""
        pass

    def parse (self, message):
        """Parse and annotate messages in the parse phase."""
        pass

    def handle (self, message):
        try:
            func, captures = self.keyword.match(self, message.text)
        except TypeError:
            # didn't find a matching function
            message.respond("Error. Your message could not be recognized by the system. Please check syntax and retry.")
            return False
        try:
            handled = func(self, message, *captures)
        except HandlerFailed, e:
            print e
            handled = True
        except Exception, e:
            print e
            message.respond("An error has occured %s" % e)
            raise
        message.was_handled = bool(handled)
        return handled

    keyword.prefix = ["fgm"]
    @keyword(r'(\d+) (\S+)')
    @registered
    def fgm_rescue(self,message,head_count):
	'''enrollment per term
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
       

    keyword.prefix = ["employed","emp"]
    @keyword(r'(\d+) (\S+)')
    @registered
    def girls_employed(self,message,head_count,month):
	'''enrollment per term
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)


    keyword.prefix = ["voc"]
    @keyword(r'(\d+) (\S+)')
    @registered
    def girls_vocational_training(self,message,head_count,month):
	'''enrollment per term
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)

    keyword.prefix = ["voc"]
    @keyword(r'(\d+) (\S+)')
    @registered
    def campaigns(self,message):
	'''enrollment per term
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
