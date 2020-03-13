from django import template

register = template.Library()

class GetFirstNode(template.Node):
    def __init__(self, comic):
        self.comic = comic
        
    def render(self, context):
        return self.comic.get_first
        

class GetPrevNode(template.Node):
    def __init__(self, comic):
        self.comic = comic
    
    def render(self, context):
        return self.comic.get_prev

class GetNextNode(template.Node):
    def __init__(self, comic):
        self.comic = comic
    
    def render(self, context):
        return self.comic.get_next
        
class GetLatestNode(template.Node):
    def __init__(self, comic):
        self.comic = comic
    
    def render(self, context):
        return self.comic.get_latest()
    

@register.simple_tag
def get_latest(comic):
    return GetLatestNode(comic)
    #return {'get_latest': get_latest }
    

@register.simple_tag
def get_first(comic):
    """
    get_first = comic.get_first()
    return {'get_first': get_first }
    """
    return GetFirstNode(comic)

@register.simple_tag
def get_next(comic):
    """
    get_next = comic.get_next()
    return {'get_next': get_next }
    """
    return GetNextNode(comic)

@register.simple_tag
def get_prev(comic):
    """
    get_prev = comic.get_prev()
    return {'get_prev': get_prev }
    """
    return GetPrevNode(comic)
