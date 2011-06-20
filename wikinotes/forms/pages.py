from django.forms import ModelForm, TypedChoiceField, CharField
from wikinotes.models.pages import Page, PageType
from wikinotes.utils.pages import *
from wikinotes.utils.semesters import get_possible_terms, get_possible_years

# The various forms
class PageForm(ModelForm):
	class Meta:
		model = Page
		fields = ('num_sections', 'subject')
        #widgets = {
        #    'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        #}
        # exclude = ('page_type', 'course_semester')
	
	subject = CharField(required=False)
	exam_type = TypedChoiceField(choices=get_possible_exams(), empty_value='', required=False)
	num_sections = TypedChoiceField(choices=get_possible_numbers(1, get_max_num_sections()), coerce=int)
	term = TypedChoiceField(choices=get_possible_terms())
	year = TypedChoiceField(choices=get_possible_years(2005), coerce=int)
	weekday = TypedChoiceField(choices=get_possible_weekdays(), empty_value='', required=False)
	# List all the months and days and just use Javascript to figure out which to show? Maybe?
	month = TypedChoiceField(choices=get_possible_months(), empty_value='', required=False)
	day = TypedChoiceField(choices=get_possible_numbers(1, 31), coerce=int, empty_value=0, required=False)
	
	# The commit message - will later be used in the history
	comment = CharField(required=False)

"""
class LectureNoteForm(ModelForm):
	class Meta:
		model = LectureNote
		# Determined within the view (whichever course page we're on etc)
		exclude = ('course')
	# 10 is not the hard limit - just makes it easier to choose at the beginning
	# The user can always select more later
	num_sections = TypedChoiceField(choices=get_possible_numbers(1, get_max_num_sections()), coerce=int)

class PastExamForm(ModelForm):
	class Meta:
		model = PastExam
		exclude = ('course')

class CourseQuizForm(ModelForm):
	class Meta:
		model = CourseQuiz
		exclude = ('course')
		
class VocabQuizForm(ModelForm):
	class Meta:
		model = VocabQuiz
		exclude = ('course')

class CourseSummaryForm(ModelForm):
	class Meta:
		model = CourseSummary
		exclude = ('course')
"""
