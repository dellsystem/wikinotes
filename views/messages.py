from django.contrib.auth.decorators import login_required
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
            data['modes'] = ['inbox', 'outbox', 'compose']
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
            'message': message
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
        form = PrivateMessageForm()

    return {'form': form}
