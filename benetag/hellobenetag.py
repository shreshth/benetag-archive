from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import about
import apolis_view_config
import apolis_view_location
import apolis_view_path
import apolis_view_product
import apolis_view_productgeneric
import apolis_view_unit
import closet_add
import closet_rem
import consumer_home
import create_badge
import create_config
import create_consumer
import create_location
import create_producer
import create_product
import create_qr
import create_units
import create_worker
import delete_config
import delete_line
import delete_location
import delete_unit
import delete_worker
import edit_config
import edit_consumer
import edit_location
import edit_producer
import edit_product
import edit_rating
import edit_worker
import home
import logout
import not_found
import producer_home
import search_product
import send_message_producer
import signup
import view_closet
import view_config
import view_consumer
import view_image
import view_location
import view_msg_inbox
import view_msg_outbox
import view_myprofile
import view_path
import view_producer
import view_producerlocations
import view_producerproducts
import view_producerworkers
import view_product
import view_productgeneric
import view_productworkers
import view_tutorial
import view_unit
import view_worker

application = webapp.WSGIApplication([
  # home pages
  ('/', home.HomePage),
  ('/signup', signup.Signup), 
  ('/logout', logout.Logout),
  ('/producerhome', producer_home.ProducerHomePage),
  ('/consumerhome', consumer_home.ConsumerHomePage), 
  ('/about', about.AboutPage),
  ('/myprofile', view_myprofile.ViewMyProfile),
  
  # create, edit and view consumer page and related entities
  ('/createconsumer', create_consumer.CreateConsumerPage),
  ('/storeconsumer', create_consumer.StoreConsumerPage),
  ('/editconsumer', edit_consumer.EditConsumerPage),
  ('/storeeditedconsumer', edit_consumer.StoreEditedConsumerPage),
  ('/viewconsumer', view_consumer.ViewConsumer),
  #('/myconsumerprofile', view_consumer.ViewMyConsumer),
  # closet
  ('/addtocloset', closet_add.AddToCloset),
  ('/removefromcloset', closet_rem.RemFromCloset),
  ('/viewcloset', view_closet.ViewCloset),
  ('/mycloset', view_closet.ViewMyCloset),
  ('/myinbox', view_msg_inbox.MyInbox),
  
  # create, edit and view producer page, and relevant entities
  ('/createproducer', create_producer.CreateProducerPage),
  ('/storeproducer', create_producer.StoreProducerPage),
  ('/editproducer', edit_producer.EditProducerPage),
  ('/storeeditedproducer', edit_producer.StoreEditedProducerPage),
  ('/viewproducer', view_producer.ViewProducer),
  ('/viewproducerworkers', view_producerworkers.ViewProducerWorkers),
  ('/viewproducerlocations', view_producerlocations.ViewProducerLocations),
  ('/viewproducerproducts', view_producerproducts.ViewProducerProducts),
  #('/myproducerprofile', view_producer.ViewMyProducer),
  ('/myworkers', view_producerworkers.ViewMyWorkers),
  ('/mylocations', view_producerlocations.ViewMyLocations),
  ('/myproducts', view_producerproducts.ViewMyProducts),
  ('/producerwritemsg', send_message_producer.WriteMessageProducer),
  ('/producersendmsg', send_message_producer.SendMessageProducer),
  ('/myoutbox', view_msg_outbox.MyOutbox),  
  
  # generic view for lines, units, configs
  ('/view', view_productgeneric.View),
  
  # create, view delete product line
  ('/createproduct', create_product.CreateProductPage),
  ('/storeproduct', create_product.StoreProductPage),
  ('/editproduct', edit_product.EditLinePage),
  ('/storeeditedproduct', edit_product.StoreEditedLinePage),
  ('/deleteline', delete_line.DeleteLinePage),
  ('/viewproduct', view_product.ViewProduct),
    
  # create, edit, view, delete product config
  ('/createconfig', create_config.CreateConfigPage),
  ('/storeconfig', create_config.StoreConfigPage),
  ('/editconfig', edit_config.EditConfigPage),
  ('/storeeditedconfig', edit_config.StoreEditedConfigPage),
  ('/deleteconfig', delete_config.DeleteConfigPage),
  ('/viewconfig', view_config.ViewConfig),
  
  # create view, delete product unit
  ('/createunits', create_units.CreateUnitsPage),
  ('/storeunits', create_units.StoreUnitsPage),
  ('/deleteunit', delete_unit.DeleteUnitPage),
  ('/viewunit', view_unit.ViewUnit),
  
  # Apolis pages
  ('/apolis_viewproduct', apolis_view_product.ViewProduct),
  ('/apolis_viewconfig', apolis_view_config.ViewConfig),
  ('/apolis_viewunit', apolis_view_unit.ViewUnit),
  ('/apolis_viewlocation', apolis_view_location.ViewLocation),
  ('/apolis_viewpath', apolis_view_path.ViewPath),
  ('/apolis_view', apolis_view_productgeneric.View),
  
  
  # config-related  
  ('/viewproductworkers', view_productworkers.ViewProductWorkers),
  ('/viewpath', view_path.ViewPath),
  ('/changerating', edit_rating.ChangeRating),
                                      
  # create and edit location
  ('/createlocation', create_location.CreateLocationPage),
  ('/storelocation', create_location.StoreLocationPage),
  ('/editlocation', edit_location.EditLocationPage),
  ('/storeeditedlocation', edit_location.StoreEditedLocationPage),
  ('/deletelocation', delete_location.DeleteLocationPage),
  ('/viewlocation', view_location.ViewLocation),
  
  # create and edit worker
  ('/createworker', create_worker.CreateWorkerPage),
  ('/storeworker', create_worker.StoreWorkerPage),
  ('/editworker', edit_worker.EditWorkerPage),
  ('/storeeditedworker', edit_worker.StoreEditedWorkerPage),
  ('/deleteworker', delete_worker.DeleteWorkerPage),
  ('/viewworker', view_worker.ViewWorker),
  
  # create badge
  ('/createbadge', create_badge.CreateBadgePage),
  ('/storebadge', create_badge.StoreBadgePage),
  
  # image retrieval
  ('/productimage', view_image.ProductImage),
  ('/workerimage', view_image.WorkerImage),
  ('/locationimage', view_image.LocationImage),
  ('/badgeimage', view_image.BadgeImage),    
  ('/producerimage', view_image.ProducerImage),
  ('/consumerimage', view_image.ConsumerImage),                      
  
  # search
  ('/searchproduct', search_product.CreateProductSearchPage),
  ('/productsearchresult', search_product.SearchResultPage),
  
  # misc
  ('/qr', create_qr.CreateQrPage),
  ('/producertutorial', view_tutorial.ProducerTutorial),
  ('/consumertutorial', view_tutorial.ConsumerTutorial),
  ('/.*', not_found.NotFound),
  
  
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
