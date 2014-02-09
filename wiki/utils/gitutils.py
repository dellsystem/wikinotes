import datetime
from math import log
from os import makedirs, environ

from django.contrib.auth.models import User
import git
import gitdb


MAX_COMMIT_BAR_WIDTH = 100
MIN_COMMIT_BAR_WIDTH = 20


class Commit:
    def __init__(self, commit):
        """This is a wrapper class for the commit object returned by gitpython
        to make it easier to use within WikiNotes. Should be instantiated with
        the commit object (git.objects.commit.Commit)."""
        self._commit = commit
        self.hexsha = commit.hexsha
        self.message = commit.message
        self.repo_path = commit.repo.working_dir
        self.author_name = commit.author.name
        self.num_lines = commit.stats.total['lines']
        self.num_insertions = commit.stats.total['insertions']
        self.num_deletions = commit.stats.total['deletions']

    def get_content(self):
        """Returns the contents of the file `content.md`.
        """
        return self._commit.tree[0].data_stream.read().decode('utf-8')

    def get_date(self):
        """Returns the timestamp for the time the commit was made."""
        return datetime.datetime.fromtimestamp(self._commit.authored_date)

    def get_author(self):
        return User.objects.get(username=self._commit.author.name)

    def get_diff(self):
        """Gets the diff between this commit and the previous one.
        """
        previous = self._get_previous()

        if previous:
            word_diff = {"word-diff":"porcelain"}
            diff = previous.diff(self.hexsha, create_patch=True, **word_diff)[0].diff
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
                section['lines'].pop()
                end_index = section['start_index'] - 1

            return sections

    def _get_previous(self):
        """Returns the gitpython Commit object for the previous commit.
        """
        is_next = False
        for commit in git.Repo(self.repo_path).iter_commits():
            if is_next:
                return commit
            else:
                is_next = self.hexsha == commit.hexsha

    def get_bar_width(self):
        bar_width = int(log(self.num_lines) * 20)
        return min(max(bar_width, MIN_COMMIT_BAR_WIDTH), MAX_COMMIT_BAR_WIDTH)

    def get_green_percent(self):
        return self.num_insertions * 100 / self.num_lines

    def get_absolute_url(self):
        return '../commit/' + self.hexsha  # TODO: fix


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
            # The directories already exist.
            pass

        self.repo = git.Repo(self.full_path)

    def commit(self, commit_message, username, email):
        """Adds and commits content.md."""
        # Only commits it if there was a change; otherwise, raises an error.
        environ['GIT_AUTHOR_NAME'] = username

        # untracked_files is true so that even the first time it will work.
        if self.repo.is_dirty(untracked_files=True):
            self.repo.index.add(["content.md"])
            commit = self.repo.index.commit(commit_message.encode('utf-8'))
            return Commit(commit)
        else:
            raise NoChangesError

    def get_commit(self, commit_hash):
        hexsha = gitdb.util.hex_to_bin(commit_hash)
        commit = git.objects.commit.Commit(self.repo, hexsha)

        try:
            commit.size
            return Commit(commit)
        except gitdb.exc.BadObject:
            # If the hash does not refer to a commit, commit.size will raise an
            # exception. Return None in that case.
            return None

    def get_latest_commit_hash(self):
        return self.repo.head.commit.hexsha

    def get_history(self):
        """Converts each gitpython Commit object into an internal Commit
        object."""
        return map(Commit, git.Repo(self.full_path).iter_commits())

    def is_unchanged(self):
        return not self.repo.is_dirty()
