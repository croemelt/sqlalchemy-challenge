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

    )

@app.route("/api/v1.0/precipitation/")
def precipitation():
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


if __name__ == '__main__':
    app.run(debug=True)
