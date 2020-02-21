import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Prior year placeholder
year_prior = dt.datetime(2016, 8, 23)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(start_date)<br/>"
        f"/api/v1.0/(start_date)/(end_date)<br/>"
        f"----------------------------<br/>"
        f"Accepted date format as YYYY-MM-DD<br/>"
        f"----------------------------<br/>"
        f"Data available from 2010-01-01 to 2017-08-23 <br/>"

    )

@app.route("/api/v1.0/stations/")
def station():
    session = Session(engine)

    results = session.query(Station.station, Station.name)

    session.close()

    all_stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp, Measurement.station).all()

    session.close()

    precips = []
    for date, prcp, station in results:
        precips_dict = {}
        precips_dict["date"] = date
        precips_dict["precipitation"] = prcp
        precips_dict["station"] = station
        precips.append(precips_dict)

    return jsonify(precips_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date > year_prior).order_by(Measurement.date).all()

    session.close()

    temps = []
    for date, tobs, station in results:
        tobs_dict = {}
        precips_dict = {}
        precips_dict["date"] = date
        precips_dict["temperature"] = tobs
        precips_dict["station"] = station
        temps.append(tobs_dict)

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    dates = []                       
    for x in results:
        date_dict = {}
        date_dict["Date"] = x[0]
        date_dict["Low Temp"] = x[1]
        date_dict["Avg Temp"] = x[2]
        date_dict["High Temp"] = x[3]
        dates.append(date_dict)
    
    return jsonify(dates)    

@app.route('/api/v1.0/datesearch/<startDate>/<endDate>')
def start_end (start, end):

    session = Session(engine)
    
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    dates = []                       
    for y in results:
        date_dict = {}
        date_dict["Date"] = y[0]
        date_dict["Low Temp"] = y[1]
        date_dict["Avg Temp"] = y[2]
        date_dict["High Temp"] = y[3]
        dates.append(date_dict)
    
    return jsonify(dates) 


if __name__ == '__main__':
    app.run(debug=True)
