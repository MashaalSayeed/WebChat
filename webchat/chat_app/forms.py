from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Room, Message


class CreateRoomForm(forms.ModelForm):
    name = forms.SlugField(max_length=30, min_length=3,
        widget=forms.TextInput(attrs={'class':'form-control col-md-9', 'placeholder': 'Enter Room Name'}))

    class Meta:
        model = Room
        fields = ('name', )


class JoinRoomForm(forms.Form):
    invite = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-md-9', 'placeholder': 'Enter Invite ID'}))
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_invite(self):
        invite = self.cleaned_data['invite']

        try:
            room = Room.objects.get(invite=invite)
        except:
            raise forms.ValidationError(_("Invalid invite code"))
        
        if room.users.filter(pk=self.user.pk).exists():
            raise forms.ValidationError(_('You have already joined this room'))

        return invite


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget = forms.TextInput(attrs={'class': 'write_msg', 'placeholder': 'Type a message'})
