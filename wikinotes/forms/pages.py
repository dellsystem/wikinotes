from django.forms import ModelForm
from wikinotes.models.pages import *

# The various forms

class LectureNoteForm(ModelForm):
	class Meta:
		model = LectureNote
		# Determined within the view (whichever course page we're on etc)
		exclude = ('course')

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
