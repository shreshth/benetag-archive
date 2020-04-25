from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib
        

"""
Creates a form for Producers to change a config
"""
class EditConfigPage(webapp.RequestHandler):
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
            TODO: If no ID sent?
            '''
            self.redirect('/')
            return
        _productconfig = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _productconfig.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        _productline = _productconfig.getProductLine()
                        
        template_values = bene_util.initTemplate(self.request.uri)
        
        template_values['path'] = "product"
        template_values['product'] = _productline
        template_values['cropentity'] = _productline
        template_values['id'] = ID
        template_values['name_old'] = _productline.name
        template_values['description_old'] = _productline.description
        template_values['configname_old'] = _productconfig.config_name
        template_values['num_products'] = _productconfig.numProducts()
        template_values['display_amazon'] = _productconfig.displayAmazon
        template_values['storelink'] = _productconfig.store_link
        # locations
        template_values['no_locations'] = True
        _locations_old = _productconfig.getLocations()
        if _locations_old: template_values['no_locations'] = False
        template_values['locations_old'] = _locations_old
        # workers
        template_values['no_workers'] = True
        _workers_old = _productconfig.getWorkers()
        if _workers_old.get(): template_values['no_workers'] = False
        template_values['workers_old'] = _workers_old
        #badges
        template_values['no_badges'] = True
        _badges_old = _productconfig.getBadges()
        if _badges_old: template_values['no badges'] = False        
        template_values['badges_old'] = _badges_old
                                
        '''
        TODO: Find better way to do below. For some reason equality doesn't work implicitly. 
        Need to explicitly check equality of key()
        '''

        template_values['locations'] = []
        _locations = _producer.getLocations()
        count = 0
        if _locations:
            for location in _locations:
                if location:
                    add = True
                    count += 1
                    if len(location.name) > 10:
                        count += 1
                    if _locations_old:
                        for location_old in _locations_old:
                            if location_old:
                                if location_old.key() == location.key():
                                    add = False
                    if add:
                        template_values['locations'].append(location)
                        template_values['no_locations'] = False
        if not count:
            count = 1
        template_values['pathheight'] = count*40              
        template_values['workers'] = []
        _workers = _producer.getWorkers()
        if _workers:
            for worker in _workers:
                if worker:
                    add = True
                    if _workers_old:
                        for worker_old in _workers_old:
                            if worker_old:
                                if worker_old.key() == worker.key():
                                    add = False
                    if add:
                        template_values['workers'].append(worker)
                        template_values['no_workers'] = False
                                
        template_values['badges'] = []
        _badges = entities.Badge.all()
        if _badges:
            for badge in _badges:
                if badge:
                    add = True
                    if _badges_old:
                        for badge_old in _badges_old:
                            if badge_old.key() == badge.key():
                                add = False
                    if add:
                        template_values['badges'].append(badge)
                        template_values['no badges'] = False
                    
        path = os.path.join(os.path.dirname(__file__), 'editconfig.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditConfigPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                             
"""
Page that stores config in datastore
"""
class StoreEditedConfigPage(webapp.RequestHandler):
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
                    
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: If no ID sent?
            '''
            self.redirect('/')
            return
        _productconfig = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _productconfig.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        _configname = bene_util.sanitize(self.request.get('configname'))     
        _configname_save = _productconfig.config_name  
        _productconfig.config_name=_configname
        
        # already exists
        if bene_util.doesSimilarProductConfigExist(_productconfig, _productconfig.getProductLine()) and not _configname_save == _productconfig.config_name: 
            self.redirect('/editconfig?%s' % urllib.urlencode({'repeatedit': True, 'id': ID}))
            return 
                    
        # locations
        _locations = bene_util.sanitize(self.request.get('orderedlocations'))
        if _locations:
            _locations = _locations.split(',')
            locations = db.get(_locations)
            
        config_key = _productconfig.key()
        # remove config from old locations
        locations_old = _productconfig.getLocations()
        if locations_old:
            for location_old in locations_old:
                if location_old:
                    if not _locations: # convert nonetype to empty array
                        _locations = []
                    if location_old.key() not in _locations:
                        location_old.remProductConfig(config_key)
                        location_old.put()
        _productconfig.clearPath() 
        if _locations:
            i = 0
            if locations:
                for location in locations:
                    if location:
                        # add config to new locations
                        location.addProductConfig(config_key)
                        location.put()
                        # add to path
                        _productconfig.addLocationToPath(location, "", i)
                        i = i + 1 
                    
        # workers
        _workers = bene_util.sanitizeList(self.request.get_all('workers'))
        if not _workers:
            _workers = []
        # remove config from old locations
        workers_old = _productconfig.getWorkers()
        if workers_old:
            for worker_old in workers_old:
                if worker_old:
                    if worker_old.key() not in _workers:
                        worker_old.remProductConfig(config_key)
                        worker_old.put()
        # add config to new locations
        workers = db.get(_workers)
        if workers:
            for worker in workers:
                if worker:
                    worker.addProductConfig(config_key)
                    worker.put() 
                        
                        
        # badges
        _badgeskeys = bene_util.sanitizeList(self.request.get_all('badges'))
        _badges_old = _productconfig.getBadges()
        if not _badges_old: # convert None to empty array
            _badges_old = []
        if not _badgeskeys: # convert None to empty array
            _badgeskeys = []
        if _badges_old:
            for badge in _badges_old:
                if badge.key() not in _badgeskeys:
                    _productconfig.remBadge(badge.key())
        if _badgeskeys:
            for badgekey in _badgeskeys:
                badge = db.get(badgekey)
                if badge not in _badges_old:
                    _productconfig.addBadge(db.Key(badgekey))
        
        #storelink
        s_price = bene_util.sanitize(self.request.get('storePrice'))
        s_name = bene_util.sanitize(self.request.get('storeName'))
        s_url = bene_util.sanitize(self.request.get('storeLink'))
        s_link = _productconfig.store_link
        
        if s_name and s_url:
            if not s_price:
                s_price = "0.0"
            try:
                s_price = float(s_price)
            except ValueError:
                s_price= 0.0
            if s_link:
                s_link.name=s_name
                s_link.url=s_url
                s_link.price=s_price
                s_link.put()
            else:
                s_link = entities.StoreLink(name=s_name,
                                            url=s_url,
                                            price=s_price)
                s_link.put()
            _productconfig.store_link = s_link
        else:
            if s_link:
                s_link.delete()
            _productconfig.store_link = None
        
        if self.request.get('displayAmazon'):
            _productconfig.displayAmazon = True
        else:
            _productconfig.displayAmazon = False
        
        _productconfig.put()
        
        # edit product line
        _picture = self.request.get('picturedata')
        _name = bene_util.sanitize(self.request.get('name'))
        _description = bene_util.sanitize(self.request.get('description'))
        _productline = _productconfig.getProductLine()
        if _name != _productline.name or _description != _productline.description or _picture:
            _name_save = _productline.name
            _productline.name = _name
            _productline.description = _description
            if bene_util.doesSimilarProductLineExist(_productline) and _name_save != _productline.name: # already exists
                self.redirect('/editconfig?%s' % urllib.urlencode({'repeatprodname': True, 'id': ID}))
                return
            _productline.addPicture(_picture)
            _productline.put()   
       
        self.redirect('/view?%s' % urllib.urlencode({'id': ID}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedConfigPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return