from django.db import models
from apps.reporters.models import Reporter
from apps.locations.models import Location


class Center(models.Model):
	name=models.CharField(max_length=160)
	location=models.ForeignKey(Location)
	code=models.CharField(max_length=30)

	def __unicode__ (self):
		return self.name

	class Meta:
		verbose_name="ECD Center"


class Child(models.Model):
	firstname=models.CharField(max_length=160)
	middlename=models.CharField(max_length=160)
	lastname=models.CharField(max_length=160)
	center=models.ForeignKey(Center)
	code=models.CharField(max_length=30,help_text="unique code to identify student")

	def __unicode__ (self):
		return self.firstname + ' ' + self.lastname

	class Meta:
		verbose_name="Child"
		
		
class Enrollment(models.Model):
	term=models.CharField(max_length=160)
	male_count=models.CharField(max_length=160)
	female_count=models.CharField(max_length=30)
	center=models.ForeignKey(Center)
	reporter=models.ForeignKey(Reporter)
	

	def __unicode__ (self):
		return self.center.name

	class Meta:
		verbose_name="Enrollment"
		

class ChildGrade(models.Model):
	child=models.ForeignKey(Child)
	grade=models.CharField(max_length=160)
	center=models.ForeignKey(Center)
	reporter=models.ForeignKey(Reporter)

	def __unicode__ (self):
		return self.child.firstname + ' ' + self.child.lastname

	class Meta:
		verbose_name="Child Term Grade"

	
class FundsRaised(models.Model):
	amount=models.CharField(max_length=160)
	center=models.ForeignKey(Center)
	reporter=models.ForeignKey(Reporter)


	def __unicode__ (self):
		return self.center.name

	class Meta:
		verbose_name="Child Term Grade"

	