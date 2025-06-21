from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI()
app.include_router(router)

def main():
    print("Hello from crud-api-server-python!")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
