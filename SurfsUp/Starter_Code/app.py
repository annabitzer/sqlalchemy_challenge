# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///sqlalchemy_challenge\SurfsUp\Starter_Code\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
######f###########################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available routes."""
    return(
        f"Welcome to the Hawaii climate analysis API!<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"To return all data after a specific date, replace 'start' with desired date in yyyy-mm-dd format.<br>"
        f"/api/v1.0/start<br/>"
        f"To return all data between specific dates, replace 'start' and 'end' with desired date range in yyyy-mm-dd format.<br>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session
    session = Session(engine)

    #return last 12 months of precipitation data in JSON format
    # Perform a query to retrieve the data and precipitation scores

    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    one_year_precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date.desc()).all()

    session.close()

    #create a dictionary from the query data
    precip_data = []
    for date, prcp in one_year_precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation amount"] = prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    #Create session
    session = Session(engine)

    #query all info from the station table
    stations = session.query(Station.id, 
                             Station.station, 
                             Station.name,
                             Station.latitude,
                             Station.longitude,
                             Station.elevation).all()
    
    session.close()

    #convert list of tuples to normal list
    stations_info = list(np.ravel(stations))

    #Return a JSON list of stations from the dataset.
    return jsonify(stations_info)

@app.route("/api/v1.0/tobs")
def temperature():
    #Create session
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    #define the station with most data points (determined in climate analysis)
    main_station = 'USC00519281'

    # Perform a query to retrieve the date and temperature
    one_year_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == main_station).\
        filter(Measurement.date >= year_ago).all()

    session.close()

    #create a dictionary from the query data
    temp_data = []
    for date, tobs in one_year_temp:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = tobs
        temp_data.append(temp_dict)

    #return last 12 months of temperature data in JSON format
    return jsonify(temp_data)

@app.route("/api/v1.0/<start_date>")
def temp(start_date):
     #Create session
    session = Session(engine)

    #find data after the given start date        
    temp_messy = session.query(func.min(Measurement.tobs),
                              func.avg(Measurement.tobs),
                              func.max(Measurement.tobs)).\
                             filter(Measurement.date >= start_date).all()
    
    session.close()

    temp_clean = list(np.ravel(temp_messy))

    return jsonify(f'The min, mean and max temps after the selected date are: {temp_clean}')
                
@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_range(start_date, end_date):
     #Create session
    session = Session(engine)

    #find data after the given start date        
    temp_messy = session.query(func.min(Measurement.tobs),
                              func.avg(Measurement.tobs),
                              func.max(Measurement.tobs)).\
                             filter(Measurement.date >= start_date).\
                             filter(Measurement.date <= end_date).all()
    
    session.close()

    temp_clean = list(np.ravel(temp_messy))

    return jsonify(f'The min, mean and max temps for the selected date range are: {temp_clean}')
    
if __name__ == '__main__':
    app.run(debug=True)