from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib



"""
Creates a form to create a Worker
"""
class CreateWorkerPage(webapp.RequestHandler):
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
        template_values['locations'] = _producer.getLocations()
                
        path = os.path.join(os.path.dirname(__file__), 'createworker.html')
        template_values['path'] = "worker"
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateWorkerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        
"""
Puts a worker in the database
"""
class StoreWorkerPage(webapp.RequestHandler):
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
        _location = bene_util.sanitize(self.request.get('location'))
        #_picture = self.request.get('picture')
        _picture = self.request.get('picturedata')
        _profile = bene_util.sanitize(self.request.get('profile'))
        _unique = bene_util.sanitize(self.request.get('unique'))
        popupproduct = bene_util.sanitize(self.request.get('popupproduct'))
                            
        w = entities.Worker(name=_name,  
                            profile=_profile,
                            unique=_unique,
                            owner=user)
        w.addProducer(_producer)
        if _location:
            w.addLocation(db.get(_location))
        w.addPicture(_picture)
        
        # already exists
        if bene_util.doesExactWorkerExist(w): 
            if popupproduct:
                self.redirect('/createworker?%s' % urllib.urlencode({'repeatid': True, 'popupproduct': True}))
                return
            else:
                self.redirect('/createworker?%s' % urllib.urlencode({'repeatid': True}))
                return
        if not _unique:
            if bene_util.doesSimilarWorkerExist(w):
                if popupproduct:
                    self.redirect('/createworker?%s' % urllib.urlencode({'repeatname': True, 'popupproduct': True}))
                    return               
                else:
                    self.redirect('/createworker?%s' % urllib.urlencode({'repeatname': True}))
                    return
        
        w.put()
        if bene_util.sanitize(self.request.get('more')): # want to add more
            self.redirect('/createworker?%s' % urllib.urlencode({'added': True}))
            return
        
        # otherwise redirect to worker page
        if popupproduct:
            self.redirect('/viewworker?%s' % urllib.urlencode({'id' : w.key(), 'popupproduct': True}))
            return
        self.redirect('/viewworker?%s' % urllib.urlencode({'id' : w.key()}))
        return
            
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreWorkerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            