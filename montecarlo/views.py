from django.shortcuts import render
from django.views import generic
from .montecarlo import Producto, ProductoConVencimiento, ProductoSinVencimiento
from .forms import ParametersForm, ParametersForm2
# Create your views here.

class Montecarlo(generic.FormView):
    form_class = ParametersForm
    template_name = 'montecarlo/forms/montecarlo.html'

    def form_valid(self, form):
        if form.cleaned_data['pseudoaleatorio'] == 'True':
            num_pseudoaleatorios = [0.94, 0.74, 0.62, 0.11, 0.17, 0.66, 0.54, 0.30, 0.69, 0.08,
           0.27, 0.13, 0.80, 0.10, 0.54, 0.60, 0.49, 0.78, 0.66, 0.44]
        else:
            num_pseudoaleatorios = []

        if form.cleaned_data['vencimiento'] is None:
            product = ProductoSinVencimiento(
                c=form.cleaned_data['costo'],
                p=form.cleaned_data['precio_venta'],
                tr=form.cleaned_data['tiempo_reposicion'],
                cr=form.cleaned_data['cant_a_reponer'],
                si=form.cleaned_data['stock_inicial'],
                r=form.cleaned_data['recupero'],
                num_pseudoaleatorios=num_pseudoaleatorios
            )
        else:
            product = ProductoConVencimiento(
                c=form.cleaned_data['costo'],
                p=form.cleaned_data['precio_venta'],
                tr=form.cleaned_data['tiempo_reposicion'],
                cr=form.cleaned_data['cant_a_reponer'],
                si=form.cleaned_data['stock_inicial'],
                # Se agrega 1 porque segun el enunciado ingresamos los dias que se vence despues de haber llegado
                # y en la libreria se consideria dias de vencimiento a partir de que llego
                v=form.cleaned_data['vencimiento'] + 1,
                num_pseudoaleatorios=num_pseudoaleatorios
            )
        iteraciones = form.cleaned_data['cant_iteraciones']
        ganancia = product.simular(iteraciones)

        context = {}
        context['ganancia'] = ganancia
        context['ganancia_media'] = round(ganancia / iteraciones, 2)
        context['form'] = form

        if len(product.tabla) >= 30:
            context['tabla'] = product.tabla[0:30]
            if len(product.tabla) >= 40:
                context['tabla_fin'] = product.tabla[-10:]
            else:
                context['tabla_fin'] = product.tabla[30:]
        else:
            context['tabla'] = product.tabla

        return render(self.request, template_name=self.template_name, context=context)


class Montecarlo2(Montecarlo):
    form_class = ParametersForm2