from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from wiki.forms.messages import PrivateMessageForm
from wiki.models.users import PrivateMessage


class ViewMessage(Exception):
    def __init__(self, message_id):
        self.message_id = message_id


def base_view(function):
    @login_required
    def inner_view(request, *args, **kwargs):
        name = function.__name__
        template_file = 'messages/%s.html' % name
        try:
            data = function(request, *args, **kwargs)
            data['this_mode'] = name
            data['title'] = "Private messages (%s)" % name
            modes = ['inbox', 'outbox', 'compose']
            data['modes'] = [(mode, 'messages_%s' % mode) for mode in modes]
            return render(request, template_file, data)
        except PermissionDenied:
            return redirect('messages_inbox')
        except ViewMessage, e:
            return redirect('messages_view', message_id=e.message_id)

    return inner_view


@base_view
def inbox(request):
    return {
        'messages': request.user.received_messages.all(),
        'num_new': request.user.received_messages.new().count(),
    }


@base_view
def view(request, message_id):
    message = get_object_or_404(PrivateMessage, pk=message_id)

    if request.user == message.sender or request.user == message.recipient:
        if not message.is_read and request.user == message.recipient:
            message.is_read = True
            message.save()

        return {
            'message': message,
            'show_reply': request.user == message.recipient,
        }
    else:
        # Trying to view someone else's message ... return to inbox
        raise PermissionDenied


@base_view
def outbox(request):
    return {
        'messages': request.user.sent_messages.all()
    }


@base_view
def compose(request):
    if request.method == 'POST':
        message = PrivateMessage()
        form = PrivateMessageForm(request.POST, instance=message)
        if form.is_valid():
            message.sender = request.user
            form.save()
            raise ViewMessage(message.id)
    else:
        message = PrivateMessage()

        # If we want to send a message to a specific person
        recipient_name = request.GET.get('to', '')
        try:
            message.recipient = User.objects.get(username__iexact=recipient_name)
        except User.DoesNotExist:
            pass

        # Pre-filled subject (reply to)
        reply_to = request.GET.get('reply_to', '')
        if reply_to:
            message.subject = 'Re: %s' % reply_to

        form = PrivateMessageForm(instance=message)

    return {'form': form}
