# Import Dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# Database Setup
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
# Reflect existing database into a new model
Base = automap_base()
# Reflect tables
Base.prepare(engine, reflect=True)
# View all classes
Base.classes.keys()
# Save to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create link
session = Session(engine)
# Setup Flask
app = Flask(__name__)


# Define homepage 
@app.route("/")
def home():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"   

 )

## Define Precipitation

@app.route("/api/v1.0/precipitation")
def precipitation():
    Last_Year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= Last_Year).all()
    precipitation = {date: prcp for date, prcp in results}
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
     results = session.query(Station.station).all()
     stations = list(np.ravel(results))
     return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
       Last_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
       results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= Last_year).all()
       Temps = list(np.ravel(results))
       return jsonify(Temps)

@app.route("/api/v1.0/<start>")
def start(start):
    Results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    stats = {
        "Minimum Temperature": Results[0][0],
        "Average Temperature": Results[0][1],
        "Maximum Temperature": Results[0][2]
    }
    return jsonify(stats)



@app.route("/api/v1.0/<start>/<end>")





##if __name__ == '__main__':
    ##app.run(debug=True)