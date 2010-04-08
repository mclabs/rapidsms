from django.db import models
from apps.reporters.models import Reporter
from apps.locations.models import Location

class Permissions(models.Model):
    '''This is a fake model that has nothing in it, because
       django expects all app-level permissions to be in
       a model'''
    
    class Meta:
        # the permission required for this tab to display in the UI
        permissions = (
            ("can_view", "Can view"),
        )

class Farmer(Reporter):
	class Meta:
		verbose_name= "Farmer"

	def __unicode__ (self):
		return self.firstname + " " + self.lastname


class Farm(models.Model):
	farmname=models.CharField(max_length=160)
	description=models.TextField(help_text="Brief Description of Farm")
	location=models.ForeignKey(Location)
	farmer=models.ForeignKey(Farmer)

	class Meta:
		verbose_name= "Farm"

	def __unicode__ (self):
		return self.farmname


class Crop(models.Model):
	crop=models.CharField(max_length=100, help_text="Name of crop")
	code=models.CharField(max_length=30, unique=True)

	class Meta:
		verbose_name="Farm Crop"

	def __unicode__ (self):
		return self.crop
		
'''
class CropSales(models.Model):
	reporter=models.ForeignKey(Reporter)
	class Meta:
		verbose_name="Crop Sales"
		

class FarmersCount(models.Model):
	male_farmers=models.CharField(max_length=30,help_text="Number of male farmers")
	female_farmers=models.CharField(max_length=30,help_text="Number of female farmers")
	reporter=models.ForeignKey(Reporter)
	class Meta:
		verbose_name="Number of Farmers by Gender"


class Visitor(models.Model):
	visitor_count=models.CharField(max_length=20,help_text="Number of visitors to each farm")
	reporter=models.ForeignKey(Reporter)
	class Meta:
		verbose_name="Farm Visitors"

'''

	
		

