from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib



"""
Creates a form for Producers to enter information
about a Location
"""
class CreateLocationPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer  == None: # no producer signed up, so ask to sign up
            self.redirect('/')
            return
        
        if not _producer.verified: # if producer is not verified
            self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
            return
            
        template_values = bene_util.initTemplate(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'createlocation.html')
        template_values['path'] = "location"
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateLocationPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            

"""
Page that stores Location in datastore
"""
class StoreLocationPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer  == None: # no producer signed up, so ask to sign up
            self.redirect('/')
            return
        
        if not _producer.verified: # if producer is not verified
            self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
            return
        
        _name = bene_util.sanitize(self.request.get('name'))
        _address = bene_util.sanitize(self.request.get('address'))
        _location = bene_util.sanitize(self.request.get('location'))
        _unique = bene_util.sanitize(self.request.get('unique'))
        _picture = self.request.get('picturedata')
        _description = bene_util.sanitize(self.request.get('description'))
        popupworker = bene_util.sanitize(self.request.get('popupworker'))
        popupproduct = bene_util.sanitize(self.request.get('popupproduct'))
                                                                               
        fields = _location.split(',')
        if len(fields) == 2:
            try:
                lat = float(fields[0])
                lon = float(fields[1])
                gp = db.GeoPt(lat, lon)
            except ValueError:
                gp = None
        else:
            gp = None
            
        f = entities.Location(name=_name,
                             address=_address,
                             location=gp,
                             description=_description,
                             unique=_unique,
                             owner=user)
        f.addProducer(_producer)
        f.addPicture(_picture)
        
                    
        if bene_util.doesExactLocationExist(f): 
            if popupworker:
                self.redirect('/createlocation?%s' % urllib.urlencode({'repeatid': True, 'popupworker': True}))
                return
            if popupproduct:
                self.redirect('/createlocation?%s' % urllib.urlencode({'repeatid': True, 'popupproduct': True}))
                return
            else:
                self.redirect('/createlocation?%s' % urllib.urlencode({'repeatid': True}))
                return
        if not _unique:
            if bene_util.doesSimilarLocationExist(f):
                if popupworker:
                    self.redirect('/createlocation?%s' % urllib.urlencode({'repeatname': True, 'popupworker': True}))
                    return     
                if popupproduct:
                    self.redirect('/createlocation?%s' % urllib.urlencode({'repeatname': True, 'popupproduct': True}))
                    return               
                else:
                    self.redirect('/createlocation?%s' % urllib.urlencode({'repeatname': True}))
                    return
        
        f.put()
        
        if bene_util.sanitize(self.request.get('more')): # want to add more
            self.redirect('/createlocation?%s' % urllib.urlencode({'added': True}))
            return
        
        # otherwise redirect to location page
        if popupworker:
            self.redirect('/viewlocation?%s' % urllib.urlencode({'id' : f.key(), 'popupworker': True}))
            return
        if popupproduct:
            self.redirect('/viewlocation?%s' % urllib.urlencode({'id' : f.key(), 'popupproduct': True}))
            return
        
        self.redirect('/viewlocation?%s' % urllib.urlencode({'id' : f.key()}))
        return
        
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreLocationPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                
