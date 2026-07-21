from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Test")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)