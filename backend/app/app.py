from fastapi import FastAPI

app = FastAPI()

@app.get("/")

async def check_status():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

