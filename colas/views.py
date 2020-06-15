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
            capcacidades=[form.cleaned_data['capacidad_A'], form.cleaned_data['capacidad_B'],
                          form.cleaned_data['capacidad_C'], form.cleaned_data['capacidad_D']],
            desde=desde,
            hasta=hasta,
            ultimas_filas=ultimas_filas
        )
        # Se realizan las simulaciones requeridas

        it.calcular_iteracion(tiempo=int(form.cleaned_data['tiempo']))
        # print(it.print_tabla(it.tabla))
        # Mostrar tabla
        # Divido la tabla en sus 2 partes
        visitantesA , visitantesB, visitantesC, visitantesD = it.get_visitantes_por_sala()
        colaA, colaB, colaC, colaD = it.get_numero_lotes_encolados()
        lotesA, lotesB, lotesC, lotesD = it.get_numero_lotes()
        #tiempoA, tiempoB, tiempoC, tiempoD = it.get_tiempo_medio_recorrido()
        tiempoA, tiempoB, tiempoC, tiempoD = it.get_tiempo_espera_cola()
        pctjeA,pctjeB,pctjeC,pctjeD = it.calcular_porcentaje_lotes_cola()
        context = {
            'tabla': it.tabla,
            'pctjeA': pctjeA,
            'pctjeB': pctjeB,
            'pctjeC': pctjeC,
            'pctjeD': pctjeD,
            'tiempoA': tiempoA,
            'tiempoB': tiempoB,
            'tiempoC': tiempoC,
            'tiempoD': tiempoD,
            'visitantesA': visitantesA,
            'visitantesB': visitantesB,
            'visitantesC': visitantesC,
            'visitantesD': visitantesD,
            # 'tabla_final': it.get_tabla_final(),
            # 'lotes_final': it.get_matrix(it.get_tabla_final()),
            'form': form}

        # it.ordenar_tabla_final()
        tabla = it.tabla + it.tabla_final

        it.limpiar_salas()

        context['tabla'], context['num_lotes'] = it.get_matrix(tabla)
        tabla.insert(len(it.tabla), {})
        tabla.insert(len(it.tabla), {})


        return render(self.request, template_name=self.template_name, context=context)
