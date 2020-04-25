from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from random import randint
import bene_query
import bene_util
import json
import os
import sys
import urllib

sys.path.append(os.path.join(os.path.dirname(__file__), "dlo-bottlenose-a6fb547"))
import bottlenose
import xml.dom.minidom

"""
    View page for the config
"""

class ViewConfig(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: If no ID sent, default to page with all products?
            '''
            self.redirect('/')
            return
        # Fetch the data for this product
        productconfig = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        productline = productconfig.getProductLine()
        
        # Make a dictionary for template
        template_values = bene_util.initTemplate(self.request.uri)
        # generic
        template_values['id'] = ID
        template_values['name'] = productconfig.getName()
        template_values['is_config'] = True
        template_values['is_unit'] = False 
        template_values['producer'] = productconfig.getProducer()
        template_values['rating'] = productconfig.getRoundedRating()
        template_values['productconfig'] = productconfig
        template_values['config_key'] = productconfig.key()
        # urls
        template_values['url'] = self.request.url
        template_values['path'] = "product"
        template_values['qr_url'] = self.request.url.replace('viewpath','qr')
        template_values['image_url'] = self.request.url.replace('viewconfig', 'productimage')
        template_values['comment_url'] = '%s/viewproduct?%s' % (self.request.host_url, urllib.urlencode({'id': productline.key()}))
        # primary location
        _location = productconfig.getPrimaryLocation()
        if _location and _location.location:
            latitude = _location.location.lat
            longitude = _location.location.lon
        else:
            latitude = None
            longitude = None
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['location'] = _location
        
        # worker to display
        _workers = productconfig.getWorkers()
        if _workers.get(): 
            template_values['has_workers'] = True
            workerlist = []
            for _worker in _workers:
                if _worker:
                    workerlist.append(_worker)
            template_values['has_multiple_workers'] = len(workerlist) > 1
            template_values['num_other_workers'] = len(workerlist)-1
            template_values['more_than_one_other'] = len(workerlist) > 2
            template_values['worker'] = workerlist[randint(0, len(workerlist)-1)]
        else:
            template_values['has_workers'] = False
        # badges
        _badges = productconfig.getBadges()
        if _badges:
            template_values['badges'] = _badges
            template_values['has_badges'] = True
        else:
            template_values['has_badges'] = False
        # interaction - producer
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if productconfig.owner == user and bene_query.getCurrentUser().isProducer:
                template_values['enable_rating'] = False
                template_values['can_edit'] = True
                template_values['edit_link'] = '/editconfig?%s' % urllib.urlencode({'id': productconfig.key()})
                template_values['show_qr'] = False
        # interaction - consumer
        template_values['in_closet'] = False
        template_values['add_closet'] = False
        if user:
            if bene_query.getCurrentUser().isConsumer:
                template_values['enable_rating'] = True
                consumer = bene_query.getCurrentConsumer()
                if consumer:
                    if consumer.hasProduct(productconfig.key()):
                        template_values['in_closet'] = True
                        template_values['rem_closet_link'] = '/removefromcloset?%s' % urllib.urlencode({'id': ID})
                    else:
                        template_values['add_closet'] = True
                        template_values['add_closet_link'] = '/addtocloset?%s' % urllib.urlencode({'id': ID})
        
        
        template_values['num_products'] = productconfig.numProducts()
        template_values['closet_count'] = productconfig.getClosetCount()
        num_configs = productline.numConfigs()
        if num_configs == 1: 
            template_values['last_config'] = True
        if num_configs > 1:
            template_values['otherconfig'] = True
            if (num_configs > 2):
                template_values['more_than_one_other_config'] = True
            template_values['num_other_configs'] = num_configs - 1 
            template_values['config_link'] = '/view?%s' % urllib.urlencode({'id': productline.key()})         
    
        if productconfig.displayAmazon:
            template_values['display_amazon'] = True
            # Amazon stuff
            amazon = bottlenose.Amazon("AKIAIT4OSXQMYQB2XLUQ", "RPzfxhl7eEa/NiIcmkNinQ8OG6kTW65M6UrRqFgD", "BeneTag")
            response = amazon.ItemSearch(Keywords = productline.name + " " + productconfig.getProducer().name, ResponseGroup = "Offers,Images,ItemAttributes,Variations", SearchIndex="All")
            dom = xml.dom.minidom.parseString(response)
            totalres =  int(dom.getElementsByTagName("TotalResults")[0].firstChild.nodeValue)
            if totalres > 0:
                if dom.getElementsByTagName("ItemAttributes"):
                    if dom.getElementsByTagName("ItemAttributes")[0].getElementsByTagName("Title"):
                        product_name = dom.getElementsByTagName("ItemAttributes")[0].getElementsByTagName("Title")[0].firstChild.nodeValue
                        if productline.name in product_name:
                            if productconfig.getProducer().name in product_name:
                                if dom.getElementsByTagName("DetailPageURL"):
                                    template_values['AmazonURL'] = dom.getElementsByTagName("DetailPageURL")[0].firstChild.nodeValue
                                if dom.getElementsByTagName("OfferSummary"):
                                    if dom.getElementsByTagName("OfferSummary")[0].getElementsByTagName("LowestNewPrice"):
                                        if dom.getElementsByTagName("OfferSummary")[0].getElementsByTagName("LowestNewPrice")[0].getElementsByTagName("FormattedPrice"):
                                            template_values['price'] =  dom.getElementsByTagName("OfferSummary")[0].getElementsByTagName("LowestNewPrice")[0].getElementsByTagName("FormattedPrice")[0].firstChild.nodeValue 
            
        else:
            template_values['display_amazon'] = False
        
        storeLink = productconfig.store_link
        if storeLink:
            template_values['has_store_link'] = True
            template_values['storeName'] = storeLink.name
            template_values['storeUrl'] = storeLink.url
            template_values['storePrice'] = storeLink.price
        else:
            template_values['has_store_link'] = False
        
        # render
        path = os.path.join(os.path.dirname(__file__), 'viewconfig.html')
        self.response.out.write(template.render(path, template_values))
        return
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewConfig, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return

