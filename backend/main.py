from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI()
app.include_router(router)

def main():
    print("Hello from crud-api-server-python!")
    # Optionally, you can run the server here for local development
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
