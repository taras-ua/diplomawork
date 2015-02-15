from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django import forms

import app.controllers.main as controller


class GraphForm(forms.Form):
    MODEL_CHOICES = (('simple', 'Simple random graph',), ('bollobas-riordan', 'Bollobás–Riordan model',))
    model = forms.ChoiceField(widget=forms.Select, choices=MODEL_CHOICES)
    nodes = forms.IntegerField(min_value=0)
    subnodes = forms.IntegerField(min_value=0)


def home(request):
    if request.method == 'GET':
        form = GraphForm(initial={'model': 'bollobas-riordan'})
        return render_to_response('home.html', {'form': form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            return redirect(controller.build_request(form))
        else:
            return HttpResponse(status=500)


def graph(request):
    graph_json = controller.get_graph(request)
    return render_to_response('graph.html', {'graph': graph_json}, context_instance=RequestContext(request))
