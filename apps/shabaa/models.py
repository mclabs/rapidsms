from django.db import models
from apps.locations.models import Location
from apps.reporters.models import Reporter,PersistantConnection, Location 

class Permissions(models.Model):
    '''This is a fake model that has nothing in it, because
       django expects all app-level permissions to be in
       a model'''
    
    class Meta:
        # the permission required for this tab to display in the UI
        permissions = (
            ("can_view", "Can view"),
        )


	
	
class Organisation(models.Model):
	organisation=models.CharField(max_length=160)

	def __unicode__ (self):
		return self.organisation


class ShabaaReporter(Reporter):
	GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
	)
	gender=models.CharField(max_length=1,choices=GENDER)
	email=models.CharField(max_length=100,blank=True)
	organisation=models.ForeignKey(Organisation)
	mobile_number=models.CharField(max_length=100,blank=True,help_text="Number format is +2547XXXXXXXX")

	def __unicode__ (self):
		return self.alias
		

		
	

class Industry(models.Model):
	industry=models.CharField(max_length=100)
	code=models.CharField(max_length=160)

	def  __unicode__ (self):
		return self.industry

	class Meta:
		verbose_name_plural="Industry"


class ActivityType(models.Model):
	activity_type=models.CharField(max_length=160)
	code=models.CharField(max_length=160)

	def  __unicode__ (self):
		return self.activity_type

	class Meta:
		verbose_name_plural="Activity Type"


class Activity(models.Model):
	male_attendees=models.CharField(max_length=160)
	female_attendees=models.CharField(max_length=160)
	created_at=models.DateTimeField(auto_now_add=1)
	activity_date=models.DateField()
	activitytype=models.ForeignKey(ActivityType)
	reporter=models.ForeignKey(ShabaaReporter)
	alias=models.SlugField()
	location=models.ForeignKey(Location)

	def save(self):
		self.alias="%s-Enterprise-from-%s"%(self.activitytype, self.reporter)
		super(Activity,self).save()
		

	def  __unicode__ (self):
		return self.activitytype.activity_type
	
	class Meta:
		verbose_name_plural="Activities"

class Enterprise(models.Model):
	jobs_created=models.CharField(max_length=160)
	industry=models.ForeignKey(Industry)
	reporter=models.ForeignKey(ShabaaReporter)
	location=models.ForeignKey(Location)
	created_at=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural="Enterprises Created"

	def  __unicode__ (self):
		return "%s Enterprise from %s"%(self.industry, self.reporter)


class VisitorType(models.Model):
	visitor_type=models.CharField(max_length=160)
	code=models.CharField(max_length=160)

	def  __unicode__ (self):
		return self.visitor_type

	class Meta:
		verbose_name_plural="Visitor Type"
"""


class Visitor(models.Model):
	visitor_count=models.CharField(max_length=160)
	visitortype=models.ForeignKey(VisitorType)
	reporter=models.ForeignKey(ShabaaReporter)
	created_at=models.DateTimeField(auto_now_add=1)

	def  __unicode__ (self):
		return self.visitortype.visit_type


	class Meta:
		verbose_name_plural="Visitors"

"""	