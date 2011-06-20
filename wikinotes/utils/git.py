# Abstraction layer to make it easier to use git etc
# We don't need all of git's functionality, hence just a few methods instead of using an existing python wrapper
import os

class Git:
	# Relative to the content/ directory
	# Make the directory name configurable somewhere later
	def __init__(self, path_to_repo):
		self.full_path = 'content/' + path_to_repo.strip('/') # don't need leading/trailing slashes
		# If the repository has not been created yet, create it
		# Yeah leads to race conditions or whatever but, whatever, deal with later
		if not os.path.exists("%s/.git" % self.full_path):
			os.system("cd %s; git init" % self.full_path)
	
	# Stages the file (relative to the repository path)
	def add(self, filename):
		os.system("cd %s; git add %s" % (self.full_path, filename))
	
	# Commits all the staged files
	def commit(self, commit_message):
		# First escape quotation marks
		commit_message = commit_message.replace('"', '\\"')
		# If the comment is empty, fill it with the default ("Minor edit")
		if commit_message == '':
			commit_message = 'Minor edit'
		os.system('cd %s; git commit -m "%s"' % (self.full_path, commit_message))
		
		# Make sure something was actually committed - later
