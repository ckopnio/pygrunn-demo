from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    redis_url: str = "redis://redis:6379"
    stream_name: str = "subscriptions"
    statistics_stream_name: str = "subscriptions_statistics"
    sink_consumer_group: str = "subscriptions-sink"
    enrichment_consumer_group: str = "subscriptions-enrichment"

    pg_host: str = "subscription_db"
    pg_port: int = 5432
    pg_user: str = "postgres"
    pg_password: str = "postgres"
    pg_database: str = "subscriptions"

    model_config = SettingsConfigDict(env_prefix="PYGRUNN_", env_file=".env", env_file_encoding="utf-8", extra="ignore")
