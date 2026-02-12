from fastapi import FastAPI

app=FastAPI(title="Papi's pet API")

@app.get("/")
def root():
    return {"message":"Papi's pet running"}

@app.get("/health")
def health_check():
    return {"Status": "OK"}