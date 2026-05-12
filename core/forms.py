from django import forms
from django.forms import formset_factory
from .models import UniformOrder, UniformItem, SIZE_CHOICES


class UniformOrderForm(forms.ModelForm):
    class Meta:
        model = UniformOrder
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Alguma observação? (opcional)',
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm '
                         'focus:outline-none focus:ring-2 focus:ring-yellow-300 '
                         'bg-white text-gray-700 resize-none',
            }),
        }


class UniformOrderItemForm(forms.Form):
    uniform_item = forms.ModelChoiceField(
        queryset=UniformItem.objects.filter(available=True),
        label="Item",
        empty_label="Selecione um item",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm '
                     'focus:outline-none focus:ring-2 focus:ring-yellow-300 bg-white',
        }),
    )
    size = forms.ChoiceField(
        choices=[('', 'Tamanho')] + SIZE_CHOICES,
        label="Tamanho",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm '
                     'focus:outline-none focus:ring-2 focus:ring-yellow-300 bg-white',
        }),
    )
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        label="Qtd",
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm '
                     'focus:outline-none focus:ring-2 focus:ring-yellow-300 bg-white text-center',
            'min': '1',
            'max': '20',
        }),
    )


UniformOrderItemFormSet = formset_factory(
    UniformOrderItemForm,
    extra=1,
    min_num=1,
    validate_min=True,
)
