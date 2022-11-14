from django import forms

from patients.models import PatientCard, ExaminationNote


class AddCardForm(forms.ModelForm):
    class Meta:
        model = PatientCard
        fields = '__all__'
        labels = {
            'full_name': 'Повне ім\'я',
            'home_address': 'Адреса',
            'date_of_birth': 'Дата народження'
        }
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(AddCardForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'field-value'


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = ExaminationNote
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }


class EditNoteForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
