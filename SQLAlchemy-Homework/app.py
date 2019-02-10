# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd

# engine = create_engine("sqlite:///C:/Users/Brian/Desktop/homework_problem/hawaii-2.sqlite")
# engine = create_engine("sqlite:///correct_file.sqlite")
from sqlalchemy.pool import SingletonThreadPool #attempt
#engine = create_engine("sqlite:///hawaii.sqlite", poolclass=SingletonThreadPool)
engine = create_engine("sqlite:///hawaii.sqlite.", connect_args={'check_same_thread':False}, echo=True)
print(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

print(Base)

print(Base.classes.keys())

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return ("Welcome to the Hawaii Trip Planner<br/>"
    "Available routes:<br/>"
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/Start_Date/YYYY-MM-DD<br/>"
    
    "/api/v1.0/Date_Range/YYYY-MM-DD/YYYY-MM-DD (Start date to end date)"  )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #recip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > first_date).order_by(Measurement.date).all()
    #precipitation_df = pd.DataFrame(precip_data, columns=["Date", "Precipitation"]).set_index(['Date'], inplace=True).to_dict()
    #precipitation_df.set_index(['Date'], inplace=True)
    #print(precipitation_df)
    #return jsonify(precipitation_df)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()
    output = pd.DataFrame(results).set_index('date').rename(columns={'prcp': 'precipitation'}).to_dict()
    #print(results)
    return jsonify(output)

@app.route("/api/v1.0/stations")
def stations():
    output1 = list(np.ravel(session.query(Station.name).all()))

    return jsonify(output1)
    
@app.route("/api/v1.0/tobs")
def tobs():
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > first_date).order_by(Measurement.date).all()
    output2 = pd.DataFrame(precip_data).set_index('date').to_dict()
    return jsonify(output2)

@app.route("/api/v1.0/Start_Date/<start>")
def start(start):
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).first()
    #create dictionary from result
    output3 = {"minimum temperuture": temps[0], "maximum temperature": temps[1], "average temperature": temps[2]}
    return jsonify(output3)

@app.route("/api/v1.0/Date_Range/<start>/<end>")
def range(start, end):
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).first()
    #create dictionary from result
    output = {"minimum temperuture": temps[0], "maximum temperature": temps[1], "average temperature": temps[2]}
    return jsonify(output)



if __name__ == "__main__":
    app.run(debug=True)

