import rapidsms
import re
from rapidsms.parsers.keyworder import Keyworder
from apps.reporters.models import *
from apps.shabaa.models import *


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

    keyword.prefix = ["visitors","visit","v"]
    @keyword(r'(\d+) (\w+)')
    @registered
    def vistors(self, message,head_count,code):
	#FORMAT: enterprise count jobs count
	#match
	message.respond(industry+" "+ count+" "+location)

