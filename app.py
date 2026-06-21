from flask import Flask,render_template,request
from flask_cors import cross_origin
import pickle
import sklearn
import pandas as pd

app=Flask(__name__)
output=0

model=pickle.load(open("flight_rf.pkl","rb"))

@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/predict',methods=["GET","POST"])
@cross_origin()
def predict():
    if request.method=="POST":
        #date_of_journey
        date_dep=request.form["Dep_time"]
        journey_day=int(pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").day)
        journey_month=int(pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").month)

        #departure hour
        dep_hour=int(pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").hour)
        dep_min=int(pd.to_datetime(date_dep,format="%Y-%m-%dT%H:%M").minute)

        #arrival hour
        date_arr=request.form["Arrival_time"]
        arr_hour=int(pd.to_datetime(date_arr,format="%Y-%m-%dT%H:%M").hour)
        arr_min=int(pd.to_datetime(date_arr,format="%Y-%m-%dT%H:%M").minute)

        #duration
        duration_hour=abs(arr_hour-dep_hour)
        duration_min=abs(arr_min-dep_min)

        total_stops=int(request.form["stops"])

        airline=request.form["airline"]

        if airline=='Jet Airways':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 1
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline=='Air India':
            Airline_AirIndia = 1
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline=='IndiGo':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 1
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline=='GoAir':
            Airline_AirIndia = 0
            Airline_GoAir = 1
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline=='Multiple carriers':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 1
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline=='SpiceJet':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 1
            Airline_Vistara = 0
            Airline_Other = 0
        elif airline=='Vistara':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 1
            Airline_Other = 0
        else:
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 1
        
        source=request.form["Source"]
        if source == 'Delhi':
            Source_Delhi = 1
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0
        elif source=='Kolkata':
            Source_Delhi = 0
            Source_Kolkata = 1
            Source_Mumbai = 0
            Source_Chennai = 0
        elif source=='Mumbai':
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 1
            Source_Chennai = 0
        elif source=='Chennai':
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 1
        else:
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0
        
        destination=request.form["Destination"]
        if destination == 'Cochin':
            Destination_Cochin = 1
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        elif destination == 'Delhi':
            Destination_Cochin = 0
            Destination_Delhi = 1
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        elif destination == 'Hyderabad':
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 1
            Destination_Kolkata = 0
        elif destination == 'Kolkata':
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 1
        else:
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

        prediction=model.predict([[
            total_stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arr_hour,
            arr_min,
            duration_hour,
            duration_min,
            Airline_AirIndia,
            Airline_GoAir,
            Airline_IndiGo,
            Airline_JetAirways,
            Airline_MultipleCarriers,
            Airline_Other,
            Airline_SpiceJet,
            Airline_Vistara,
            Source_Chennai,
            Source_Kolkata,
            Source_Mumbai,
            Destination_Cochin,
            Destination_Delhi,
            Destination_Hyderabad,
            Destination_Kolkata,
        ]])

        output=round(prediction[0],2)
        return render_template('index.html',prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template('index.html')
    

if __name__=="__main__":
    app.run(debug=True,port=8000)