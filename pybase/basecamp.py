############
### Author: Kenneth Miller
### Email Address: ken@erdosmiller.com
### Date: Wed Sep  9 21:02:54 2009
### Function: Basecamp API Wrapper!
############

import base64
import urllib2
import datetime
from elementtree.ElementTree import fromstring

#this is where we define the entire API! In a dict!
url_mapping = {'get_projects':'/projects.xml', #projects
               'get_project':'/projects/%d.xml',
               'who_am_i':'/me.xml', #people
               'all_people':'/people.xml',
               'people_in_project':'/projects/%d/people.xml',
               'people_in_company':'/companies/%d/people.xml',
               'get_person':'/people/%d.xml',
               'companies':'/companies.xml', #companies
               'get_companies_in_project':'/projects/%d/companies.xml',
               'get_company':'/companies/%d.xml',
               'get_categories':'/projects/%d/categories.xml', #categories #this is not complete
               'get_category':'/categories/%d.xml',
               'get_messages':'/projects/%d/posts.xml', #messages
               'get_message':'/posts/%d.xml',
               'get_message_by_category':'/projects/%d/cat/%d/posts.xml',
               'get_archived_messages':'/projects/%d/posts/archive.xml',
               'get_archived_messages_by_category':'/projects/%d/cat/%d/posts/archive.xml',
               'new_message':'/projects/%d/posts/new.xml',
               'edit_message':'/posts/%d/edit.xml',
               'get_project_time':'/projects/%d/time_entries.xml',
               'get_all_todo_entries':'/todo_items/%d/time_entries.xml',
               'get_entry':'/time_entries/%d.xml',
               }

class pythonic_objectify(object):
    def __init__(self,tree,parent=None):
        
        self._parent = parent
        
        if isinstance(tree,str):
            self._tree = fromstring(tree)
        else:
            self._tree = tree

        #this is required to call on all the children
        self._children = [pythonic_objectify(child,self) for child in self._tree]
        
        #assigning attributes to the parent
        if parent is not None:
            
            #making the tags more pythonic - don't hate me!
            tag = self._tree.tag
            tag = tag.replace('-','_')

            #getting the tags value
            value = self._tree.text
            #known type conversion
            if 'type' in self._tree.attrib and value is not None:
                kind = self._tree.attrib['type']
                if kind == 'integer':
                    value = int(value)
                elif kind == 'float':
                    value = float(value)
                elif kind == 'boolean':
                    value = bool(value)
                elif kind == 'date':
                    year, month, day = value.split('-')
                    value = datetime.date(int(year),int(month),int(day))
                
            #apply it to it's parent
            setattr(self._parent,tag,value)
        
        
    def __repr__(self):
        return self._tree.tag

    def __iter__(self):
        return self._children.__iter__()

    def __getitem__(self,index):
        return self._children[index]

    def get_children(self):
        return self._children

    children = property(get_children)
    data = property(get_children)
        
        
        

class Basecamp(object):
    
    def __init__(self, baseURL, username, password):
        self.baseURL = baseURL
        if self.baseURL[-1] == '/':
            self.baseURL = self.baseURL[:-1]

        self.opener = urllib2.build_opener()

        self.auth_string = '%s:%s' % (username, password)
        self.encoded_auth_string = base64.encodestring(self.auth_string)

        self.encoded_auth_string = self.encoded_auth_string.replace('\n', '')
        self.headers = [
            ('Content-Type', 'application/xml'),
            ('Accept', 'application/xml'),
            ('Authorization', 'Basic %s' % self.encoded_auth_string), ]
        self.opener.addheaders = self.headers

    def _request(self, path, data=None):
        if hasattr(data, 'findall'):
            data = ET.tostring(data)

        req = urllib2.Request(url=self.baseURL + path, data=data)
        return self.opener.open(req).read()

    def __getattr__(self,index):
        if index in url_mapping.keys():
            def temp_func(*args):
                #print self._request(url_mapping[index] % args)
                return pythonic_objectify(self._request(url_mapping[index] % args))
            return temp_func
        else:
            return self.__dict__[index]
