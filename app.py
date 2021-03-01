import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Calculate the date one year from the last date in data set.
maxdate = '2017-08-23'
#maxdate was '2017-08-23'
mindate = '2016-08-23'

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<startdate><br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipiatation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipiatation data including date"""
    # Query all passengers
    data2 = session.query(Measurements.date,Measurements.prcp).group_by(Measurements.date).all()

    session.close()

    # Create a dictionary
    all_precip = []
    for date, prcp in data2:
        precip_dict = {}
        precip_dict[date] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Stations.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temperatures"""
    # Perform a query to retrieve the data and precipitation scores
    data1 = session.query(Measurements.date,Measurements.tobs).\
        filter(Measurements.date < maxdate).\
        filter(Measurements.date > mindate).\
        group_by(Measurements.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(data1))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    """Fetch the date."""
    #dateexists = False
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #for i in Measurements:
    #    if start == Measurements.date:
    #        dateexists = True

    #if dateexists:
    """Date Exists."""
    data3 = session.query(Measurements.date, func.max(Measurements.tobs), func.avg(Measurements.tobs), func.min(Measurements.tobs)).\
        filter(Measurements.date > start).\
        group_by(Measurements.date).all()
    #close session
    session.close()
    # Convert list of tuples into normal list
    all_start = list(np.ravel(data3))

    return jsonify(all_start)
    #close session
    #session.close()
    #return jsonify({"error": f"Start Date {start} not found."}), 404

@app.route("/api/v1.0/<start>/<end>")
def end_date(start, end):
    """Fetch the date."""
    #startdateexists = False
    #enddateexists = False
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #for i in Measurements:
    #    if start == Measurements.date:
    #       """Start Date Exists."""
    #       startdateexists = True
    #   if end == Measurements.date:
    #        """End Date Exists."""
    #        enddateexists = True

    #if startdateexists and enddateexists:
    data4 = session.query(Measurements.date, func.max(Measurements.tobs), func.avg(Measurements.tobs), func.min(Measurements.tobs)).\
        filter(Measurements.date < end).\
        filter(Measurements.date > start).\
        group_by(Measurements.date).all()
    #close session
    session.close()
    # Convert list of tuples into normal list
    all_startend = list(np.ravel(data4))

    return jsonify(all_startend)
    #close session
    #session.close()
    #if startdateexists:
    #    """End Date Must not exist."""
    #    return jsonify({"error": f"End Date {end} not found."}), 404
    #if enddateexists:
    #    """Start Date Must not exist."""
    #    return jsonify({"error": f"Start Date {start} not found."}), 404
    #return jsonify({"error": f"Start or End Date not found {start} {end}."}), 404


if __name__ == '__main__':
    app.run(debug=True)
