from django import forms
from crispy_forms.helper import FormHelper


class ParametersForm(forms.Form):
    costo = forms.IntegerField(label='costo', initial=10, min_value=0)
    precio_venta = forms.IntegerField(label='precio de venta', initial=16, min_value=0)
    tiempo_reposicion = forms.IntegerField(label='tiempo de reposicion', initial=3, min_value=1)
    cant_a_reponer = forms.IntegerField(label='cantidad a reponer', initial=15, min_value=0)
    stock_inicial = forms.IntegerField(label='stock inicial', initial=15, min_value=0)
    vencimiento = forms.IntegerField(label='vencimiento', initial=2, min_value=1, required=False)
    cant_iteraciones = forms.IntegerField(label='cantidad de dias', min_value=1, initial=15)

    # Permite elegir si utlizar los numeros aleatorios del ejercicio o los random
    PSEUDO_CHOICES = ((True, 'Si'), (False, 'No'))
    pseudoaleatorio = forms.ChoiceField(label='Utilizar numeros del ejercicio?', choices=PSEUDO_CHOICES,
                                        initial=PSEUDO_CHOICES[0])
    recupero = forms.IntegerField(label='valor de recupero', initial=0, min_value=0)

    def __init__(self, *args, **kwargs):
        super(ParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False

class ParametersForm2(ParametersForm):
    costo = forms.IntegerField(label='costo', initial=13, min_value=0)
    vencimiento = forms.IntegerField(label='vencimiento', min_value=1, required=False)
    recupero = forms.IntegerField(label='valor de recupero', initial=11, min_value=0)
