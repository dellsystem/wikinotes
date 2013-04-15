from django import forms

from wiki.models.users import PrivateMessage


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ('recipient', 'subject', 'message')

    def __init__(self, *args, **kwargs):
        super(PrivateMessageForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['class'] = 'xxlarge'
        self.fields['message'].widget.attrs['class'] = 'xxlarge'
        self.fields['recipient'].widget.attrs['class'] = 'chosen'
