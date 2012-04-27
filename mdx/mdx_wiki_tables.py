#!/usr/bin/env Python
"""
Tables Extension for Python-Markdown
====================================

Added parsing of tables to Python-Markdown.

A simple example:

	First Header  | Second Header
	------------- | -------------
	Content Cell  | Content Cell
	Content Cell  | Content Cell

Copyright 2009 - [Waylan Limberg](http://achinghead.com)
"""
import markdown
from markdown.util import etree


class TableProcessor(markdown.blockprocessors.BlockProcessor):
	""" Process Tables. """
	allowed_classes = ['sort', 'clear', 'autumn', 'lights', 'ribbon', 'fresh', 'iris', 'column'] # lol

	def test(self, parent, block):
		rows = block.split('\n')
		return (len(rows) > 2 and '|' in rows[0] and
				'|' in rows[1] and '-' in rows[1] and
				rows[1].strip()[0] in ['|', ':', '-'])

	def run(self, parent, blocks):
		""" Parse a table block and build table. """
		block = blocks.pop(0).split('\n')
		header = block[0].strip()
		separator = block[1].strip()
		rows = block[2:]
		# Get format type (bordered by pipes or not)
		border = False
		if header.startswith('|'):
			border = True
		# Get alignment of columns
		align = []
		for c in self._split_row(separator, border):
			if c.startswith(':') and c.endswith(':'):
				align.append('center')
			elif c.startswith(':'):
				align.append('left')
			elif c.endswith(':'):
				align.append('right')
			else:
				align.append(None)
		# Build table
		table = etree.SubElement(parent, 'table')
		thead = etree.SubElement(table, 'thead')
		self._build_row(header, thead, align, border)
		tbody = etree.SubElement(table, 'tbody')

		# Set any necessary classes on the table
		classes = self.__get_classes(separator)
		if classes:
			table.set('class', ' '.join(classes))

		for row in rows:
			self._build_row(row.strip(), tbody, align, border)

	def _build_row(self, row, parent, align, border):
		""" Given a row of text, build table cells. """
		tr = etree.SubElement(parent, 'tr')
		tag = 'td'
		if parent.tag == 'thead':
			tag = 'th'
		cells = self._split_row(row, border)
		# We use align here rather than cells to ensure every row
		# contains the same number of columns.
		span = 0
		for i, a in enumerate(align):
			try:
				if cells[i] == "":
					span += 1
					continue
			except:
				pass
			c = etree.SubElement(tr, tag)
			
			try:
				if span > 0:
					c.set('colspan',"%d" % (span+1))
					span = 0
				c.text = cells[i].strip()
			except IndexError:
				c.text = ""
			if a:
				c.set('class', a + '-align')

	def _split_row(self, row, border):
		""" split a row of text into list of cells. """
		if border:
			if row.startswith('|'):
				row = row[1:]
			if row.endswith('|'):
				row = row[:-1]
		return row.split('|')

	def __get_classes(self, separator):
		classes = []
		for possible_class in separator.split(' '):
			if not possible_class.startswith('-') and not possible_class.startswith('|'):
				if possible_class in self.allowed_classes:
					classes.append(possible_class)
		return classes

class TableExtension(markdown.Extension):
	""" Add tables to Markdown. """

	def extendMarkdown(self, md, md_globals):
		""" Add an instance of TableProcessor to BlockParser. """
		md.parser.blockprocessors.add('table',
									  TableProcessor(md.parser),
									  '<hashheader')


def makeExtension(configs={}):
	return TableExtension(configs=configs)
