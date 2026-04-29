from fastapi import FastAPI

app = FastAPI()


@app.get("/api/hello")
def hello() -> dict:
    return {"message": "hello"}


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
