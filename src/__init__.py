from flask import Flask

#Create all routes
from .routes import twitter_auth

app = Flask(__name__)

#define the initial app
def init_app(config):
  app.config.from_object(config)
  
  #blue prints
  app.register_blueprint(twitter_auth.routes, url_prefix='/twitter')
  
  return app