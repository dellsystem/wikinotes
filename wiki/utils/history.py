import datetime
# Put here because, why not
def get_date_x_days_ago(num_days):
	return datetime.datetime.now() - datetime.timedelta(days=num_days)

# Used by HistoryItem to output a human-readable timestamp
# More vague than the built-in timesince filter, which is good
# Written by Joey Bratton http://www.joeyb.org/blog/2009/10/08/custom-django-template-filter-for-humanized-timesince
def humanise_timesince(start_time):
	delta = datetime.datetime.now() - start_time

	plural = lambda x: 's' if x != 1 else ''

	num_years = delta.days / 365
	if (num_years > 0):
		return "%d year%s" % (num_years, plural(num_years))

	num_weeks = delta.days / 7
	if (num_weeks > 0):
		return "%d week%s" % (num_weeks, plural(num_weeks))

	if (delta.days > 0):
		return "%d day%s" % (delta.days, plural(delta.days))

	num_hours = delta.seconds / 3600
	if (num_hours > 0):
		return "%d hour%s" % (num_hours, plural(num_hours))

	num_minutes = delta.seconds / 60
	if (num_minutes > 0):
		return "%d minute%s" % (num_minutes, plural(num_minutes))

	return "a few seconds"


def collapse(items):
	users = set([item.user for item in items]);
	history_item = {};
	if(len(items)>len(users)):
		if(len(users)==1):
			history_item["owner"] = items[0].user
		else:
			history_item["owner"] = items[0].user
			history_item["others"] = "and %d other" %(len(users)-1);
			if(len(users)>2):
				history_item["other"] +="s"
		if(items[0].page):
			history_item["event"] = "%s %s %d times" %(items[0].action,items[0].page,len(items))
		else:
			history_item["event"] = "%s this course %d times" % (items[0].action,len(items))
	else:
		history_item["owner"] = (items[0].user);
		history_item["others"] ="and %d other" %(len(users)-1);
		if(len(items)>2):
			history_item["others"] +="s"
		if(items[0].page):
			history_item["event"] = "%s %s" %(items[0].action,items[0].page)
		else:
			history_item["event"] = "%s this course" % (items[0].action)
	history_item["time"] = items[0].timestamp;
	history_item["time_since"] = items[0].get_timesince();
	history_item["items"] = items
	return history_item


