import rapidsms
import re
from rapidsms.parsers.keyworder import Keyworder
from apps.reporters.models import *
from apps.locations.models import Location
from apps.shabaa.models import *

from rapidsms.message import Message
from rapidsms.connection import Connection


class HandlerFailed (Exception):
    pass




def registered(func):

    def wrapper(self, message, *args):
	shabaa_reporter=ShabaaReporter.objects.filter(mobile_number=message.peer)
        if shabaa_reporter:
		return func(self, message, *args)
	else:
		message.respond("Sorry, only registered Shabaa users "
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
                        message.respond("Unknown shabaa SMS format please try %s"%format)
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

    keyword.prefix = ["shabaa"]
    @keyword(r'(\S+)')
    @registered
    def subscribe (self,message,token):
	self.debug("registering shabaa reporter")
	shabaa_reporter=ShabaaReporter.objects.get(mobile_number=message.peer)
	if shabaa_reporter:
		per_con=message.persistant_connection
		per_con.reporter=shabaa_reporter
		per_con.save()
	message.respond("Thank you for activating your Shabaa account")
	return True
    subscribe.format="shabaa join"

    	
    keyword.prefix = ["act"]
    @keyword(r'(\w+) (M) (\d+) (F) (\d+) (\d{6,8}) (\S+)')
    @registered
    #format: activity code male/female number_of_attendees date location
    def activities(self, message,code,male_gender,male_count,female_gender,female_count,activity_date,loc_code):
	activity_code=code
	shabaa_reporter=ShabaaReporter.objects.get(mobile_number=message.peer)
	#self.debug(message.persistant_connection.reporter.id)
	try:
		activity_type=ActivityType.objects.get(code=activity_code)
	except models.ObjectDoesNotExist:
		message.respond("Sorry the activity code entered is wrong")
		return True
	#check if location code is valid
	try:
		location=Location.objects.get(code=loc_code)
	except models.ObjectDoesNotExist:
		message.respond("Invalid location code")
		return True
	actv=Activity(activitytype=activity_type,
	male_attendees=male_count,
	female_attendees=female_count,
	activity_date="2003-08-04",
	reporter=shabaa_reporter,
	location=location)
	actv.save()
	message.respond("Thank you for submitting your activity to Shabaa- KCDF")
	return True
    activities.format="actv [activity_code] M [number_of_people] F [number_of_people] [date-YYYYMMDD] [Location_code]"

       

    keyword.prefix = ["enterprise","ent","entr"]
    @keyword(r'(\S+) (\S+) (\S+)')
    @registered
    #format: ent industry_code number_of_employees location
    def enterprise(self, message,industry_code,head_count,loc_code):
	shabaa_reporter=ShabaaReporter.objects.get(mobile_number=message.peer)
	try:
		industry=Industry.objects.get(code=industry_code)
	except models.ObjectDoesNotExist:
		message.respond("Sorry the industry code you have entered. Please enter correct code and resend SMS")
		return True
		#check if location code is valid
	try:
		location=Location.objects.get(code=loc_code)
	except models.ObjectDoesNotExist:
		message.respond("Invalid location code")
		return True

	enterprise=Enterprise(jobs_created=head_count,
	industry=industry,
	reporter=shabaa_reporter,
	location=location)
	enterprise.save()
	message.respond("Thank you for submitting your enterprise to Shabaa- KCDF")
	return True
    enterprise.format="ent [industry_code] [head_count] [Location_code]"

    keyword.prefix = ["visit","v"]
    @keyword(r'(\w+) (\d+)')
    @registered
    #format: v visitor_type number_of_visitors date-mmYYYY'''
    def visitor_count(self, message,code,head_count):
	visitor_code=code
	try:
		visitor_type_type=VisitorType.objects.get(code=visitor_code)
	except models.ObjectDoesNotExist:
		message.respond("Sorry the visitor code entered is wrong")
		return True

	message.respond("Thank you for submitting your activity to Shabaa- KCDF")
	return True
    visitor_count.format="v [type_of_visitor] [number_of_visitors]"


