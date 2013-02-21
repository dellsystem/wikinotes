from django.core.management.base import BaseCommand, CommandError

from wiki.models import Page
from wiki.templatetags.wikinotes_markup import wikinotes_markdown


class Command(BaseCommand):
	help = "Refreshes the content field of pages by re-processing all the markdown"

	def handle(self, *args, **options):
		pages = Page.objects.all()
		for page in pages:
			content = page.load_content()
			page.content = wikinotes_markdown(content)
			page.save()
			self.stdout.write("Refreshed %s\n" % page)
