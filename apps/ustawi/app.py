import rapidsms
import re
from rapidsms.parsers.keyworder import Keyworder
from apps.reporters.models import *
from apps.ustawi.models import *


class HandlerFailed (Exception):
    pass


def registered(func):

    def wrapper(self, message, *args):
	ustawi_reporter=Coordinator.objects.filter(mobile_number=message.peer)
        if ustawi_reporter:
		return func(self, message, *args)
	else:
		message.respond("Sorry, only registered Ustawi users "
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


    def handle(self, message):
        ''' Function selector

        Matchs functions with keyword using Keyworder
        Replies formatting advices on error
        Return False on error and if no function matched '''
        try:
            func, captures = self.keyword.match(self, message.text)
        except TypeError:
            # didn't find a matching function
            # make sure we tell them that we got a problem
            command_list = [method for method in dir(self) \
                            if hasattr(getattr(self, method), "format")]
            input_text = message.text.lower()
            for command in command_list:
                format = getattr(self, command).format
                try:
                    first_word = (format.split(" "))[0]
                    if input_text.find(first_word) > -1:
                        message.respond("Unknown ustawi SMS format please try %s"%format)
                        return True
                except:
                    #message.respond("Sorry Unknown command: '%(msg)s...' Please try again"% {'msg': message.text[:20]})
		    #return True
                    pass
            return False
        try:
            self.handled = func(self, message, *captures)
        except HandlerFailed, e:
            message.respond(e.message)

            self.handled = True
        except Exception, e:
            # TODO: log this exception
            # FIXME: also, put the contact number in the config
            message.respond("An error occurred. Please call")

            raise
        message.was_handled = bool(self.handled)
        return self.handled

    keyword.prefix = ["ustawi"]
    @keyword(r'(\S+)')
    @registered
    def subscribe (self,message,token):
	self.debug("registering ustawi reporter")
	ustawi_reporter=Coordinator.objects.get(mobile_number=message.peer)
	if ustawi_reporter:
		per_con=message.persistant_connection
		per_con.reporter=ustawi_reporter
		per_con.save()
	message.respond("Thank you for activating your Ustawi account")
	return True
    subscribe.format="ustawi join"

    
    
    keyword.prefix = ["sales","s","sl"]
    @keyword(r'(\S+) (\S+) (\S+) (\S+)')
    @registered
    def crop_sales(self, message,farm,crop,weight,price):
	'''crop sales
        Format: sales [crop] [weight] [price] 
        '''
	
	message.respond(message.text)
	return True
    crop_sales.format="sales [farm] [crop] [weight] [price]"


    keyword.prefix = ["harvest","h","yield"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def crop_harvests(self, message,farm,crop,amount):
	message.respond(message.text)
	return True
    crop_harvests.format="harvest [farm] [crop] [weight] [price]"


    keyword.prefix = ["store"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def storage(self, message,farm,crop,amount):
	message.respond(message.text)
	return True
    storage.format="store [farm] [crop] [weight] [price]"


    keyword.prefix = ["fc"]
    @keyword(r'(\d+) (\w+)')
    @registered
    def farmers_count(self, message,head_count,location):
    	''' number of farmers in a location
        Format: fc [head_count] [location] 
        '''
	message.respond(message.text)
	return True
    farmers_count.format="fc [farm] [crop] [weight] [price]"

    
    keyword.prefix = ["v"]
    @keyword(r'(\d+) (\w+)')
    @registered
    def farm_visitors(self, message,head_count,location):
	'''
        Format: visitors [head_count] 
        '''
	message.respond(message.text)
	return True
    farm_visitors.format="v [farm] [crop] [weight] [price]"
