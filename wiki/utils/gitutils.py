import os
import git
import gitdb
import datetime
from subprocess import Popen,PIPE
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
			os.system("cd \"%s\"& git init" % self.full_path)

	def add(self, filename):
		os.system("cd \"%s\"& git add \"%s\"" % (self.full_path, filename))

	# Commits all the staged files
	def commit(self, commit_message, username, email):
		# First escape quotation marks
		commit_message = commit_message.replace('"', '\\"')
		# If the comment is empty, fill it with the default ("Minor edit")
		if commit_message == '':
			commit_message = 'Minor edit'
		os.system('cd "%s"& git commit -m "%s" --author="%s <%s>"' % (self.full_path, commit_message, username, email))

		# Make sure something was actually committed - later

	# Pass it the SHA1 hash etc
	# It's not like we'll ever need to use hash() anyway lol
	def get_commit(self, hash):
		repo = git.Repo(self.full_path)
		hexsha = gitdb.util.hex_to_bin(hash) # have to convert it to hex first or something
		commit = git.objects.commit.Commit(repo, hexsha)
		return commit

	# Pass it a commit object. Returns the commit object for the previous commit in the master branch
	def get_previous(self, this_commit):
		is_next = False
		for commit in git.Repo(self.full_path).iter_commits():
			if is_next:
				return commit
			else:
				is_next = this_commit.hexsha == commit.hexsha

	def get_latest_commit(self):
		command = "cd %s & git log --format=%%H -n 1" %(self.full_path)
		hash = Popen(command,shell=True,stdout=PIPE).communicate()[0].strip()
		return hash
		

	# If there is no diff, it'll return None, which is fine
	def get_diff(self, this_commit):
		previous = self.get_previous(this_commit)

		if previous:
			diff = previous.diff(this_commit.hexsha, create_patch=True)[0].diff
			diff_lines = diff.splitlines()[2:]
			sections = []
			previous_i = 0
			for i, line in enumerate(diff_lines):
				if line.startswith('@'):
					section_info = line.split(' ')
					section_before = section_info[1].split(',')
					section_after = section_info[2].split(',')

					num_lines_before = 0 if len(section_before) == 1 else section_before[1]
					num_lines_after = 0 if len(section_after) == 1 else section_after[1]
					first_line = max(0, int(section_after[0][1:]))
					sections.append({'first_line': first_line, 'lines_before': num_lines_before, 'lines_after': num_lines_after, 'start_index': i + 1})
					previous_i = i

			# Set the lines for each section
			# THIS IS THE ONLY WAY I COULD FIGURE OUT HOW TO DO IT
			# I'm sorry
			end_index = len(diff_lines)
			for i, section in enumerate(reversed(sections)):
				sections[-1-i]['lines'] = diff_lines[section['start_index']:end_index]
				end_index = section['start_index'] - 1

			return sections

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
