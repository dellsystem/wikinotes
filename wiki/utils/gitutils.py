import datetime
from math import log
from os import makedirs, environ

import git
import gitdb


class NoChangesError(Exception):
    pass


class Git:
    def __init__(self, path_to_repo):
        self.full_path = path_to_repo.strip('/') # don't need leading/trailing slashes
        try:
            makedirs(self.full_path)

            # Initialise the repository (if it doesn't already exist)
            git.Repo.init(self.full_path)
        except OSError:
            # It already exists, that's fine
            pass

        self.repo = git.Repo(self.full_path)

    # Adds and commits content.md
    def commit(self, commit_message, username, email):
        # Only commits it if there was a change; otherwise, raises an error
        environ['GIT_AUTHOR_NAME'] = username # no other way to do this lol

        # untracked_files is true so that even the first time it will work
        if self.repo.is_dirty(untracked_files=True):
            self.repo.index.add(["content.md"])
            self.repo.index.commit(commit_message)
        else:
            raise NoChangesError

    # Pass it the SHA1 hash etc
    # It's not like we'll ever need to use hash() anyway lol
    def get_commit(self, hash):
        hexsha = gitdb.util.hex_to_bin(hash) # have to convert it first
        commit = git.objects.commit.Commit(self.repo, hexsha)
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
        return self.repo.head.commit.hexsha

    # If there is no diff, it'll return None, which is fine
    def get_diff(self, this_commit):
        previous = self.get_previous(this_commit)

        if previous:
            word_diff = {"word-diff":"porcelain"}
            diff = previous.diff(this_commit.hexsha, create_patch=True, **word_diff)[0].diff
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
                if line.startswith('~'):
                    diff_lines[i] = " \n"
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
            bar_width = int(log(num_lines) * 20)
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

    # No changes - clean working slate
    def is_unchanged(self):
        return not self.repo.is_dirty()
