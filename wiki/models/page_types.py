# NOT ACTUALLY DJANGO MODELS
# Done this way because it's better than the 4 other possible ways (believe me I tried them all)
# Define all the page types here, and their short names
import re
""" HOW TO CREATE A NEW PAGE TYPE
	Following template files:
		- pages/#{short_name}/create.html
		- pages/#{short_name}/show.html
		- pages/#{short_name}/list.html
		- assets/img/pages/#{short_name}.png
		ALTHOUGH IF YOU HAVE CUSTOM NAMES YOU CAN OVERRIDE ANY OF THE RELEVANT METHODS, ETC
"""

class PageType:
	def is_subject_valid(self, subject):
		return True

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
		return 'pages/%s/list.html' % self.short_name

	def get_icon(self):
		return '/static/img/pages/%s.png' % self.short_name

	def get_create_url(self, course):
		return '%s/create/%s' % (course.url(), self.short_name)

class LectureNote(PageType):
	short_name = 'lecture-notes'
	long_name = 'Lecture notes'
	description = 'Notes from a lecture given by a specific professor on a specific date'

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

	def format(self, content):
		# Replace every \ between $$($) and $$($) with \\
		# Fuck it. Later.
		data = {
			'content': '\n'.join(content),
		}
		return data

class PastExam(PageType):
	short_name = 'past-exam'
	long_name = 'Past exam'
	description = 'Student-made solutions to a past exam'

	def get_kwargs(self, data):
		term = data['term']
		year = data['year']
		exam_type = data['exam_type']
		version = data['version'] # figure this out later (multiple versions of an exam?)
		title = "%s %s %s" % (term, year, exam_type)
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		slug = exam_type.lower()
		return {'title': title, 'link': data['link'], 'slug': slug}

class CourseSummary(PageType):
	short_name = 'summary'
	long_name = 'Course summary'
	description = 'Anything that doesn\'t fit in the other categories'

	def get_kwargs(self, data):
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		slug = data['subject'].lower().replace(' ', '-')
		return {'subject': data['subject'], 'link': data['link'], 'slug': slug}

class VocabQuiz(PageType):
	short_name = 'vocab-quiz'
	long_name = 'Vocabulary quiz'
	description = 'For memorising terms etc'

	def get_kwargs(self, data):
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		slug = data['subject'].lower().replace(' ', '-')
		return {'subject': data['subject'], 'slug': slug}

class CourseQuiz(PageType):
	short_name = 'course-quiz'
	long_name = 'Multiple choice quiz'
	description = 'A quiz for testing your knowledge'

	# Data is the request.POST dictionary
	def get_kwargs(self, data):
		# If title is empty, it will appear in the form [PageType.long_name] - [subject] (Semester)
		# Otherwise, [PageType.long_name] - [title]
		slug = data['subject'].lower().replace(' ', '-')
		return {'subject': data['subject'], 'slug': slug}

	# Return a data dictionary, all self-contained etc
	def format(self, content):
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
