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
                        message.respond("Unknown ECD SMS format please try %s"%format)
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

    keyword.prefix = ["amount"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    def amount_raised(self, message,amount,organisation,source):
	'''amount raised
        Format: sales [crop] [weight] [price] 
        '''
	message.respond(message.text)
	return True
    amount_raised.format="amount [amount] [organisation_code] [source]"
