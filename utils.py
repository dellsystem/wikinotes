import inspect
from wiki.models import page_types as types
import os
import git
import datetime

# A dictionary for reverse lookup of page type by the short name
# So, given "course-quiz", find the CourseQuiz object etc
page_types = {}
for name, obj in inspect.getmembers(types):
	if inspect.isclass(obj):
		# Because it returns a tuple. There is probably a better way of doing it but issubclass() doesn't work so don't try it
		if obj.__bases__ == (types.PageType,):
			page_types[obj.short_name] = obj()

page_type_choices = tuple([(name, obj.long_name) for name, obj in page_types.iteritems()])

# Temporary, use wrapper library later
# Ignore special characters etc for now
class Git:
	def __init__(self, path_to_repo):
		print path_to_repo
		self.full_path = path_to_repo.strip('/') # don't need leading/trailing slashes
		try:
			os.makedirs(self.full_path)
		except OSError:
			pass
		# If the repository has not been created yet, create it
		# Yeah leads to race conditions or whatever but, whatever, deal with later
		if not os.path.exists("%s/.git" % self.full_path):
			os.system("cd \"%s\"; git init" % self.full_path)

	def add(self, filename):
		os.system("cd \"%s\"; git add \"%s\"" % (self.full_path, filename))

	# Commits all the staged files
	def commit(self, commit_message, username, email):
		# First escape quotation marks
		commit_message = commit_message.replace('"', '\\"')
		# If the comment is empty, fill it with the default ("Minor edit")
		if commit_message == '':
			commit_message = 'Minor edit'
		os.system('cd "%s"; git commit -m "%s" --author="%s <%s>"' % (self.full_path, commit_message, username, email))

		# Make sure something was actually committed - later

	def get_history(self):
		commits = []
		for commit in git.Repo(self.full_path).iter_commits():
			commit_dict = {
				'date': datetime.datetime.fromtimestamp(commit.committed_date),
				'message': commit.message,
				'author': commit.author,
			}
			commits.append(commit_dict)
		return commits
