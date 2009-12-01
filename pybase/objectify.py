class Objectify(object):
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
                    value = datetime.datetime(int(year),int(month),int(day))
                
            #apply it to it's parent
            setattr(self._parent,tag,value)
        
    def __repr__(self):
        return self._tree.tag

    def __iter__(self):
        return self._children.__iter__()

    def __getitem__(self,index):
        try:
            return self._children[index]
        except AttributeError:
            return getattr(self,index)

    def get_children(self):
        return self._children

    children = property(get_children)
    data = property(get_children)
