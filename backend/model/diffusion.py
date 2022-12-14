import jax
import numpy as np
import jax.numpy as jnp
from typing import List
import threading

from pathlib import Path
from jax import pmap
from flax.jax_utils import replicate
from flax.training.common_utils import shard
from PIL import Image

from diffusers import FlaxStableDiffusionPipeline
import huggingface_hub
import uuid
import io



def init(token):
    num_devices = jax.device_count()
    device_type = jax.devices()[0].device_kind

    print(f"Found {num_devices} JAX devices of type {device_type}.")
    assert "TPU" in device_type, "Available device is not a TPU, please select TPU"


    huggingface_hub.login(token)    

    pipeline, params = FlaxStableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        revision="bf16",
        dtype=jnp.bfloat16,
    )

    """
    Model parameters and inputs have to be replicated across the 8 parallel devices we have.
    The parameters dictionary is replicated using flax.jax_utils.replicate, which traverses the
    dictionary and changes the shape of the weights so they are repeated 8 times. Arrays are
    replicated using shard.
    """
    params = replicate(params)

    return pipeline, params


def create_key(seed=0):
    return jax.random.PRNGKey(seed)

def generate(pipeline, params, prompt: str, height=512, width=512, neg_prompt="", num_steps=50, seed = 0):
    rng = create_key(seed)
    rng = jax.random.split(rng, jax.device_count())

    prompt = [prompt] * jax.device_count()
    prompt_ids = pipeline.prepare_inputs(prompt)
    prompt_ids = shard(prompt_ids)

    images = pipeline(prompt_ids, params, rng, jit=True, negative_prompt=neg_prompt, height=height, width=width, num_inference_steps=num_steps).images

    images = images.reshape((images.shape[0] * images.shape[1], ) + images.shape[-3:])

    images = pipeline.numpy_to_pil(images)
    
    return images


def store(content, filename, bkt):
    inmem = io.BytesIO()
    content.save(inmem, "png")
    
    bkt.blob(filename).upload_from_string(inmem.getvalue())


def upload_to_gcs(images, bucket_name, storage_client):
    bkt = storage_client.bucket(bucket_name)
    filenames = []

    # upload in parallel threads
    threads = list()
    for image in images:
        filename = f'{str(uuid.uuid4())}.png'

        t = threading.Thread(target=store, args=(image, filename, bkt,))
        threads.append(t)
        t.start()        
        filenames.append(filename)
    
    # wait until all of them are done
    for t in threads:
        t.join()
    
    return filenames


def warmup(pipeline, params):
    static_prompt = """
        A cinematic film still of Morgan Freeman starring as Jimi Hendrix, portrait, 40mm lens, shallow depth of field, close up, split lighting, cinematic
    """
    generate(pipeline, params, static_prompt, height=768, width=512)
    generate(pipeline, params, static_prompt, height=512, width=512)
    generate(pipeline, params, static_prompt, height=384, width=512)
