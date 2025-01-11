import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import datetime
from sklearn.preprocessing import StandardScaler



def prepare_data(weather_data):#prepare the data for linear regression
    y = np.array([record[6] for record in weather_data])  # Average temperatures its index 6 in the data
    X = np.array(range(1, len(weather_data) + 1)).reshape(-1, 1)  # Day indices reshaped as 2D array
    #because its needed to do the linear regression
    return X, y


def train_model(X, y):
    #trains a linear regression model using the data
    model = LinearRegression()#creates an instance of the LinearRegression class
    model.fit(X, y)#learning the relationship between day and avg temperture
    return model


def predict_next_days(model, start_day, num_days=5):
    #predicts the min,max,avg temp for the next 5 days 
    predictions = []
    for i in range(num_days):
        next_day = start_day + i#calculates the day index for the next prediction
        next_day_features = np.array([[next_day]])#converts to numpy arrey as needed for this model 
        predicted_avg = model.predict(next_day_features)[0]#predicts the avg temp for next day 
        min_temp = predicted_avg - 3  # Estimated min_temp
        max_temp = predicted_avg + 3  # Estimated max_temp
        predictions.append({#append the predictions to the list 
            "date": (datetime.date.today() + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d"),
            "max_temp": max_temp,
            "min_temp": min_temp,
            "avg_temp": predicted_avg
        })
    return predictions


def suggest_activity(avg_temp, clustering_model,scaler):
    
    #Suggest an activity based on the average temperature using K-Means clustering.

    # Predict the cluster for the given average temperature
    cluster = clustering_model.predict(scaler.transform([[avg_temp]]))[0]       
    # Map clusters to activities
    cluster_to_activity = {
        0: "Stay Indoors",
        1: "Outdoor Walk",
        2: "Running",
        3: "Beach Day",
        4: "Outdoor Activities"
    }

    suggested_activity = cluster_to_activity.get(cluster, "No Suitable Activity")

    if avg_temp < 5:
        return "Stay Indoors"  # Very cold temperatures
    elif 5 <= avg_temp < 15:
        return "Running"  
    elif 15 <= avg_temp < 25:
        return "Outdoor Walk"  
    elif 25 <= avg_temp < 35:
        return "Outdoor Activities" 
    elif avg_temp >= 35:
        return "Beach Day"  # Hot temperatures
    
    # Apply fallback rules for extreme temperatures
    if avg_temp < 3:  # Extreme cold
        return "Stay Indoors"
    elif avg_temp > 38:  # Extreme heat
        return "Stay Indoors"
    else:
        # Use K-Means activity for reasonable temperatures
        return suggested_activity


def train_clustering_model(avg_temps, n_clusters=8):
    scaler = StandardScaler()  # Normalize the data
    normalized_temps = scaler.fit_transform(np.array(avg_temps).reshape(-1, 1))

    #Train a K-Means clustering model on average temperatures
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)#creates instance of the kmeans class
    #42 is common use as default
    kmeans.fit(normalized_temps)#Trains the model on average temperatures 

    return kmeans, scaler 
