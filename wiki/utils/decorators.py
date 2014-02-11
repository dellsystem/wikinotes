from django.http import Http404
from django.shortcuts import render


def show_object_detail(model, show_custom_404=False,
                       always_pass_groups=False):
    def wrapper(view):
        def new_view(request, **groups):
            filters = {}
            for group_name, field_name in model.url_fields.iteritems():
                # groups as in regex groups
                filters[field_name] = groups[group_name]

            try:
                instance = model.objects.get(**filters)
                kwargs = groups if always_pass_groups else {}
            except model.DoesNotExist:
                # If show_custom_404 is set, pass it None as the instance,
                # and pass the groups dictionary as well
                if show_custom_404:
                    instance = None
                    kwargs = groups
                else:
                    raise Http404

            # Call the function to obtain the context dictionary. If it returns
            # something else (say, a redirect object), just return that.
            context = view(request, instance, **kwargs)
            if type(context) is not dict:
                return context

            # Figure out the template name based on the function name
            parent_module = view.__module__.split('.')[-1]
            function_name = view.func_name
            template_filename = '%s/%s.html' % (parent_module,
                function_name)

            return render(request, template_filename, context)

        return new_view
    return wrapper
