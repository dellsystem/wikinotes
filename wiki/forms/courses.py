from django import forms
from django.utils.safestring import mark_safe

from wiki.models.courses import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('watchers', 'num_watchers', 'latest_activity')

    def clean(self):
        # Make sure we don't already have this course
        cleaned_data = super(CourseForm, self).clean()
        department = cleaned_data.get('department')
        number = cleaned_data.get('number')
        matching = Course.objects.filter(department=department, number=number)

        if matching.exists():
            course = matching[0]
            course_url = course.get_absolute_url()
            course_link = '<a href="%s">%s</a>' % (course_url, course)
            raise forms.ValidationError(mark_safe("The course you're trying to"
                " create already exists: %s." % course_link))

        return cleaned_data
