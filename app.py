# Import Dependencies
from flask import Flask, jsonify

import pandas as pd
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func 

# Set-Up Flask
app = Flask(__name__)

# create engine to hawaii.sqlite
dbPath = 'Resources/hawaii.sqlite'
engine = create_engine(f"sqlite:///{dbPath}")

# reflect an existing database into a new model
# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Home Route
@app.route("/")
def home():
    return(
        f"<center><h1>Welcome to the Hawaii Climate Analysis Local API!</h1></center>"
        f"<center><h2>Select from one of the routes:</h2></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/start/end</center>"
        )

# /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    # return the previous year precipitipation results as a json
    previousYear = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previousYear).all()
    session.close()

    # dictionary with the date as the key and prcp as the value (convert to json)
    precipitation = {date: prcp for date, prcp in results}
    return jsonify(precipitation)

# /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    # retrieve station names
    results = session.query(station.station).all()
    session.close()

    stationList = list(np.ravel(results))

    # convert to a json
    return jsonify(stationList)

# /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def temperatures():
    # retrieve temps from the most active station from the past year
    previousYear = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= previousYear).all()
    session.close()

    temperatureList = list(np.ravel(results))
    
    # convert to a Json
    return jsonify(temperatureList)

# /api/v1.0/start/end and /api/v1/0/start routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):
    # select statement
    selection = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    # if statement
    if not end:
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*selection).filter(measurement.date >= startDate).all()
        session.close()
        temperatureList = list(np.ravel(results))
        # convert to a Json
        return jsonify(temperatureList)

    else:
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")
        results = session.query(*selection)\
        .filter(measurement.date >= startDate)\
        .filter(measurement.date <= endDate).all()
        session.close()
        temperatureList = list(np.ravel(results))
        # convert to a Json
        return jsonify(temperatureList)


# App Launcher
if __name__ == '__main__':
    app.run(debug=True)
    


