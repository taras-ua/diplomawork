from django.shortcuts import render_to_response
from django.template import RequestContext

import app.controllers.main as controller


def home(request):
    graph_json = controller.d3_bollobas_riordan(10, 3)
    return render_to_response('home.html', {'graph': graph_json},
                          context_instance=RequestContext(request))