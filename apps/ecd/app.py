import rapidsms
import re
from rapidsms.parsers.keyworder import Keyworder
from apps.reporters.models import *
from apps.locations.models import Location
from apps.ecd.models import *


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

    keyword.prefix = ["grade","g","gd"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def student_grade(self, message,student_code,overall_grade,term):
	'''student grades per term
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
       

    keyword.prefix = ["enrollment","e","en"]
    @keyword(r'(\S+) (\d+) (\S+) (\d+)')
    @registered
    def enrollment_per_term(self,message,male_code,male_count,female_code,female_count):
	'''enrollment per term
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)


    keyword.prefix = ["amount","a","amt"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def amount_raised(self, message,amount,organisation,source):
	'''amount raised
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
