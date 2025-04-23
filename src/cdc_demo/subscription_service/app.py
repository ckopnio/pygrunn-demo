import asyncio
import random
from datetime import datetime, timedelta
from numpy.random import choice

from faststream import FastStream, Logger
from faststream.redis import RedisBroker
from faker import Faker
from cdc_demo.model.subscription import Subscription
from cdc_demo.config import Config

config = Config()
fake = Faker()

MIN_INTERVAL = 1
MAX_INTERVAL = 5

SAMPLE_TOPICS = [
    "technology",
    "science",
    "health",
    "sports",
    "business",
    "entertainment",
    "politics",
    "environment",
    "education",
    "travel",
    "food",
    "fashion",
    "music",
    "art",
    "history",
    "finance",
    "gaming",
    "cryptocurrency",
    "sustainability",
    "photography",
]

COUNTRIES = [
    "Luxembourg",
    "Sweden",
    "Ireland",
    "Portugal",
    "Malta",
    "Ukraine",
    "Albania",
    "Latvia",
    "Bosnia and Herzegovina",
    "Cyprus",
    "Algeria",
    "Singapore",
    "Kenya",
    "Gabon",
    "Australia",
    "Belgium",
    "Thailand",
    "Uruguay",
    "United Kingdom",
    "Germany",
    "Canada",
    "Slovenia",
    "Greece",
    "Suriname",
    "Japan",
    "Jamaica",
    "New Zealand",
    "Norway",
    "Tunisia",
    "North Macedonia",
    "Netherlands",
    "Paraguay",
    "Spain",
]

broker = RedisBroker(config.redis_url)
app = FastStream(broker)


def generate_random_subscription() -> Subscription:
    now = datetime.now()
    created_at = now - timedelta(seconds=random.randint(0, 86400))
    return Subscription(
        created_at=created_at,
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_subscribed=choice([True, False], 1, p=[0.7, 0.3]),
        country_name=random.choice(COUNTRIES),
        topics=random.sample(SAMPLE_TOPICS, k=random.randint(1, 5)),
    )


@app.on_startup
async def startup(logger: Logger):
    logger.info("Publisher started")


@app.on_shutdown
async def shutdown(logger: Logger):
    logger.info("Publisher stopped")


@app.after_startup
async def publish_subscription(logger: Logger):
    try:
        while True:
            subscription = generate_random_subscription()

            await broker.publish(subscription, stream=config.stream_name)

            logger.info(f"Published: {subscription}")

            sleep_time = random.uniform(MIN_INTERVAL, MAX_INTERVAL)
            await asyncio.sleep(sleep_time)

    except asyncio.CancelledError:
        logger.info("Publishing task cancelled")
        raise
