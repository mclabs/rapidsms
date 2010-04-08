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
        message.was_handled = False

    def handle (self, message):
        try:
            func, captures = self.keyword.match(self, message.text)
        except TypeError:
           
	    return False 
	try:
            self.handled = func(self, message, *captures)
        except HandlerFailed, e:
            message.respond(e)
            self.handled = True
        except Exception, e:
            print e
            message.respond("An error has occured %s" % e)
            raise
        message.was_handled = bool(self.handled)
        return self.handled

    keyword.prefix = ["grade","g","gd"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def child_grade(self, message,student_code,overall_grade,term):
	'''student grades per term
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
	return True
    child_grade.format="grade [student_code] [grade] [term]"
       

    keyword.prefix = ["enrollment","e","en"]
    @keyword(r'(\S+) (\d+) (\S+) (\d+)')
    @registered
    def enrollment_per_center(self,message,male_code,male_count,female_code,female_count):
	'''enrollment per term
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
	return True
    enrollment_per_center.format="en [male_code] [male_count] [female_code] [female_count]"


    keyword.prefix = ["amount","a","amt"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def amount_raised(self, message,amount,organisation,source):
	'''amount raised
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
	return True
    amount_raised.format="amount [amount] [organisation_code] [source]"


    keyword.prefix = ["food"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def food_distribution(self, message):
	'''amount raised
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
	return True
    food_distribution.format=""
      

