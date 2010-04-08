from django.db import models
from apps.locations.models import Location
from apps.reporters.models import Reporter

class FgmRescue(models.Model):
	activity_type=models.CharField(max_length=160)
	count=models.CharField(max_length=20)

	def  __unicode__ (self):
		return self.activity_type

	class Meta:
		verbose_name_plural="Rescued-FGM"


