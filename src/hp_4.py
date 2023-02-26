# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = list()
    formatstr = '%Y-%m-%d'
    for i in old_dates:
        start = datetime.strptime(i, formatstr)
        start = start.strftime('%d %b %Y')
        new_dates.append(str(start))
    return new_dates

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("Only string is valid input for start")
    if not isinstance(n, int):
        raise TypeError("Only int is valid input for n")
    added_dates = list()
    formatstr = "%Y-%m-%d"
    start = datetime.strptime(start, formatstr)
    for i in range(n):
        added_dates.append(start)
        start = start + timedelta(days=1)
    return added_dates

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dates = date_range(start_date, len(values))
    con_dates = tuple(dates)
    con_values = tuple(values)
    return list(zip(con_dates, con_values))

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    formatstr = '%m/%d/%Y'
    fee = dict()
    with open(infile, newline='') as f:
        reader = DictReader(f)
        for row in reader:
            patron_id = row['patron_id']
            date_due = row['date_due']
            date_returned = row['date_returned']
            date_due = datetime.strptime(date_due, formatstr)
            date_returned = datetime.strptime(date_returned, formatstr)
            rem = date_due - date_returned
            rem = rem.days
            if rem < 0:
                rem = rem * 0.25
            else:
                rem = 0.00
            rem = format(rem,".2f")
            fee[patron_id] = rem
    with open(outfile, 'w', newline='') as f:
        fieldnames = ['patron_id','late_fees']
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in fee:
            writer.writerow({'patron_id' : key, 'late_fees' : fee[key]})


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
   
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())

