# DevbotAPI
This project is a simple API to track who is currently using a dev environment.
Fundamentally it is just a list, with the ability to add and remove users and the accompanying frontend template can be found [here](https://github.com/ozwolf65/devbot).
The project is built using FastAPI and pywebpush, to support the sending of push notifications to subscribed clients.

The dependencies are managed using [poetry](https://python-poetry.org/) and is a recommended prerequisite for working on this project.

## Get Started
To get started, clone the repo and run 
```bash
poetry install
```
to install dependencies or install using the provided `requirements.txt` file.

Then modify the following values in `api.py`:
- ORIGINS: The origins that are allowed to access the API.
- PUBLIC_KEY: Public key for your desired web push service.
- PRIVATE_KEY: Private key for your desired web push service.

Finally start the application locally using:
```bash
poetry shell
uvicorn api:app --host 0.0.0.0 --port 8080
```