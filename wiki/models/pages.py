# encoding: utf-8
from django.db import models, transaction
from wiki.utils.pages import page_types, page_type_choices#, get_page_type
from wiki.utils.gitutils import Git
import os
from wiki.models.courses import CourseSemester
from wiki.templatetags.wikinotes_markup import wikinotes_markdown
import re
import hashlib
import time

class Page(models.Model):
	class Meta:
		app_label = 'wiki'
		unique_together = ('course_sem', 'slug')
		ordering = ['id']

	course_sem = models.ForeignKey('CourseSemester')
	subject = models.CharField(max_length=255, null=True) # only used for some (most) page types
	link = models.CharField(max_length=255, null=True) # remember the max length. only used for some page_types
	page_type = models.CharField(choices=page_type_choices, max_length=20)
	title = models.CharField(max_length=255, null=True) # the format of this is determined by the page type
	professor = models.ForeignKey('Professor', null=True)
	slug = models.CharField(max_length=50)
	content = models.TextField(null=True) # processed markdown, like a cache

	def load_content(self):
		file = open('%scontent.md' % self.get_filepath())
		content = file.read()
		if self.content==None:
			self.cache_markdown(content)
		file.close()
		return content.decode('utf-8')

	def edit(self, data):
		page_type = page_types[self.page_type]
		# Change the relevant attributes
		for editable_field in page_type.editable_fields:
			if editable_field != 'professor':
				setattr(self, editable_field, data[editable_field])
		self.save()
		# THE FOLDER SHOULD NOT HAVE TO BE MOVED!!! NOTHING IMPORTANT NEEDS TO BE CHANGED!!!
	
	
	def cache_markdown(self,content):
		md = wikinotes_markdown(content)
		md = self.__check_cache(md)
		self.content = md
		self.save()
	
	# gets the parsed markdown regardless whether it's cached or not, if not, it caches it
	def get_markdown_cache(self,useragent):
		if self.content:
			eqns = list(self.eqns.all())
			content = self.content.splitlines()
			engines = ["WebKit","Firefox","Trident","Presto"]
			engine = ""
			for e in engines:
				if e in useragent:
					engine = e
			modified = []
			def repl(line):
				useable = filter(lambda eqn:eqn.hash in line,eqns)
				for eqn in useable:					
					cache = getattr(eqn,engine)
					if len(cache):
						line = line.replace(eqn.hash,cache)
					else:
						line = line.replace(eqn.hash,eqn.eqn)
				return line
			modified = map(repl,content)
			return "\n".join(modified)
		else:
			load_content()
			return get_markdown_cache()
	
	def save_content(self, content, message, username):
		self.cache_markdown(content)
		path = self.get_filepath()
		repo = Git(path)
		filename = '%scontent.md' % path
		file = open(filename, 'wt')
		file.write(content.encode('utf-8'))
		file.close()
		repo.add('content.md')
		message = 'Minor edit' if not message else message
		repo.commit(message, username, 'example@example.com')

	def __unicode__(self):
		return self.get_title()

	def get_filepath(self):
		return "wiki/content%s/" % self.get_absolute_url()

	def get_type(self):
		return page_types[self.page_type]

	def get_title(self):
		if not self.title:
			return self.subject
		else:
			return self.title

	def get_metadata(self):
		metadata = {} # Key: name, value: content
		for field in self.get_type().editable_fields:
			content = self.__getattribute__(field)
			if content:
				metadata[field] = content
		return metadata

	def get_absolute_url(self):
		course = self.course_sem.course
		return "%s/%s/%s-%s/%s" % (course.get_absolute_url(), self.page_type, self.course_sem.term, self.course_sem.year, self.slug)

	# The method can't be solely on the page type itelf, since it doesn't know what course it's for
	def get_type_url(self):
		return "%s/%s" % (self.course_sem.course.get_absolute_url(), self.get_type().short_name)

	# private cache functions, should not be accessed anywhere else
	def __find_blocks(self,txt,tags):
		positions=[]
		for tag in tags:
			tag_split = re.compile(r"<%s.*?>.*?</%s>"%(tag,tag),re.MULTILINE)
			matches = tag_split.finditer(txt)
			for m in matches:
				positions.append({'begin':m.start(0),'end':m.end(0)})
		return positions

	def __get_hash(self,match):
		eqn_type = ""
		exp=""
		raw = match.group(0)
		if match.group(2):
			eqn_type = "block"
			exp = match.group(3).replace("&amp;","&")
			
		if match.group(6):
			eqn_type = "inline"
			exp=match.group(7).replace("&amp;","&")
		exp = "%s-%s" %(eqn_type,exp)
		h = hashlib.sha256()
		h.update(exp)
		exp_hash = h.hexdigest()
		MathjaxCache.objects.get_or_create(eqn=raw,hash=exp_hash,page=self)
		return exp_hash
			
	def __check_cache(self,txt):
		textblocks = self.__find_blocks(txt,["pre","code"])
		textblocks = sorted(textblocks, key=lambda k: k['begin'])
		start = 0
		modified = []
		textblocks.append({'begin':len(txt),'end':len(txt)})
		m = re.compile(r"((\$\$)(.*?)(\$\$))|((\$)(.*?)(\$))")
		with transaction.commit_on_success():
			for block in textblocks:
				if start>block['begin']:
					continue
				cur_block = txt[start:block['begin']]
				modified.append(m.sub(self.__get_hash,cur_block))
				modified.append(txt[block['begin']:block['end']])
				start = block['end']
		txt = "".join(modified)
		
		# hackish way of forcing mathjax to give the proper css even when there are no equations on the page
		txt += "$ $"
		return txt

class MathjaxCache(models.Model):
	class Meta:
		app_label = 'wiki'
	page = models.ForeignKey("Page", related_name='eqns')
	hash = models.CharField(max_length=256)
	eqn = models.TextField()
	Firefox = models.TextField()
	WebKit = models.TextField()
	Trident = models.TextField()
	Presto = models.TextField()
