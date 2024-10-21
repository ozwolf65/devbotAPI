from fastapi import FastAPI, BackgroundTasks
from models import *
from fastapi.middleware.cors import CORSMiddleware
import time
from pywebpush import webpush, WebPushException
import asyncio

queue: list[str] = []
usages: dict[str, int] = {}
currentUserTime: float = 0.0
subscribers: list[Subscription] = []

# Insert desired URLs here
ORIGINS = []

# Private and public keys for webpush
PRIVATE_KEY = "KEY_HERE"
PUBLIC_KEY = "KEY_HERE"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def notify_users(name: str, change: str):
    """Asynchronously notify all subscribers of a change."""
    for subscriber in subscribers:
        asyncio.create_task(notify(name, change, subscriber))


async def notify(name: str, change: str, subscription: Subscription):
    """Uses webpush to send a notification to a subscriber."""
    data = {
        "subscription": subscription.model_dump(),
        "data": f'{{"name":"{name}","change":"{change}"}}',
        "applicationKeys": {
            "public": PUBLIC_KEY,
            "private": PRIVATE_KEY,
        },
    }
    try:
        webpush(
            subscription_info=data["subscription"],
            data=data["data"],
            vapid_private_key=data["applicationKeys"]["private"],
            vapid_claims={"sub": "mailto:your@email.com"},
        )
    except WebPushException as e:
        if e.response.status_code == 410:
            print("Subscription is expired or no longer in use")
            subscribers.remove(subscription)
            return
        print(f"Error sending push notification", e.message)


@app.get("/queue")
async def get_queue():
    return queue


@app.post("/subscribe")
async def sub_user(body: Subscription):
    if body not in subscribers:
        subscribers.append(body)


@app.post("/queue")
async def add_to_queue(body: RequestBody, background_tasks: BackgroundTasks):
    global currentUserTime
    if body.name not in queue:
        if len(queue) == 0:
            currentUserTime = time.time()
        queue.append(body.name)
        if body.name not in usages.keys():
            usages[body.name] = 0
    background_tasks.add_task(notify_users, body.name, "add")
    return queue


@app.delete("/queue/{name}")
async def delete_from_queue(name: str, background_tasks: BackgroundTasks):
    global currentUserTime
    if name in queue:
        if name == queue[0]:
            # calculate changes to usage stats
            usages[name] += round(time.time() - currentUserTime, 0)
            currentUserTime = time.time()
            # notify next user or alert dev is free
            if len(queue) > 1:
                background_tasks.add_task(notify_users, queue[1], "next")
            else:
                background_tasks.add_task(notify_users, "Nobody!", "next")
        queue.remove(name)
    return queue


@app.get("/usage")
async def get_usages():
    return usages
