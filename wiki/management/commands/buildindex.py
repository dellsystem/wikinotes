from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from search import index_entire_history
from wiki.models.pages import Page
import time
class Command(BaseCommand):
	def handle(self, *args, **options):
		print "Clearing indices"
		cursor = connection.cursor()
		cursor.execute("DELETE FROM wiki_keyword")
		cursor.execute("DELETE FROM wiki_keywordlocation")
		print "Starting to index the pages"
		start = time.clock()
		success = 0
		fail = 0
		pages = Page.objects.all()
		for page in pages:
			(yay, no) = index_entire_history(page.get_filepath(), page.pk)
			success += yay
			fail += no
		print "%d failures" % fail
		print "Successfully indexed %d commits in %d files in %s seconds" % (success, len(pages), time.clock() - start)

