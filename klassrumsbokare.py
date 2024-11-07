from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Classrom(BaseModel):
    bokningsnummer: int
    name: str
    date: dict

#Här lagras ett meddelande som skickas när man besöker hemsidan ("/"). Meddelandet förklarar hur användarna ska använda API
message = {
    "Message": "Use the date format YYYY-MM-DD. Available dates are listed below",
    "URL": "http://127.0.0.1:8000/info"
    }


"""
Vi använder en dictionary för att enkelt kunna hitta information om klassrummen baserat på deras bokningsnummer. 
Det gör att vi kan hålla ordning på flera klassrum och deras tillgängliga datum på ett strukturerat sätt.
"""
klassrum = {
    1:Classrom(bokningsnummer=1, name="C201", date={"2024-11-04": "available", "2024-11-05": "available", "2024-11-06": "available", "2024-11-07": "available", "2024-11-08": "available"}),
    2:Classrom(bokningsnummer=2, name="C202", date={"2024-11-04": "available", "2024-11-05": "available", "2024-11-06": "available", "2024-11-07": "available", "2024-11-08": "available"}),
    3:Classrom(bokningsnummer=3, name="C203", date={"2024-11-04": "available", "2024-11-05": "available", "2024-11-06": "available", "2024-11-07": "available", "2024-11-08": "available"}),
    4:Classrom(bokningsnummer=4, name="C204", date={"2024-11-04": "available", "2024-11-05": "available", "2024-11-06": "available", "2024-11-07": "available", "2024-11-08": "available"}),
    5:Classrom(bokningsnummer=5, name="C205", date={"2024-11-04": "available", "2024-11-05": "available", "2024-11-06": "available", "2024-11-07": "available", "2024-11-08": "available"}),

}

#Den här delen skapar en "get"-route som körs när någon går till hemsidan ("/"). Den skickar tillbaka meddelandet vi definierade tidigare.
@app.get("/")
def homepage():
    return message

#Den här "get"-routen ger information om de olika klassrummen och deras tillgängliga datum
@app.get("/info")
def info():
    return klassrum


#En post endpoint som tar två argument. Ett bokningsnummer och ett datum.
@app.post("/boka/{bokningsnummer}/{datum}")
def boka_klassrum(bokningsnummer: int, datum: str): #Funktion boka_klassrum så tar samma argument som endpointen.
    if bokningsnummer not in klassrum:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    if datum not in klassrum[bokningsnummer].date:
        raise HTTPException(status_code=404, detail="Date not found")
    
    if klassrum[bokningsnummer].date[datum] == "booked":
        raise HTTPException(status_code=400, detail="Classroom on this date is already booked")
    
    """
    Allt ovan är felhantering, 
    Första kontrollen är för att kontrollera ifall användaren försöker boka ett klassrum som inte finns med i klassrum dictionary.
    Andra vilkoret är för att kontrollera att datumet användaren skriver in finns som alternativ.
    Tredje vilkoret är för att kontrollera så att användaren inte kan boka ett klassrum som redan är "booked".

    """
    

    #Denna kod ändrar så att datumet som användaren valt blir "booked" istället för available och returnerar det.
    klassrum[bokningsnummer].date[datum] = "booked"
    return {"Message": f"Classroom {klassrum[bokningsnummer].name}, Date: {datum} booked successfully!"}




@app.put("/change-booking/{bokningsnummer}/{datum}/{nytt_datum}") 
def change_booking(bokningsnummer: int, datum: str, nytt_datum: str): # Funktionen change_booking används för att ändra dag för bokningen
    # Under används flera if-statements för att hantera olika felmeddelanden, de är alla If-statemens för att hanteras separat 
    if bokningsnummer not in klassrum: # Finns inte "bokningsnummer" dict "klassrum" visas felmeddelande
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    if datum not in klassrum[bokningsnummer].date: # Finns "datum" inte i dict"klassrum" visas felmeddelande
        raise HTTPException(status_code=404, detail="Current date not found")
    
    if klassrum[bokningsnummer].date[datum] != "booked": # Finns ingen bokning på vald dag man vill flytta visas felmeddelande
        raise HTTPException(status_code=400, detail="Classroom is not booked on the current day")
    
    if nytt_datum not in klassrum[bokningsnummer].date: # Finns inte det nya valda datumet som alternativ visas felmeddelande
        raise HTTPException(status_code=404, detail="New date not found")
    
    if klassrum[bokningsnummer].date[nytt_datum] == "booked": # Om ny valt datum redan är bokad visas felmeddelande
        raise HTTPException(status_code=400, detail="Classroom is already booked on the new date")
    
    klassrum[bokningsnummer].date[datum] = "available" # Ändrar status på tidigare valt datum till "available"
    klassrum[bokningsnummer].date[nytt_datum] = "booked" # Ändrar statust på nytt valt datum till "booked"
    
    return {"Message": f"Booking changed from {datum} to {nytt_datum} for Classroom {klassrum[bokningsnummer].name}!"} 
    # Om inga av If-statements har uppfyllt och gett felmeddelande visas ett "lyckades meddelande"



#raderar bokning av ett klassrum baserat på bokningsnumret och datum
@app.delete("/raderabokning/{bokningsnummer}/{datum}")
def radera_bokad_tid (bokningsnummer: int, datum: str):

    #om bokningsnumret inte finns i klassrum så returneras ett felmeddelande
    if bokningsnummer not in klassrum:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    #om datumet inte finns i klassrum returneras ett felmeddelande
    if datum not in klassrum[bokningsnummer].date:
        raise HTTPException(status_code=404, detail="Date not found")
    
    #om klassrummet inte är bokat returneras ett felmeddelande
    if klassrum[bokningsnummer].date[datum] == "available":
        raise HTTPException(status_code=400, detail="Classroom on this date is not booked")

    #om klassrum är bokat sätter vi det nu som availible och meddelar användaren att bokningen är borttagen
    klassrum[bokningsnummer].date[datum] = "available"
    return {"Message": f"Classroom {klassrum[bokningsnummer].name}, Date: {datum} booking deleted successfully!"} 