from django import forms
from app.models import Tournament

class TournamentAdminForm(forms.ModelForm):
    class Meta:
        model = Tournament

    def clean_players(self):
        cleaned_data = self.cleaned_data['players']
        if len(cleaned_data)%2==1:
            raise forms.ValidationError(u'The number of players cannot be odd.')
        return cleaned_data
