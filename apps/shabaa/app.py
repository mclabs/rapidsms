import rapidsms
import re
from rapidsms.parsers.keyworder import Keyworder
from apps.reporters.models import *
from apps.locations.models import Location
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
        message.was_handled = False

    def handle (self, message):
        try:
            func, captures = self.keyword.match(self, message.text)
        except TypeError:
            # didn't find a matching function
	    
	    message.respond("Sorry Unknown command: '%(msg)s...' Please try again"% {'msg': message.text[:20]})
	    return False
        try:
            self.handled = func(self, message, *captures)
        except HandlerFailed, e:
            message.respond(e)
            self.handled = True
        except Exception, e:
            message.respond("An error has occured %s" % e)
            raise
        message.was_handled = bool(self.handled)
        return self.handled

    keyword.prefix = ["activity","actv","act"]
    @keyword(r'(\w+) (M) (\d+) (F) (\d+) (\d{6,8}) (\w+)')
    @registered
    #format: activity code male/female number_of_attendees date location
    def activities(self, message,code,male_gender,male_count,female_gender,female_count,activity_date,loc_code):
	activity_code=code
	self.debug(message.persistant_connection.reporter.id)
	try:
		activity_type=ActivityType.objects.get(code=activity_code)
	except models.ObjectDoesNotExist:
		message.respond("Sorry the activity code entered is wrong")
		return True
	#check if location code is valid
	try:
		Location=Location.objects.get(code=loc_code)
	except models.ObjectDoesNotExist:
		message.respond("Invalid location code")
		return True
	actv=Activity(activitytype=activity_type,
	male_attendees=male_count,
	female_attendees=female_count,
	reporter=message.persistant_connection.reporter)
	#actv.save()
	message.respond("Thank you for submitting your activity to KCDF")
	return True
    activities.format="actv [activity_code]"

       

    keyword.prefix = ["enterprise","ent","entr"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    #format: ent industry_code number_of_employees location
    def enterprise(self, message,industry_code,head_count,location):
	message.respond(message.text)
	return True
    enterprise.format="ent [industry_code] [jobs_created] [location]"

    keyword.prefix = ["visitors","visit","v"]
    @keyword(r'(\w+) (\d+)')
    @registered
    #format: v visitor_type number_of_visitors date-mmYYYY'''
    def visitors(self, message,code,head_count):
	visitor_code=code
	try:
		visitor_type_type=VisitorType.objects.get(code=visitor_code)
	except models.ObjectDoesNotExist:
		message.respond("Sorry the visitor code entered is wrong")
		return True

	message.respond(message.text)
	return True
    visitors.format="v [type_of_visitor] [number_of_visitors]"


