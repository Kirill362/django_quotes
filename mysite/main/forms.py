from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        if source and Quote.objects.filter(source=source).count() >= 3:
            self.add_error(
                'source',
                f"Нельзя добавлять больше 3-х цитат для одного источника: {source}"
            )
        return cleaned_data
