from django.db import models

class EventType(models.Model):
	event_type=models.CharField(max_length=160)

class Event(models.Model):
	attendees=models.CharField(max_length=160)
	event_date=models.DateTimeField(blank=True, null=True)

class Enterprise(models.Model):
	attendees=models.CharField(max_length=160)

class Industry(models.Model):
	industry=models.CharField(max_length=160)

class Visitor(models.Model):
	visitor_count=models.CharField(max_length=160)
	
	