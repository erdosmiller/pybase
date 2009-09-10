from pybase import Basecamp

t = Basecamp('http://erdosmiller.basecamphq.com','erdosmiller','mosfet')

for project in t.get_projects():
    print project.name, project.id
