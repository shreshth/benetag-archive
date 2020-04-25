from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_util
import entities
import os



"""
Creates a form to search for a Product
"""
class CreateProductSearchPage(webapp.RequestHandler):
    def get(self):
        template_values = bene_util.initTemplate(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'searchproduct.html')
        self.response.out.write(template.render(path, template_values))
        return

"""
Page that stores Location in datastore
"""
class SearchResultPage(webapp.RequestHandler):
    def post(self):
        query = bene_util.sanitize(self.request.get('query'))
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['query'] = query
        if (len(query) != 0):
            productlist = entities.ProductLine.all()
            producerlist = entities.Producer.all()
            workerlist = entities.Worker.all()
            locationlist = entities.Location.all()
            
            max_results = 10


            matchesProduct = [p for p in productlist if query.lower() in p.name.lower()]
            template_values['matchesProduct'] = bene_util.bestMatch(query, matchesProduct)[0:max_results]
            
            matchesProducer = [p for p in producerlist if query.lower() in p.name.lower()]
            template_values['matchesProducer'] = bene_util.bestMatch(query, matchesProducer)[0:max_results]
            
            matchesWorker = [p for p in workerlist if query.lower() in p.name.lower()]
            template_values['matchesWorker'] = bene_util.bestMatch(query, matchesWorker)[0:max_results]
            
            matchesLocation = [p for p in locationlist if query.lower() in p.name.lower()]
            template_values['matchesLocation'] = bene_util.bestMatch(query, matchesLocation)[0:max_results]
            
            template_values['allListEmpty'] = False	
            if (not matchesProduct) and (not matchesWorker) and (not matchesLocation) and (not matchesProducer):
                template_values['allListEmpty'] = True 
            path = os.path.join(os.path.dirname(__file__), 'searchresult.html')
            self.response.out.write(template.render(path, template_values))
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'searchproduct.html')
            self.response.out.write(template.render(path, template_values))
