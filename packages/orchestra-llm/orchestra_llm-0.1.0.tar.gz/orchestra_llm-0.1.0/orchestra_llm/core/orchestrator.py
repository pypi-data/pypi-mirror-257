from fastapi import FastAPI
from langserve import add_routes

class Orchestrator:

    def __init__(self, host: str, port: int, url, **kwargs) -> None:
        self.host = host
        self.port = port
        self.url = url
        self.kwargs = kwargs

    def run(self, debug: bool = False):
        app = FastAPI(
            title="LangChain Server",
            version="1.0",
            description="A simple api server using Langchain's Runnable interfaces",
        )
        for route in self.url.to_json():
            add_routes(app, route["kwargs"]["composer"], path=route["kwargs"]['path'])
        # print(self.url.to_json())
        import uvicorn

        uvicorn.run(app, host=self.host, port=self.port)
        print(f"orchestrator running on {self.host}:{self.port}")