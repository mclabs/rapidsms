import rapidsms
import re
from rapidsms.parsers.keyworder import Keyworder
from apps.reporters.models import *
from apps.ustawi.models import *


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
	    # didn't find a matching function
            # make sure we tell them that we got a problem
            command_list = [method for method in dir(self) \
                            if hasattr(getattr(self, method), 'format')]
            birth_input = message.text.lower()
            for command in command_list:
                format = getattr(self, command).format
                try:
                    first_word = (format.split(' '))[0]
                    if birth_input.find(first_word) > -1:
                        message.respond(format)
                        return True
                except Exception, e:
                    pass
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

    keyword.prefix = ["sales","s","sl"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def crop_sales(self, message,crop,weight,price):
	'''crop sales
        Format: sales [crop] [weight] [price] 
        '''
	
	message.respond(message.text)
	return True
    crop_sales.format=" sales [crop_code] [weight] [price]"


    keyword.prefix = ["harvest","h","yield"]
    @keyword(r'(\S+) (\S+)')
    @registered
    def crop_harvests(self, message,crop,amount):
	message.respond(message.text)
	return True
    crop_harvests.format="h [crop_code] [amount]"


    keyword.prefix = ["fc"]
    @keyword(r'(\d+) (\w+)')
    @registered
    def farmers_count(self, message,head_count,location):
    	''' number of farmers in a location
        Format: fc [head_count] [location] 
        '''
	message.respond(message.text)
	return True
    farmers_count.format="fc [head_count] [location]"

    
    keyword.prefix = ["visitors","visit","v"]
    @keyword(r'(\d+) (\w+)')
    @registered
    def farm_visitors(self, message,head_count,location):
	'''
        Format: visitors [head_count] 
        '''
	message.respond(message.text)
    farm_visitors.format="visitors [blah]"

