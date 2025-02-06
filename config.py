from decouple import config

class Config():
  SECRET_KEY = config("SECRET_KEY")
  
class DevelopConfig(Config):
  DEBUG=True
  PORT=3000
  
class Master(Config):
  DEBUG=False
  
  
config = {
    'develop': DevelopConfig,
    'master': Master
}