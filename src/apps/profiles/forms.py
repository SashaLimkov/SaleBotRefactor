from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(max_length=4000, widget=forms.Textarea)
