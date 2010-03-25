from django.db import models
from apps.location import Location


class Organisation(models.Model):
	name=models.CharField(max_length=160)

	def __unicode__ (self):
		return self.name
		

class School(models.Model):
	name=models.CharField(max_length=160)
	location=models.ForeignKey(Location)

	def __unicode__ (self):
		return self.name

class Student(models.Model):
	firstname=models.CharField(max_length=160)
	middlename=models.CharField(max_length=160)
	lastname=models.CharField(max_length=160)
	student=models.ForeignKey(School)
	code=models.CharField(max_length=30,help_text="unique code to identify student")

	def __unicode__ (self):
		return self.firstname + ' ' + self.lastname
		


	
	