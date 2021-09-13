from flask import Flask

from routes.database import database
from routes.weather import weather

# Create Flask instance
app = Flask(__name__)


# Check connection route
@app.route('/health-check', methods=['GET'])
def health_check():
    return "Healthy"


# weather routes
app.register_blueprint(database, url_prefix='/database')

# weather routes
app.register_blueprint(weather, url_prefix='/weather')

#  app with a debugger
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
