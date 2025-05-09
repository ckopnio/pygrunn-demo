from faststream import FastStream, Logger
from faststream.redis import RedisBroker, StreamSub
import asyncpg

from cdc_demo.model.subscription import Subscription
from cdc_demo.model.subscription_statistic import SubscriptionStatistic
from cdc_demo.config import Config

config = Config()

broker = RedisBroker(config.redis_url)
app = FastStream(broker)

db_pool = None


@broker.subscriber(stream=StreamSub(config.stream_name, group=config.sink_consumer_group, consumer="1"))
async def process_subscription(message: Subscription, logger: Logger):
    try:
        logger.info(f"Received subscription: {message}")
        subscription_id = await save_subscription_to_postgres(message)
        logger.info(f"Saved subscription to database with ID: {subscription_id}")
    except Exception as e:
        logger.error(f"Error processing subscription: {str(e)}")


@broker.subscriber(stream=StreamSub(config.statistics_stream_name, group=config.sink_consumer_group, consumer="2"))
async def process_subscription_statistic(message: SubscriptionStatistic, logger: Logger):
    try:
        logger.info(f"Received subscription statistic: {message}")
        statistic_id = await save_statistic_to_postgres(message)
        logger.info(f"Saved subscription to database with ID: {statistic_id}")
    except Exception as e:
        logger.error(f"Error processing subscription: {str(e)}")


async def save_statistic_to_postgres(statistic: SubscriptionStatistic) -> int:
    if not db_pool:
        raise RuntimeError("Database connection not established")

    query_statistic = """
        INSERT INTO subscription_statistics (
            is_subscribed,
            country_name,
            created_at,
            subscribed_on_holiday,
            continent,
            day_part,
            country_code
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
    """

    query_topic = """
        INSERT INTO subscription_topics (subscription_statistic_id, topic)
        VALUES ($1, $2)
    """

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                query_statistic,
                statistic.is_subscribed,
                statistic.country_name,
                statistic.created_at,
                statistic.subscribed_on_holiday,
                statistic.continent,
                statistic.day_part.value,
                statistic.country_code,
            )
            statistic_id = row["id"]

            for topic in statistic.topics:
                await conn.execute(query_topic, statistic_id, topic)

    return statistic_id


async def save_subscription_to_postgres(subscription: Subscription) -> int:
    if not db_pool:
        raise RuntimeError("Database connection not established")

    query = """
        INSERT INTO subscriptions
        (email, first_name, last_name, is_subscribed, country_name, topics, created_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (email) DO UPDATE SET
            first_name = $2,
            last_name = $3,
            is_subscribed = $4,
            country_name = $5,
            topics = $6,
            created_at = $7
        RETURNING id
    """

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            query,
            subscription.email,
            subscription.first_name,
            subscription.last_name,
            subscription.is_subscribed,
            subscription.country_name,
            subscription.topics,
            subscription.created_at,
        )
        return row["id"]


@app.on_startup
async def startup(logger: Logger):
    global db_pool

    try:
        db_pool = await asyncpg.create_pool(
            host=config.pg_host, port=config.pg_port, user=config.pg_user, password=config.pg_password, database=config.pg_database
        )
        logger.info("Connected to PostgreSQL database")
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

    logger.info("Sink consumer app started")


@app.on_shutdown
async def shutdown(logger: Logger):
    global db_pool

    if db_pool:
        logger.info("Closing database connection...")
        await db_pool.close()
        logger.info("Database connection closed")

    logger.info("Sink consumer app stopped")
