import os
import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from blog.models import BlogPost
from urls import static_urls
from wiki.models.courses import Course
from wiki.models.history import HistoryItem
from wiki.models.pages import Page
from wiki.models.users import UserProfile
from wiki.utils.decorators import show_object_detail
from wiki.utils.users import validate_username


def index(request):
    """
    If the user is logged in, the dashboard is shown. Otherwise, it's
    just the generic homepage.
    """
    if request.user.is_authenticated():
        user = request.user.get_profile()
        watched_courses = user.courses.all()

        # First get things done to courses user is watching (exclude self actions)
        history_items = HistoryItem.objects.filter(course__in=watched_courses).exclude(user=request.user).order_by('-timestamp')

        # Get 5 recently edited pages
        recent_pages = request.user.get_profile().get_recent_pages(5)

        try:
            latest_post = BlogPost.objects.order_by('-timestamp')[0]
        except IndexError:
            latest_post = None

        # Show the user's dashboard
        data = {
            'title': 'Your dashboard',
            'recent_pages': recent_pages,
            'watched_courses': watched_courses,
            'history_items': history_items[:20],
            'latest_post': latest_post,
            'profile': request.user.get_profile(),
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
        if request.POST.get('login'):
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

    # Redirect to the page the user was on, or / if none is specified
    path = request.POST.get('path', '/')
    # Check if the path starts with / eventually? Necessary?
    return redirect(path)


# Recent changes
def recent(request, num_days=1, show_all=False):
    base_title = 'All recent activity' if show_all else 'Recent activity'
    title = "%s in the past %s day(s)" % (base_title, num_days)

    data = {
        'title': title,
        'history': HistoryItem.objects.get_since_x_days(num_days, show_all),
        'num_days': num_days,
        'base_url': 'main_all_recent' if show_all else 'main_recent',
        'other_url': 'main_recent' if show_all else 'main_all_recent',
        'show_all': show_all
    }

    return render(request, 'main/recent.html', data)


def explore(request):
    data = {
        'lol': range(4)
    }
    return render(request, 'main/explore.html', data)


def all_recent(request, num_days=1):
    return recent(request, num_days=num_days, show_all=True)


@show_object_detail(UserProfile)
def profile(request, profile):
    this_user = profile.user

    # Figure out the number of pages created and modified
    pages_modified = Page.objects.filter(historyitem__user=this_user).distinct()
    creation_history = HistoryItem.objects.filter(action='created', user=this_user)
    pages_created = pages_modified.filter(historyitem__in=creation_history)
    courses_contributed_to = Course.objects.filter(coursesemester__page__in=pages_modified).distinct()
    num_edits = HistoryItem.objects.filter(user=this_user, page__isnull=False).count()

    return {
        'title': 'Viewing profile for %s' % this_user.username,
        'this_user': this_user, # can't call it user because the current user is user
        'profile': profile,
        'recent_activity': HistoryItem.objects.filter(user=this_user).order_by("-timestamp")[:10],
        'num_pages_modified': pages_modified.count(),
        'num_pages_created': pages_created.count(),
        'num_courses_contributed_to': courses_contributed_to.count(),
        'num_edits': num_edits,
        'contributions_url': reverse('main_contributions', kwargs={'username': this_user.username}),
    }


@show_object_detail(UserProfile)
def contributions(request, profile):
    # If the mode is not specified, show all the pages the user has edited
    mode = request.GET.get('mode', 'modified')
    this_user = profile.user

    if mode == 'courses':
        mode_name = 'Courses contributed to'
        table_data = Course.objects.filter(coursesemester__page__historyitem__user=this_user).distinct()
    elif mode == 'edits':
        mode_name = 'Edits'
        table_data = HistoryItem.objects.filter(user=this_user, page__isnull=False)
    elif mode == 'created':
        mode_name = 'Pages created'
        table_data = this_user.get_profile().get_recent_pages(0, created=True)
    else:
        # Assume the mode is just 'modified'
        mode_name = 'Pages modified'
        table_data = this_user.get_profile().get_recent_pages(0)

    return {
        'table_data': table_data, # the data to be displayed in the table
        'mode': mode,
        'mode_name': mode_name,
        'this_user': this_user,
        'title': "Viewing contributions for %s" % this_user.username,
    }


def register(request):
    # If the user is already logged in, go to the dashboard page
    if request.user.is_authenticated():
        return index(request)
    else:
        if request.POST and 'register' in request.POST:
            # Make sure everything checks out ...

            errors = []
            username = request.POST.get('username')
            email = request.POST.get('email', '')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            university = request.POST.get('university', '').lower()

            # Now check all the possible errors
            if not university.startswith(settings.UNIVERSITY_NAME):
                errors.append("Anti-spam question wrong.")

            if not username:
                errors.append("You didn't fill in your username!")

            if not password:
                errors.append("Please enter a password.")

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
                return redirect('home')
        else:
            return render(request, 'main/registration.html', {'title': 'Create an account'})


def ucp(request, mode=''):
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
        if request.method == 'POST':
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
            if mode == 'account':
                form = PasswordChangeForm(user=request.user,
                                          data=request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['success'] = False

                data['form'] = form

            user_profile.save()
        else:
            if mode == 'account':
                data['form'] = PasswordChangeForm(user=request.user)

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
    query = request.GET.get('query', '')
    # If it's in the form MATH 141, just redirect to that page
    course_re = re.match('(\w{4})[ _-]?(\d{3}D?[12]?)', query)
    if course_re:
        department = course_re.group(1)
        number = course_re.group(2)
        try:
            return redirect(Course.objects.get(department=department.upper(), number=number))
        except Course.DoesNotExist:
            # Just show the search results
            pass

    # Order by popularity (num watchers), descending
    course_results = Course.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) |
        Q(number=query)).order_by('-num_watchers')

    data = {
        'title': 'Search results',
        'query': query,
        'course_results': course_results,
    }

    return render(request, 'search/results.html', data)


def static(request, mode='', page=''):
    # Pretty bad, fix another day
    section_pages = [('overview', mode)]
    section_pages += [(p, '%s_%s' % (mode, p)) for p in static_urls[mode]]
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
