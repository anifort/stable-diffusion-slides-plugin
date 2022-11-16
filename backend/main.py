import uvicorn
from fastapi import FastAPI
from pydantic import BaseSettings, BaseModel
import os
import json
from model import diffusion
from typing import Union

from google.cloud import storage
from google.oauth2 import service_account




# load env with default
class Environment(BaseSettings):
    app_name: str = "stable_diffusion_"+ os.uname().nodename
    model_token: str = ""
    
    # gcs
    base_gcs_api_url: str = "https://storage.googleapis.com"
    bucket_name: str = "lhw-stable-diffusion"
    project_id: str = "stable-diffusion-368310"

    creds_path: str = "./creds.json"


    class Config:
        env_file = ".env"


env = Environment()
app = FastAPI()

pipeline, params = diffusion.init(env.model_token)

with open(env.creds_path) as source:
    info = json.load(source)
    storage_credentials = service_account.Credentials.from_service_account_info(info)

    storage_client = storage.Client(project=env.project_id, credentials=storage_credentials)

# warm up takes 1-2 mins
diffusion.warmup(pipeline, params)

@app.get("/ping")
def pingH():
    return "pong"


class Req(BaseModel):
    prompt: str
    seed: Union[int, None] = None
    # todo augment

@app.post("/generate")
async def generate_images(req: Req):

    files = diffusion.upload_to_gcs(
        diffusion.generate(pipeline, params, prompt=req.prompt, seed = req.seed if req.seed else 0),
        env.bucket_name,
        storage_client
    )

    return {
        "urls": [f'{env.base_gcs_api_url}/{env.bucket_name}/{file}' for file in files]
    }

if __name__ == "__main__":
    uvicorn.run(app)
