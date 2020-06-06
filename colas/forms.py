from django import forms
from crispy_forms.helper import FormHelper

class ParametersForm(forms.Form):
    desde = forms.IntegerField(label='desde', initial=0, min_value=0)
    hasta = forms.IntegerField(label='hasta', initial=20, min_value=0)
    ultimas_filas = forms.IntegerField(label='ultimas filas', initial=10, min_value=0)
    tiempo = forms.IntegerField(label='tiempo', initial=60, min_value=0, max_value=1000)

    def __init__(self, *args, **kwargs):
        super(ParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.form_tag = False