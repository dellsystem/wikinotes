from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from wiki.models.courses import Course
from wiki.models.history import HistoryItem
from wiki.utils.users import validate_username
from wiki.models.pages import Page
from blog.models import BlogPost
from wiki.models.searchindex import Result
from django.http import Http404
from urls import static_urls
import os
import re
from time import clock
from search import search as search_module
from django.utils.html import escape

# welcome is only set to true when called from register()
# Triggers the display of some sort of welcome message
def index(request, show_welcome=False):
	if request.user.is_authenticated():
		user = request.user.get_profile()
		watched_courses = user.courses.all()

		# First get things done to courses user is watching (exclude self actions)
		history_items = HistoryItem.objects.filter(course__in=watched_courses).exclude(user=request.user)

		# Now get things the user has done
		your_actions = HistoryItem.objects.filter(user=user).order_by('-timestamp')

		try:
			latest_post = BlogPost.objects.order_by('-timestamp')[0]
		except IndexError:
			latest_post = {'title': 'Nothing', 'summary': 'Nothing'}

		# Show the user's dashboard
		data = {
			'title': 'Your dashboard',
			'watched_courses': watched_courses,
			'history_items': history_items[::-1],
			'show_welcome': show_welcome,
			'latest_post': latest_post,
		}
		return render(request, 'main/dashboard.html', data)
	else:
		# Show the main page for logged-out users
		return render(request, 'main/index.html')

# POSTed to by the login form; should never be accessed by itself
def login_logout(request):
	# Check if the user is already logged in and is trying to log out
	if request.user.is_authenticated():
		if 'logout' in request.POST:
			logout(request)
	else:
		if request.POST['login']:
			try:
				username = User.objects.get(username__iexact=request.POST['username'])
				password = request.POST['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
				else:
					raise User.DoesNotExist
			except User.DoesNotExist:
				return render(request, 'main/login_error.html')

	# Redirect to the index page etc
	return redirect('/')

# Recent changes
def recent(request, num_days=1, show_all=False):
	data = {
		'title': 'Recent activity',
		'history': HistoryItem.objects.get_since_x_days(num_days, show_all),
		'num_days': num_days,
		'base_url': '/recent/all' if show_all else '/recent', # better way of doing this?
		'show_all': show_all
	}
	return render(request, 'main/recent.html', data)

def all_recent(request, num_days=1):
	return recent(request, num_days=num_days, show_all=True)

def profile(request, username):
	this_user = User.objects.get(username__iexact=username)
	data = {
		'title': 'Viewing profile (%s)' % this_user.username,
		'this_user': this_user, # can't call it user because the current user is user
		'profile': this_user.get_profile(),
		'recent_activity': HistoryItem.objects.filter(user=this_user),
		'user_pages': Page.objects.filter(historyitem__user=this_user),
	}
	return render(request, 'main/profile.html', data)

def register(request):
	# If the user is already logged in, go to the dashboard page
	if request.user.is_authenticated():
		return index(request)
	else:
		if request.POST and 'register' in request.POST:
			# Make sure everything checks out ...

			errors = []
			username = request.POST['username']
			email = request.POST['email'] # this can be blank. it's okay.
			password = request.POST['password']
			password_confirm = request.POST['password_confirm']
			university = request.POST['university'].lower()

			# Now check all the possible errors
			if university != 'mcgill' and university != 'mcgill university':
				errors.append("Anti-spam question wrong! Please enter the university WikiNotes was made for.")

			if username == '':
				errors.append("You didn't fill in your username!")

			if len(password) < 6:
				errors.append("Your password is too short. Please keep it to at least 6 characters.")

			if password_confirm != password:
				errors.append("Passwords don't match!")

			# First check if the username is valid (might migrate to using the form from django.contrib.auth later)
			# Only allow alphanumeric chars for now, can change later
			if username and not validate_username(username):
				errors.append("Please only use alphanumeric characters and the underscore for your username.")

			# Now check if the username (any case combination) is already being used
			if User.objects.filter(username__iexact=username).count() > 0:
				errors.append("This username is already in use! Please find a new one.")

			data = {
				'title': 'Create an account (errors)',
				'errors': errors,
				'username': username,
				'email': email,
				'password': password,
				'university': university # so if there's an unrelated error user doesn't have to enter it again
			}

			if errors:
				return render(request, 'main/registration.html', data)
			else:
				# If the registration proceeded without errors
				# Create the user, then log the user in
				User.objects.create_user(username, email, password)
				new_user = authenticate(username=username, password=password)
				login(request, new_user)
				return index(request, show_welcome=True)
		else:
			return render(request, 'main/registration.html', {'title': 'Create an account'})

def ucp(request, mode):
	modes = ['overview', 'account', 'profile', 'preferences']
	if mode == '' or mode not in modes:
		mode = 'overview'
	if request.user.is_authenticated():
		user = request.user
		user_profile = user.get_profile()
		data = {
			'title': 'User control panel (%s)' % mode,
			'profile': user_profile,
			'mode': mode,
			'modes': modes,
			'template': 'ucp/' + mode + '.html',
			'success': False,
		}

		# Now check if a request has been submitted
		if request.POST:
			data['success'] = True
			if mode == 'preferences':
				user_profile.show_email = request.POST['show_email'] == '1'
			if mode == 'profile':
				user_profile.bio = request.POST['ucp_bio']
				user_profile.website = request.POST['ucp_website']
				user_profile.twitter = request.POST['ucp_twitter']
				user_profile.github = request.POST['ucp_github']
				user_profile.facebook = request.POST['ucp_facebook']
				user_profile.gplus = request.POST['ucp_gplus']
				user_profile.major = request.POST['ucp_major']
			user_profile.save()

		return render(request, 'main/ucp.html', data)
	else:
		return register(request)

def markdown(request):
	if 'content' in request.POST and 'csrfmiddlewaretoken' in request.POST:
		data = {
			'content': request.POST['content']
		}
		return render(request, 'main/markdown.html', data)
	else:
		raise Http404

def search(request):
	if 'query' in request.GET:
		start = clock()
		results = search_module(request.GET["query"], 0)
		parsed_results = []
		for result in results:
			presult = Result()
			page = Page.objects.get(pk=result["id"])
			presult.page_url = page.get_absolute_url()
			presult.page_title = presult.page_url.replace("_", " ").strip("/").replace("/", " / ")
			line_nums = [k["line"] for k in result["lines"]]
			content = page.load_content().splitlines()
			content_length = len(content)
			preview_line_nums = []
			if len(line_nums):
				preview_line_nums = line_nums[:2]
			else:
				preview_line_nums = [0]

			# get the surrounding lines for context
			preview_lines = map(lambda k: escape(content[k - 1]), preview_line_nums)
			preview = " ...<br />... ".join(preview_lines)

			#not working perfectly, suppose to contract long paragraphs to only show the parts containing the words
			"""
			if len(preview) > 200:
				seg_length = 200 / len(result['words'])
				p = re.compile("(([^ ]* (.){0,%d})(%s)(.{0,%d} [^ ]*) +)+" % (seg_length, "|".join(result['words']), seg_length), re.IGNORECASE)
				shortened = []
				for match in p.finditer(preview):
					shortened.append(match.group(0))
				preview = "..." + " ... ".join(shortened) + " ..."
			"""
			# highlight found words
			p = re.compile("|".join(result['words']), re.IGNORECASE)
			preview = p.sub(lambda m: "<strong>%s</strong>" % m.group(0), preview)

			presult.preview_text = preview

			for commit in result["commits"][:3]:
				presult.commits_mentioned.append({"name":commit["commit"][:10], "url":(presult.page_url + "/commit/" + commit["commit"])})
			presult.commits_hidden = len(result["commits"]) - 3 if len(result["commits"]) > 3 else 0
			parsed_results.append(presult)
		data = {
			'query': request.GET['query'],
			'results':parsed_results,
			'time':"%0.4f" % (clock() - start)
		}
		return render(request, 'search/results.html', data)
	else:
		raise Http404

def static(request, mode='', page=''):
	section_pages = ['overview'] + static_urls[mode]
	markdown_file = '%s/%s.md' % (mode, page)
	html_file = '%s/%s.html' % (mode, page)
	data = {
		'title': mode.title() + ' (' + page.title() + ')',
		'html_file': html_file if os.path.isfile('templates/' + html_file) else None,
		'markdown_file': markdown_file if os.path.isfile('templates/' + markdown_file) else None,
		'page': page,
		'mode': mode,
		'section_pages': section_pages,
	}
	return render(request, 'static.html', data)
