FROM python:3.8.15-slim-buster

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install "jax[tpu]>=0.2.16" -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
RUN pip install --upgrade clu
 
COPY . /code

EXPOSE 8080
ENV JAX_PLATFORMS=""

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
