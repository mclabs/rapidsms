from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
from django.template import RequestContext
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from rapidsms.webui.utils import render_to_response


def index (req):
	return render_to_response(req,'ecd/index.html');



def map(req):
	return render_to_response(req,'ecd/map.html');
		