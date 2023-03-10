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
        f"List of Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"for the next API call, after the / Please enter the date as YYYY/MM/DD!<br>"
        f"/api/v1.0/<start><br/>"
        f"for the next API call, after the / Please enter the date as YYYY/MM/DD for both dates in the range!<br>"
        f"/api/v1.0/<start>/<end><br/>"

 )

## Define Routes

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    Last_Year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= Last_Year).all()
    precipitation = {date: prcp for date, prcp in results}
    session.close()
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
     session = Session(engine)
     results = session.query(Station.station).all()
     stations = list(np.ravel(results))
     session.close()
     return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
       session = Session(engine)
       Last_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
       results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= Last_year).all()
       Temps = list(np.ravel(results))
       session.close()
       return jsonify(Temps)


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    Results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    stats = {
        "Min Temperature": Results[0][0],
        "Avg Temperature": Results[0][1],
        "Max Temperature": Results[0][2]
    }
    session.close()
    return jsonify(stats)




@app.route("/api/v1.0/<start>/<end>")
def End(start, end):
    session = Session(engine)
    Results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    stats = {
        "Min Temperature": Results[0][0],
        "Avg Temperature": Results[0][1],
        "Max Temperature": Results[0][2]
    }
    session.close()
    return jsonify(stats)



if __name__ == '__main__':
    app.run(debug=True)