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

class Coordinator(Reporter):
	organisation=models.CharField(max_length=160,help_text="Organisation the coordinator represents")
	mobile_number=models.CharField(max_length=20)
	class Meta:
		verbose_name= "Coordinator"

	def __unicode__ (self):
		return "%s %s"%(self.firstname,self.lastname)

class Farmer(models.Model):
	firstname=models.CharField(max_length=100)
	


class Farm(models.Model):
	farmname=models.CharField(max_length=160)
	description=models.TextField(help_text="Brief Description of Farm")
	location=models.ForeignKey(Location)
	code=models.CharField(max_length=10,unique=True,help_text="Unique code to identify each farm")
	farmer=models.ForeignKey(Farmer,null=True,blank=True)

	class Meta:
		verbose_name= "Farm"

	def __unicode__ (self):
		return self.farmname


class Crop(models.Model):
	crop=models.CharField(max_length=100, help_text="Name of crop")
	code=models.CharField(max_length=30, unique=True,help_text="Unique code to identify each crop e.g. MZ for Maize")

	class Meta:
		verbose_name="Farm Crop"

	def __unicode__ (self):
		return self.crop

class CropSales(models.Model):
	farm=models.ForeignKey(Farm)
	crop=models.ForeignKey(Crop)
	weight=models.CharField(max_length=30)
	price=models.CharField(max_length=30)
	coordinator=models.ForeignKey(Coordinator)
	class Meta:
		verbose_name= "Cop Sales"


class CropHarvests(models.Model):
	farm=models.ForeignKey(Farm)
	crop=models.ForeignKey(Crop)
	weight=models.CharField(max_length=30)
	coordinator=models.ForeignKey(Coordinator)

	class Meta:
		verbose_name= "Crop Harvests"
