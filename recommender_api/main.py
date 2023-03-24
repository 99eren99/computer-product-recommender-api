import os
import logging
from flask import Flask, jsonify
from api.config.config import DevelopmentConfig,TestingConfig,ProductionConfig
from api.utils.database import db
from api.utils.serializer_deserializer import ma
from api.routes.db_update import db_update_routes

app=Flask(__name__)

app.register_blueprint(db_update_routes, url_prefix="/api/db")

logging.basicConfig(filename = 'log_records.log', level=logging.INFO, 
    format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s') 

if os.environ.get("WORK_ENV")=="PROD":
    app_config = ProductionConfig
elif os.environ.get("WORK_ENV")=="TEST":
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)
 
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(port=3333,host="0.0.0.0")

