from django import forms

class VideoForm(forms.Form):
    video_link = forms.URLField(label='Video havolasini kiriting', max_length=200, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v='}))
