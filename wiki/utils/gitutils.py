import os
import git
import gitdb
import datetime
from math import log

# Temporary, use wrapper library later
# Ignore special characters etc for now
class Git:
	def __init__(self, path_to_repo):
		print path_to_repo
		self.full_path = path_to_repo.strip('/') # don't need leading/trailing slashes
		try:
			os.makedirs(self.full_path)
		except OSError:
			print "WTF???"
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

	# Pass it the SHA1 hash etc
	# It's not like we'll ever need to use hash() anyway lol
	def get_commit(self, hash):
		repo = git.Repo(self.full_path)
		hexsha = gitdb.util.hex_to_bin(hash) # have to convert it to hex first or something
		commit = git.objects.commit.Commit(repo, hexsha)
		return commit

	def get_history(self):
		commits = []
		for commit in git.Repo(self.full_path).iter_commits():
			num_lines = commit.stats.total['lines']
			bar_width = int(log(num_lines)) * 20
			max_width = 100
			min_width = 20
			commit_dict = {
				'date': datetime.datetime.fromtimestamp(commit.committed_date),
				'message': commit.message[:70] + ' ...' if len(commit.message) > 70 else commit.message,
				'author': commit.author,
				'lines': num_lines,
				'url': 'commit/' + commit.hexsha,
				'undo_url': 'undo/' + commit.hexsha,
				'insertions': commit.stats.total['insertions'],
				'deletions': commit.stats.total['deletions'],
				'bar_width': min(bar_width, max_width) if bar_width > max_width else max(bar_width, min_width), # width in pixels of bar ... based on the number of lines
				'green_percent': (commit.stats.total['insertions'] * 100) / num_lines, # how much of this commit is insertions - int div
			}
			commits.append(commit_dict)
		return commits
