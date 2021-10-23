from flask import Flask
import warnings

from routes.utils import utils
from routes.database import database
from routes.weather import weather

warnings.simplefilter('ignore')

# Create Flask instance
app = Flask(__name__)

# utils routes
app.register_blueprint(utils, url_prefix='/utils')

# database routes
app.register_blueprint(database, url_prefix='/database')

# weather routes
app.register_blueprint(weather, url_prefix='/weather')

#  app with a debugger
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
