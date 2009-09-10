from pybase import Basecamp

basecamp_url = raw_input('BaseCamp URL.')
username = raw_input('BaseCamp UserName:')
password = raw_input('BaseCamp PassWord:')

conn = Basecamp(basecamp_url,username,password)

for project in conn.get_projects():
    print project.name, project.id
