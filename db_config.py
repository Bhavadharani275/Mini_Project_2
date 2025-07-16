import mysql.connector 
import pandas as pd 

def load_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Bird_Species_data"  
    )
    
    query = "SELECT * FROM Species_analysis"
    df = pd.read_sql(query, connection)
    connection.close()
    return df