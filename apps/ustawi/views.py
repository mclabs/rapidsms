from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseServerError
from django.template import RequestContext
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from rapidsms.webui.utils import render_to_response
from django.contrib.auth.decorators import permission_required


@permission_required('ustawi.can_view')
def index (req):
	return render_to_response(req,'ustawi/index.html');


@permission_required('ustawi.can_view')
def map(req):
	return render_to_response(req,'ustawi/map.html');
		