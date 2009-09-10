import datetime
import sys
from pybase import Basecamp
import pdb

def people_keys(bc):
    keys = {}
    
    for person in bc.all_people():
        keys[person.id] = person.first_name + ' ' + person.last_name
        
    return keys

def project_keys(bc):
    keys = {}
    for project in bc.get_projects():
        keys[project.id] = project.name

    return keys


def get_date(name=''):

    date_str = raw_input('Enter %s Date (YYYY-MM-DD) ' % name)
    year, month, day = date_str.split('-')
    return datetime.date(int(year),int(month),int(day))



conn = Basecamp('http://erdosmiller.basecamphq.com','erdosmiller','mosfet')

our_people = people_keys(conn)
our_projects = project_keys(conn)

#for project in conn.get_projects():
#    print project.id

entries = conn.get_project_time(3335163)

all_entries = []

start_date = get_date('Start')
print "Start date is",start_date

end_date = get_date('End Date')
print "End date is",end_date

if start_date > end_date:
    print "Error, start date is after end date."
    sys.exit(0)

for project in our_projects.keys():
    print "Retrievin data for %s" % our_projects[project]
    all_entries.extend(conn.get_project_time(project))

summary = {}

for project in our_projects.keys():
    summary[project] = {}
    for person in our_people.keys():
        summary[project][person] = 0.0
    
for entry in all_entries:
    if entry.date >= start_date and entry.date <= end_date:
        summary[entry.project_id][entry.person_id] += entry.hours
        #print entry.hours, entry.date, our_people[entry.person_id], our_projects[entry.project_id]

for project in summary.keys():
    print "Project %s" % our_projects[project]

    for person in summary[project].keys():
        if summary[project][person] > 0.0:
            print "%s %f" % (our_people[person], summary[project][person])
        


