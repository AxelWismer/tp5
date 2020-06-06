from django.shortcuts import render
from django.views import generic

from .forms import ParametersForm
from .iterador import Iteracion

class Colas(generic.FormView):
    form_class = ParametersForm
    template_name = 'colas/colas.html'

    def form_valid(self, form):
        desde = form.cleaned_data['desde']
        hasta = form.cleaned_data['hasta']
        ultimas_filas = form.cleaned_data['ultimas_filas']
        # Se genera el iterador con los parametros que indican que valores guardar
        it = Iteracion(
            desde=desde,
            hasta=hasta,
            ultimas_filas=ultimas_filas
        )
        # Se realizan las simulaciones requeridas

        it.calcular_iteracion(tiempo=int(form.cleaned_data['tiempo']))
        print(it.print_tabla(it.tabla))
        # Mostrar tabla
        # Divido la tabla en sus 2 partes
        context = {
            'tabla': it.tabla,
            # 'tabla_final': it.get_tabla_final(),
            # 'lotes_final': it.get_matrix(it.get_tabla_final()),
            'form': form}
        it.limpiar_salas()

        it.ordenar_tabla_final()
        tabla = it.tabla + it.tabla_final
        context['tabla'], context['num_lotes'] = it.get_matrix(tabla)
        tabla.insert(len(it.tabla), {})


        return render(self.request, template_name=self.template_name, context=context)
