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

    height: Union[int, None] = None
    width: Union[int, None] = None

    negative_prompt: Union[str, None] = None

    num_steps: Union[int, None] = None
    # todo augment


class Default:
    seed = 0
    height = 512
    width = 512
    neg_prompt = ""
    num_steps = 50

@app.post("/generate")
async def generate_images(req: Req):
    print("request received: ", req.height, req.width, req.negative_prompt, req.num_steps)
    
    files = diffusion.upload_to_gcs(
        diffusion.generate(pipeline,
        params,
        prompt=req.prompt,
        seed = req.seed if req.seed else Default.seed,
        height = req.height if req.height else Default.height,
        width = req.width if req.width else Default.width,
        neg_prompt = req.negative_prompt if req.negative_prompt else Default.neg_prompt,
        num_steps= req.num_steps if req.num_steps else Default.num_steps,
        ),

        env.bucket_name,
        storage_client
    )

    return {
        "urls": [f'{env.base_gcs_api_url}/{env.bucket_name}/{file}' for file in files]
    }

if __name__ == "__main__":
    uvicorn.run(app)
