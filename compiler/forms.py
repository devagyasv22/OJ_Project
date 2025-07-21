from django import forms
from .models import CodeSubmission

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model =CodeSubmission
        fields=['language','code','input_data']
        widgets={
            'code': forms.Textarea(attrs={'rows': 10}),
            'input_data': forms.Textarea(attrs={'rows': 3}),
        }
