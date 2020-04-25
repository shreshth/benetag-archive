from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib

"""
Delete a location cleanly
"""
class DeleteLocationPage(webapp.RequestHandler):
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
                  
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: If no ID sent, default to page with all locations?
            '''
            self.redirect('/')
            return
        _location = db.get(ID)
        ''' an error in getting the location will be redirected to exception handler'''
        
        if _location.owner != user: # if not owner of location
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        # remove from all workers
        _workers = _location.getWorkers()
        if _workers:
            for _worker in _workers:
                if _worker:
                    _worker.remLocation(_location)
                    _worker.put()
                    
        # remove from path in configs
        _configs = _location.getProductConfigs()
        if _configs:
            for _config in _configs:
                if _config:
                    # all path locations for a config
                    locations = _config.getLocations()
                    _config.clearPath() # clear path to rebuild
                    if locations:
                        i = 0
                        index_rem_save = -1 # index of removed element
                        # rebuild path
                        for location in locations:
                            if location.key() != _location.key():
                                _config.addLocationToPath(location, "", i)
                                i = i+1
                            else:
                                index_rem_save = i
                        # fix primary index
                        if _config._path_primary_index:
                            if index_rem_save == _config._path_primary_index:
                                _config._path_primary_index = None
                            if index_rem_save != -1 and index_rem_save < _config._path_primary_index:
                                _config._path_primary_index -= 1
                    _config.put()        
        
        # remove from datastore
        db.delete(ID)
        
        self.redirect('/mylocations')
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(DeleteLocationPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                        
