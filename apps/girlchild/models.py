from django.db import models
from apps.locations.models import Location
from apps.reporters.models import Reporter

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
	activity_date=models.DateTimeField()
	activitytype=models.ForeignKey(ActivityType)
	reporter=models.ForeignKey(Reporter)
	alias=models.SlugField()

	def save(self):
		self.alias=slugify(self.activitytype.activity_type+reporter.alias)
		super(Activity,self).save()
		

	def  __unicode__ (self):
		return self.activitytype.activity_type
	
	class Meta:
		verbose_name_plural="Activities"

"""
class Enterprise(models.Model):
	employees=models.CharField(max_length=160)
	industry=models.ForeignKey(Industry)
	reporter=models.ForeignKey(Reporter)
	created_at=models.DateTimeField(auto_now_add=1)

	class Meta:
		verbose_name_plural="Enterprises Created"


class Industry(models.Model):
	industry=models.CharField(max_length=160)
	code=models.CharField(max_length=160)
	slug=models.SlugField()

	def  __unicode__ (self):
		return self.industry


class VisitorType(models.Model)
	visit_type=models.CharField(max_length=160)
	code=models.CharField(max_length=160)

	def  __unicode__ (self):
		return self.visitor_type

	class Meta:
		verbose_name_plural="Visitor Type"


class Visitor(models.Model):
	visitor_count=models.CharField(max_length=160)
	visitortype=models.ForeignKey(VisitorType)
	reporter=models.ForeignKey(Reporter)
	created_at=models.DateTimeField(auto_now_add=1)

	def  __unicode__ (self):
		return self.visitortype.visit_type


	class Meta:
		verbose_name_plural="Visitors"

"""	