import psycopg2

def getConnectionDB():
    return psycopg2.connect(
        dbname="fraud_detection",
        user="postgres",      
        password="Latifmuhammad13",  
        host="localhost",          
        port="5432"                
    )