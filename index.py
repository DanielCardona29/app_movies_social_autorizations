from config import config
from src import init_app
import sys

if len(sys.argv) > 1:
  configurations = config[sys[1:]]
else:
  configurations = config['develop']
  
app = init_app(configurations)

if __name__ == '__main__':
  app.run();