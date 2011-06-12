from django.forms import ModelForm, TypedChoiceField
from wikinotes.models.pages import *
from wikinotes.utils.pages import get_possible_numbers

# The various forms

class LectureNoteForm(ModelForm):
	class Meta:
		model = LectureNote
		# Determined within the view (whichever course page we're on etc)
		exclude = ('course')
	# 10 is not the hard limit - just makes it easier to choose at the beginning
	# The user can always select more later
	num_sections = TypedChoiceField(choices=get_possible_numbers(1, 10), coerce=int)

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
