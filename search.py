# encoding: utf-8
import sys
import subprocess
import re
import traceback
import os
import hashlib
from django.db import connection, transaction
import itertools
import time
from django.utils.encoding import smart_str, smart_unicode
def index_entire_history(file_path, page_id, *args, **kwargs):
	print "indexing %s - %s" % (file_path.split('/')[2] , file_path.split("/")[5])
	try:
		file_path = file_path.strip('/')

		# not a git repo
		if not os.path.exists("%s/.git" % file_path):
			return


		command = "cd \"%s\" && git log --reverse --format=format:\"%%H\"" % (file_path)
		lines = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].splitlines()
	except:
		return (0, 1)
	commit_count = 0
	fail_count = 0
	#index each commit starting from the earliest
	for (i, line) in enumerate(lines):
		try:
			index_commit(file_path, page_id, commit=line)

			#progress bar lol
			total_width = 60
			current_width = (i + 1) * total_width / len(lines)
			sys.stdout.write("\r|" + ('-' * (current_width)).ljust(total_width) + "|" + "%d%%" % ((i + 1) * 100 / len(lines)))

			commit_count += 1
		except:
			traceback.print_exc(file=sys.stdout)
			fail_count = 1
	print "\nDone!"
	return (commit_count, fail_count)

#TODO: return total num of results, better ordering (tf-idf?), and COMMENT
def search(search_query, start):
	results = []
	subqueries = get_valid_keywords(search_query)
	con = connection.cursor()
	subresults = []
	pages_hit = {}
	for q in subqueries:
		query = "\
				SELECT page,max(frequency * exp(-3*head)) as score FROM wiki_keyword where keyword = %s\
				GROUP BY page ORDER BY score DESC LIMIT 20 OFFSET %s\
				"
		con.execute(query , (q, start))
		for (i, row) in enumerate(con.fetchall()):
			page = row[0]
			if page not in pages_hit:
				pages_hit[page] = {"priority":1.0 + (10.0 - i) / 10, "words":[q], "id":page}
			else:
				pages_hit[page]["priority"] += 1.0 + (10.0 - i) / 10
				pages_hit[page]["words"].append(q)
	pages = sorted(pages_hit.values(), key=lambda k: k["priority"], reverse=True)[:10]
	commit_queries = []
	for page in pages:
		commits_hit = {}
		lines_hit = {}
		for word in page["words"]:
			con.execute("SELECT \"commit\" from wiki_keyword where page = %s and keyword = %s", (page["id"], word))
			for row in con.fetchall():
				if row[0] in commits_hit:
					commits_hit[row[0]]["count"] += 1
				else:
					commits_hit[row[0]] = {"commit": row[0], "count": 1}
			con.execute("SELECT head_line_num from wiki_keywordlocation where head = 0 and page = %s and word = %s", (page["id"], word))
			for row in con.fetchall():
				if row[0] in lines_hit:
					lines_hit[row[0]]["count"] += 1
				else:
					lines_hit[row[0]] = {"line": row[0], "count": 1}
		page["commits"] = sorted(commits_hit.values(), key=lambda k:k["count"], reverse=True)
		page["lines"] = sorted(lines_hit.values(), key=lambda k:k["count"], reverse=True)[:3]
	return pages

@transaction.commit_manually()
def index_commit(file_path, page_id, *args, **kwargs):
	start = time.clock()
	#indexes the head by default, but can index past commits
	commit = kwargs.get("commit", "HEAD")

	conn = kwargs.get("db", connection)
	file_path = file_path.strip('/')
	command = "cd \"%s\" && git show --format=format:\"%%H%%n%%ct\" %s" % (file_path , commit)
	lines = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].splitlines()


	commit = None
	date = None
	current_hunk = None


	words_changed = {}
	words_to_add = []

	#we don't really care about what word was deleted, all the words in the line are deleted
	lines_deleted = []

	# used to calculate the positions of words in the older commit now in the newest version, with added/removed lines
	line_offset = []

	#parse the diff to index the new commit
	for (i, line) in enumerate(lines):

		#first two lines are the commit and the date respectively
		if i == 0:
			commit = line
		if i == 1:
			date = line

		#a hunk header, we're starting a hunk, parse the header
		if line[0:2] == "@@":
			# hunk header is in the format of 
			# @@ -\d,\d +\d,\d @@ line-content
			hunk_pattern = re.compile(r"@@ -([\d]+),?([\d]*) \+([\d]+),?([\d]*) @@.*")
			m = hunk_pattern.match(line)
			current_hunk = {}
			current_hunk["oldstart"] = int(m.group(1))

			#sometimes the range of the hunk is omitted because it's 1
			if len(m.group(2)):
				current_hunk["oldlen"] = int(m.group(2))
			else:
				current_hunk["oldlen"] = 1
			current_hunk["newstart"] = int(m.group(3))
			if len(m.group(4)):
				current_hunk["newlen"] = int(m.group(4))
			else:
				current_hunk["newlen"] = 1

			#0 lines read for this current hunk
			current_hunk["oldread"] = 0
			current_hunk["newread"] = 0

		#not inside a hunk, and not a hunk header so no need to parse
		if not current_hunk or len(line) == 0:
			continue

		#inserted line
		if line[0] == '+':

			#line number in the current commit
			line_num = current_hunk["newstart"] + current_hunk["newread"]
			old_line_num = current_hunk["oldstart"] + current_hunk["oldread"]

			#a start of a + block
			#sometimes a blank line is put between every line of the hunk for some reason
			prev_line = lines[i - 1] if len(lines[i - 1]) else lines[i - 2]
			if prev_line[0] != line[0]:
				line_offset.append({"line_num":old_line_num, "len": 1})
			#middle of a + block
			else:
				line_offset[-1]["len"] += 1

			keywords = get_valid_keywords(line)
			if len(keywords) == 0:
				current_hunk["newread"] += 1
				continue

			for (word_pos, word) in enumerate(keywords):
				hash = None
				if word not in words_changed:
					hash = "%d-%s-%s" % (page_id, hashlib.md5(word).hexdigest()[:20], commit[:10])

					words_changed[word] = {"count":1, "hash":hash}

				else:
					hash = words_changed[word]["hash"]
					words_changed[word]["count"] += 1
				id = "%d-%d-%s-%d" % (page_id, word_pos, commit[:20], line_num)
				words_to_add.append({"id":id, "word":word, "hash":hash, "line":line_num, "pos":word_pos})

			current_hunk["newread"] += 1

		#deleted line
		elif line[0] == '-':
			#line number in older version
			line_num = current_hunk["oldstart"] + current_hunk["oldread"]

			#a start of a - block
			prev_line = lines[i - 1] if len(lines[i - 1]) else lines[i - 2]
			if prev_line[0] != line[0]:
				#has to add one because the line is deleted, so every line starting from the line after it will
				#be shifted
				line_offset.append({"line_num":line_num + 1, "len":-1})
			#middle of a - block
			else:
				line_offset[-1]["len"] -= 1
				line_offset[-1]["line_num"] = line_num + 1

			keywords = get_valid_keywords(line)
			if len(keywords) == 0:
				current_hunk["oldread"] += 1
				continue

			for (word_pos, word) in enumerate(keywords):
				hash = None
				if word not in words_changed:
					hash = "%d-%s-%s" % (page_id, hashlib.md5(word).hexdigest()[:20], commit[:10])

					words_changed[word] = {"count":-1, "hash":hash}
				else:
					words_changed[word]["count"] -= 1

			lines_deleted.append(line_num)


			current_hunk["oldread"] += 1

		#unchanged line
		elif line[0] == ' ':
			line_num = current_hunk["newstart"] + current_hunk["newread"]
			old_line_num = current_hunk["oldstart"] + current_hunk["oldread"]

			current_hunk["newread"] += 1
			current_hunk["oldread"] += 1

	def split_seq(iterable, size):
		it = iter(iterable)
		item = list(itertools.islice(it, size))
		while item:
			yield item
			item = list(itertools.islice(it, size))

	cursor = conn.cursor()

	try:
		#add the changes to the word base in this commit, no positional information yet
		insert_commit_changes(words_changed, page_id, commit, date, cursor)
		for chunk in split_seq(lines_deleted, 100):
			#the words in the deleted lines are no longer in the head
			unflag_deleted(chunk, page_id, cursor)
		#the position of the words in the unmodified lines is pushed to different positions
		shift_older_lines(line_offset, page_id, cursor)
	except:
		transaction.rollback()
	else:
		#have to commit here so the new keywords don't collide with the old ones(which are shifted from the commit)
		transaction.commit()
		try:
			#finally add the new words to the index
			add_new_words(words_to_add, page_id, cursor)
		except:
			transaction.rollback()
		else:
			transaction.commit()

def add_new_words(words, page, cursor):
	values = []
	for word in words:
		value = (word["id"], word["hash"], word["word"], page, word["line"], word["pos"], word["line"])
		values.append(value)
	query = "INSERT INTO wiki_keywordlocation values (%s,%s,%s,%s,%s,%s,0,%s,0)"
	try:
		cursor.executemany(query, values)
	except:
		traceback.print_exc(file=sys.stdout)
		raise Exception

def shift_older_lines(offsets, page, cursor):
	highest_affected = sys.maxint
	#have to use temp because we're want to modify head_line_num based on the old value of head_line_num
	cursor.execute("UPDATE wiki_keywordlocation SET temp = head_line_num WHERE page = %d and head = 0" % (page))
	for offset in offsets:
		loc = offset["line_num"]
		if loc < highest_affected:
			highest_affected = loc
		len = offset["len"]
		query = "UPDATE wiki_keywordlocation SET temp = temp + %d WHERE page = %d and head_line_num >= %d and head = 0" % (len, page, loc)
		try:
			cursor.execute(query)
		except:

			traceback.print_exc(file=sys.stdout)
			raise Exception
	cursor.execute("UPDATE wiki_keywordlocation SET head_line_num = temp WHERE page = %d and head_line_num >= %d and head = 0" % (page, highest_affected))

def unflag_deleted(lines, page, cursor):
	query = "UPDATE wiki_keywordlocation SET head = head +1 WHERE page = " + str(page) + " and head_line_num = %s"
	try:
		cursor.executemany(query, [(k,) for k in lines])
	except:
		print query
		traceback.print_exc(file=sys.stdout)
		raise Exception


def insert_commit_changes(words, page, commit, date, cursor):
	start = time.clock()
	values = []
	query = u"UPDATE wiki_keyword SET head = head + 1  WHERE page = " + str(page) + " and keyword = %s"
	try:
		cursor.executemany(query, [(k,) for k in words.keys()])
	except:
		print query
		traceback.print_exc(file=sys.stdout)
		raise Exception
	for word in words.keys():
		frequency = words[word]["count"]
		value = (words[word]["hash"], page, word, commit, word, page, frequency, frequency, date)
		values.append(value)

	query = u"INSERT INTO wiki_keyword values(%s,%s,%s,%s,COALESCE((SELECT frequency FROM wiki_keyword WHERE keyword = %s and page = %s and head = 1)+%s,%s),%s,0)"
	try:
		cursor.executemany(query, values)
	except:
		traceback.print_exc(file=sys.stdout)
		raise Exception


ignore_words = ["the", "be", "to", "of", "and", "a",
			"in", "that", "have", "I", "it", "for",
			"not", "on", "with", "he", "as", "you", "why",
			"do", "at", "this", "but", "his", "by", "where",
			"from", "they", "we", "say", "her", "she", "name",
			"or", "an", "will", "my", "one", "all",
			"would", "there", "their", "what", "so",
			"up", "out", "if", "about", "who", "get",
			"which", "go", "me", "when", "make", "can",
			"like", "time", "no", "just", "him", "know",
			"take", "person", "into", "year", "your",
			"good", "some", "could", "them", "see", "number",
			"other", "than", "then", "now", "look", "only",
			"come", "its", "over", "think", "also", "back", "has",
			"after", "use", "two", "how", "our", "work", "usually",
			"first", "well", "way", "even", "new", "want", "ago", "com",
			"because", "any", "these", "give", "day", "are", "dont", "don"
			"most", "us", "toc", "iff", "neg", "let", "lor"]

def get_valid_keywords(line):
	line = smart_str(line)
	#split on delimiters
	delim = re.compile(r"[\.,:;\[\]\(\)\-_\\/=\+\}\{><\|]")
	line = delim.sub(" ", line)

	#strip random punctuations and quotes
	punct = re.compile(r"[\*#\\?@`~!\$%\^&\"\']")
	line = punct.sub(" ", line)


	#split camel case words into individual words
	#pattern = re.compile('([A-Z][A-Z][a-z])|([a-z][A-Z])')
	#with_camel = pattern.sub(lambda m: m.group()[:1] + " " + m.group()[1:], with_spacing)

	keywords = line.split()


	#eliminate words shorter than 3 letters, and frequently used words
	def eliminate(word):
		return word.lower() not in ignore_words and len(word) > 2
	keywords = map(lambda k:k.lower(), filter(eliminate, keywords))
	return keywords

if len(sys.argv) > 2:
	if sys.argv[1] == "index":
		index_commit(sys.argv[2], sys.argv[3])

	if sys.argv[1] == "search":
		search(sys.argv[2])

