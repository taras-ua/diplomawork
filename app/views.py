from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django import forms
import app.controllers.main as controller
import math


class GraphForm(forms.Form):
    MODEL_CHOICES = (('erdos-renyi', 'Erdős–Rényi model'), ('bollobas-riordan', 'Bollobás–Riordan model'), ('new-model', 'Model of forgetting'))
    model = forms.ChoiceField(widget=forms.Select, choices=MODEL_CHOICES)
    nodes = forms.IntegerField(min_value=1)
    subnodes = forms.IntegerField(min_value=1, required=False)
    initial_weight = forms.FloatField(min_value=math.ldexp(1.0, -53), required=False)
    forget_coef = forms.FloatField(min_value=math.ldexp(1.0, -53), required=False)
    probability = forms.FloatField(min_value=0, max_value=1, required=False)


def home(request):
    gform = GraphForm(initial={'model': 'erdos-renyi'})
    return render_to_response('home.html', {'gform': gform}, context_instance=RequestContext(request))



def graph(request):
    if request.method == 'GET':
        graph_json, degrees, fractions, degreebynode, matrix, name, data, direct, diameter, nodes, edges, subnodes = controller.get_graph(request)
        return render_to_response('graph.html', {'nodes': graph_json['nodes'],
                                                 'edges': graph_json['links'],
                                                 'nodesnumber': nodes,
                                                 'edgesnumber': edges,
                                                 'directed': direct,
                                                 'diameter': diameter,
                                                 'degrees': degrees,
                                                 'fractions': fractions,
                                                 'degreebynode': degreebynode,
                                                 'matrix': matrix,
                                                 'model': name, 'modeldata': data,
                                                 'subnodes': subnodes},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            return redirect(controller.build_graph_request(form))
        else:
            return HttpResponse(status=500)

