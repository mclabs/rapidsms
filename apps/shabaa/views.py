from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
from django.template import RequestContext
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from rapidsms.webui.utils import render_to_response
from django.contrib.auth.decorators import permission_required
from apps.shabaa.models import *
from django.utils import simplejson 

from pygooglechart import SimpleLineChart, Axis, PieChart2D, PieChart3D,StackedVerticalBarChart
from datetime import datetime, timedelta
from django.db.models import Count



@permission_required('shabaa.can_view')
def index (req):
	activities=Activity.objects.order_by("created_at")
	enterprises=Enterprise.objects.order_by("created_at")
	locs=Location.objects.all();
	return render_to_response(req,'shabaa/index.html',{"activities":activities,"enterprises":enterprises,"locs":locs});

	
@permission_required('shabaa.can_view')
def map (req):
	locs=Location.objects.all();
	activities=Activity.objects.all()
	enterprises=Enterprise.objects.order_by("created_at")
	return render_to_response(req,'shabaa/map.html',{"activities":activities,"locs":locs,"enterprises":enterprises});


def to_json (req):
	locations=Location.objects.all()
	loc=[]
	for location in locations:
		loc.append({"latitude":str(location.latitude),"longitude":str(location.longitude),"city":location.name})
	data=simplejson.dumps(loc, indent=4) 		
	return HttpResponse(data, mimetype='application/javascript')

@permission_required('shabaa.can_view')
def reports (req):
	return render_to_response(req,'shabaa/reports.html');

def entries_graph ():
	# Create a chart object of 250x100 pixels
	chart = PieChart3D(250, 100)

	# Add some data
	male_count=ShabaaReporter.objects.annotate(num_males=Count('id')).filter(gender='M')
	female_count=ShabaaReporter.objects.annotate(num_females=Count('id')).filter(gender='F')
	if not male_count:
		#male_count[0].num_males=0
		male_count_data=0
	else:
		male_count_data=male_count[0].num_males
	if not female_count:
		female_count_data=0
	else:
		female_count_data=female_count[0].num_females
		
	
	
	chart.add_data([male_count_data, female_count_data])

	# Assign the labels to the pie data
	chart.set_pie_labels(['Male', 'Female'])

	# Print the chart URL
	print chart.get_url()

	# Download the chart
	chart.download('apps/shabaa/static/graphs/pie-hello-world.png')

	return 'pie-hello-world.png'


def random_color(color=''):
	from random import random

	color = (random(0,255),random(0,255),random(0,255))
	return color

def activities_bar ():
	chart_name="activities_created.png"
	# Create a chart object of 250x100 pixels
	chart = StackedVerticalBarChart(440,300,x_range=(0, 35))
	# Assign the labels to the pie data
	labels=[]
	data=[]
	legend={}
	act=ActivityType.objects.all()
	for a in act :
		labels.append(a.code)
		legend[a.activity_type]=True
	# Add some data
	#colors = [random_color() for x in legend.keys()] 
	chart.set_colours(['0091C7','0591C7'])
	chart.add_data([10,12])
	chart.add_data([0,0])
	chart.set_legend(legend.keys())
	chart.set_bar_width(30)
	chart.set_axis_labels(Axis.BOTTOM,labels)
	chart.set_axis_labels(Axis.BOTTOM, ['','Activity Type', ''])
	chart.set_axis_labels(Axis.LEFT, ['', 5, 10,15,20,35])

	print chart.get_url()
	chart.download('apps/shabaa/static/graphs/' + chart_name)

	return chart_name
	
def enterprises_created_bar ():
	chart_name="enterprises_created.png"
	# Create a chart object of 250x100 pixels
	chart = StackedVerticalBarChart(440,300,x_range=(0, 35))
	# Assign the labels to the pie data
	labels=[]
	data=[]
	legend={}
	industry=Industry.objects.all()
	for i in industry :
		labels.append(i.code)
		legend[i.industry]=True
	# Add some data
	#colors = [random_color() for x in legend.keys()] 
	chart.set_colours(['0091C7','0591C7'])
	chart.add_data([10,12])
	chart.add_data([0,0])
	chart.set_legend(legend.keys())
	chart.set_bar_width(30)
	chart.set_axis_labels(Axis.BOTTOM,labels)
	chart.set_axis_labels(Axis.BOTTOM, ['','Industry Code', ''])
	chart.set_axis_labels(Axis.LEFT, ['', 5, 10,15,20,35])

	print chart.get_url()
	chart.download('apps/shabaa/static/graphs/' + chart_name)

	return chart_name

def enterprises_graph(num_days=14):
	chart_name="enterprises.png"
	# its a beautiful day
	today = datetime.today().date()

	# step for x axis
	step = timedelta(days=1)

	# empties to fill up with data
	counts = []
	dates = []

	# only get last two weeks of entries 
	day_range = timedelta(days=num_days)
	entries = Enterprise.objects.filter(
			created_at__gt=(today	- day_range))
	
	# count entries per day
	for day in range(num_days):
		count = 0
		d = today - (step * day)
		for e in entries:
			if e.created_at.day == d.day:
				count += 1
		dates.append(d.day)
		counts.append(count)
    
    	line = SimpleLineChart(440, 100, y_range=(0, 100))
	line.add_data(counts)
	line.set_axis_labels(Axis.BOTTOM, dates)
	line.set_axis_labels(Axis.BOTTOM, ['','Date', ''])
	line.set_axis_labels(Axis.LEFT, ['', 5, 10])
	line.set_colours(['0091C7'])
	line.download('apps/shabaa/static/graphs/' + chart_name)
	return chart_name


def graphs (req):
	sample=entries_graph()
	enterprises=enterprises_graph()
	ent_created=enterprises_created_bar()
	act_reported=activities_bar()
	return render_to_response(req,'shabaa/graphs.html',{"sample":sample,"enterprises":enterprises,
	"ent_created":ent_created,"act_reported":act_reported});
