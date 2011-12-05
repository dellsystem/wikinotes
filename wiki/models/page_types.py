# NOT ACTUALLY DJANGO MODELS
# Done this way because it's better than the 4 other possible ways (believe me I tried them all)
# Define all the page types here, and their short names
import re
from django.template.defaultfilters import slugify
from wiki.utils.constants import terms, years, exam_types

""" HOW TO CREATE A NEW PAGE TYPE
	Following template files:
		- pages/#{short_name}/create.html
		- pages/#{short_name}/show.html
		- pages/#{short_name}/list.html
		- assets/img/pages/#{short_name}.png
		ALTHOUGH IF YOU HAVE CUSTOM NAMES YOU CAN OVERRIDE ANY OF THE RELEVANT METHODS, ETC
"""

class PageType:
	# Defaults - override if necessary
	uneditable_fields = ['semester', 'subject']
	editable_fields = ['professor', 'link']

	# Wrapper around short_name basically
	def get_form_template(self):
		return 'pages/%s/create_form.html' % self.short_name

	def get_help_template(self):
		return 'pages/%s/create_help.html' % self.short_name

	# For showing ONE page of this type
	def get_show_template(self):
		return 'pages/%s/show.html' % self.short_name

	# For showing all the pages of this type (on a per-course level)
	def get_list_template(self):
		return 'pages/%s/list' % self.short_name

	def get_list_header(self):
		return self.get_list_template() + '_header.html'

	def get_list_body(self):
		return self.get_list_template() + '_body.html'

	def get_icon(self):
		return '/static/img/pages/%s.png' % self.short_name

	def get_create_url(self, course):
		return '%s/create/%s' % (course.get_url(), self.short_name)

	@staticmethod
	def get_field_templates(fields):
		return ['pages/%s_field.html' % field for field in fields]

	def get_editable_fields(self):
		return self.get_field_templates(self.editable_fields)

	def get_uneditable_fields(self):
		return self.get_field_templates(self.uneditable_fields)

	# The simplest version, override if necessary
	def format(self, content):
		data = {
			'content': '\n'.join(content),
		}
		return data

	def find_errors(self, data):
		validators = self.get_validators(data) + [
			(data['term'] in terms, 'Invalid term'),
			(int(data['year']) in years, 'Invalid year'),
		]

		error = False
		errors = []

		for validator in validators:
			if not validator[0]:
				error = True
				errors.append(validator[1])

		if error:
			return errors
		else:
			return []

class LectureNote(PageType):
	short_name = 'lecture-notes'
	long_name = 'Lecture notes'
	description = 'Notes from a lecture given by a specific professor on a specific date'
	uneditable_fields = ['semester', 'date']
	# Subject IS editable in this case only because it's not part of the slug
	editable_fields = ['subject', 'professor', 'link']
	# If you have other fields that have not yet been created, make the template file in the template dir / pages / blah_field.html

	def get_kwargs(self, data):
		weekday = data['date_weekday']
		month = data['date_month']
		date = data['date_date']
		year = data['year']
		title = "%s, %s %s, %s" % (weekday.title(), month.title(), date, year)
		slug = "%s-%s-%s" % (weekday, month, date)
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		professor = None # for now, from data['professor']
		return {'title': title, 'subject': data['subject'], 'link': data['link'], 'professor': professor, 'slug': slug}

	def get_validators(self, data):
		return [
			#(len(data['subject']) > 0, 'Invalid subject'),
		]

class PastExam(PageType):
	short_name = 'past-exam'
	long_name = 'Past exam'
	description = 'Student-made solutions to a past exam'
	uneditable_fields = ['semester', 'exam']
	editable_fields = ['professor', 'link']

	def get_kwargs(self, data):
		term = data['term']
		year = data['year']
		exam_type = data['exam_type']
		title = "%s %s %s" % (term.title(), year, exam_type.title())
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		slug = exam_type
		return {'title': title, 'link': data['link'], 'slug': slug}

	def get_validators(self, data):
		return [
			(data['exam_type'] in exam_types, 'Invalid exam type'),
		]

class CourseSummary(PageType):
	short_name = 'summary'
	long_name = 'Course summary'
	description = 'Anything that doesn\'t fit in the other categories'

	def get_kwargs(self, data):
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		return {'subject': data['subject'], 'link': data['link'], 'slug': slugify(data['subject'])}

	def get_validators(self, data):
		return [
			(len(data['subject']) > 0, 'Invalid subject'),
		]

class VocabList(PageType):
	short_name = 'vocab-list'
	long_name = 'Vocabulary list'
	description = 'For memorising terms etc'

	def get_kwargs(self, data):
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		return {
			'subject': data['subject'],
			'slug': slugify(data['subject']),
		}

	def get_validators(self, data):
		return [
			(len(data['subject']) > 0, 'Invalid subject'),
		]

class CourseQuiz(PageType):
	short_name = 'course-quiz'
	long_name = 'Multiple choice quiz'
	description = 'A quiz for testing your knowledge'

	# Data is the request.POST dictionary
	def get_kwargs(self, data):
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		return {'subject': data['subject'], 'slug': slugify(data['subject'])}

	def get_validators(self, data):
		return [
			(len(data['subject']) > 0, 'Invalid subject'),
		]

	# Return a data dictionary, all self-contained etc
	def format(self, content):
		try:
			data = {
				'questions': []
			}
			# Assume it's properly formatted
			number = 1
			question = {'heading': '', 'question': '', 'choices': [], 'correct': -1, 'answer': '', 'number': 1}
			choice_number = 0
			for line in content:
				if line.strip() == '': # stupid fucking carriage returns ???
					# New question
					question['heading'] = question['heading'].strip() # do it here just bcuz
					data['questions'].append(question)
					number += 1
					question = {'heading': '', 'question': '', 'choices': [], 'correct': -1, 'answer': '', 'number': number}
					choice_number = 0
				else:
					if line[:2] == '* ':
						question['question'] = line[2:].strip()
					elif line[:2] == '- ':
						question['choices'].append({'text': line[2:].strip(), 'number': choice_number})
						choice_number += 1
					elif line[:2] == '+ ':
						question['choices'].append({'text': line[2:].strip(), 'number': choice_number})
						choice_number += 1
						question['correct'] = len(question['choices']) - 1
					elif line[:2] == '? ':
						question['answer'] = line[2:].strip()
					else:
						question['heading'] += line
			question['heading'] = question['heading'].strip() # do it here just bcuz
			data['questions'].append(question)
			return data
		except: # except what???
			return None
