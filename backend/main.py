from fastapi import FastAPI

app = FastAPI(
    title="Research Paper Assistant",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to the Research Paper Assistant API!"
    }

@app.get("/health")
def health():
    return {
        "status": "Server is running successfully!"
    }