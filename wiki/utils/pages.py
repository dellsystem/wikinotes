import inspect

from wiki.models import page_types as types


# A dictionary for reverse lookup of page type by the short name
# So, given "course-quiz", find the CourseQuiz object etc
page_types = {}
for name, obj in inspect.getmembers(types):
    if inspect.isclass(obj):
        # Because it returns a tuple. There is probably a better way of doing it but issubclass() doesn't work so don't try it
        if obj.__bases__ == (types.PageType,):
            page_types[obj.short_name] = obj()

page_type_choices = tuple([(name, obj.long_name) for name, obj in page_types.iteritems()])

