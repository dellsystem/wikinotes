from datetime import datetime

now = datetime.now()

# Figure out the term from the month ... let's hope McGill doesn't change this anytime soon
month = now.month
if month < 5:
    current_term = 'winter'
elif month < 9:
    current_term = 'summer'
else:
    current_term = 'fall'

current_year = now.year
