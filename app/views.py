from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django import forms
import app.controllers.main as controller


class GraphForm(forms.Form):
    MODEL_CHOICES = (('simple', 'Simple random directed multigraph'), ('bollobas-riordan', 'Bollobás–Riordan model'), ('new-model', 'New Model'))
    model = forms.ChoiceField(widget=forms.Select, choices=MODEL_CHOICES)
    nodes = forms.IntegerField(min_value=0)
    subnodes = forms.IntegerField(min_value=0, required=False)
    probability = forms.FloatField(min_value=0, max_value=1, required=False)


class ProbabilityForm(forms.Form):
    SPEC_CHOICES = (('edges', 'Total number of edges'),)# ('degree', 'Degree of single node'))
    spec = forms.ChoiceField(widget=forms.Select, choices=SPEC_CHOICES)
    edges = forms.IntegerField(min_value=1)
    degree = forms.IntegerField(min_value=1, required=False)
    time = forms.IntegerField(min_value=1)


def home(request):
    gform = GraphForm(initial={'model': 'bollobas-riordan'})
    pform = ProbabilityForm(initial={'spec': 'edges'})
    return render_to_response('home.html', {'gform': gform, 'pform': pform}, context_instance=RequestContext(request))



def graph(request):
    if request.method == 'GET':
        graph_json, matrix, eig, name, data = controller.get_graph(request)
        return render_to_response('graph.html', {'nodes': graph_json['nodes'],
                                                 'edges': graph_json['links'],
                                                 'matrix': matrix, 'eigenvalues': eig,
                                                 'model': name, 'modeldata': data},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            return redirect(controller.build_graph_request(form))
        else:
            return HttpResponse(status=500)


def probabilities(request):
    if request.method == 'GET':
        spec, spec_data, x, y, init_degree = controller.get_probabilities(request)
        return render_to_response('probabilities.html', {'spec': spec, 'specdata': spec_data,
                                                         'x': x, 'y': y, 'init_degree': init_degree},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = ProbabilityForm(request.POST)
        if form.is_valid():
            return redirect(controller.build_probabilities_request(form))
        else:
            return HttpResponse(status=500)

