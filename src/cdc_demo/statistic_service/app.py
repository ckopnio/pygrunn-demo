from faststream import FastStream, Logger
from faststream.redis import RedisBroker, StreamSub

from cdc_demo.model.subscription import Subscription
from cdc_demo.model.subscription_statistic import SubscriptionStatistic
from cdc_demo.config import Config

config = Config()

broker = RedisBroker(config.redis_url)
app = FastStream(broker)


@broker.subscriber(stream=StreamSub(config.stream_name, group=config.enrichment_consumer_group, consumer="1"))
@broker.publisher(stream=config.statistics_stream_name)
async def process_subscription(message: Subscription, logger: Logger):
    logger.info(f"Received subscription: {message}")

    return SubscriptionStatistic.from_subscription(message)


@app.on_startup
async def startup(logger: Logger):
    logger.info("Enrichment consumer started:")


@app.on_shutdown
async def shutdown(logger: Logger):
    logger.info("Enrichment consumer stopped")
