CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_subscribed BOOLEAN NOT NULL DEFAULT TRUE,
    country_name VARCHAR(255) NOT NULL,
    topics TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ingested_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_subscriptions_email ON subscriptions(email);
CREATE INDEX IF NOT EXISTS idx_subscriptions_created_at ON subscriptions(created_at);
CREATE INDEX IF NOT EXISTS idx_subscriptions_ingested_at ON subscriptions(ingested_at);

CREATE TABLE IF NOT EXISTS subscription_statistics (
    id SERIAL PRIMARY KEY,
    is_subscribed BOOLEAN NOT NULL,
    country_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    subscribed_on_holiday BOOLEAN NOT NULL,
    continent VARCHAR(100) NOT NULL,
    day_part VARCHAR(50) NOT NULL,
    country_code VARCHAR(10) NOT NULL,
    ingested_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_statistics_created_at ON subscription_statistics(created_at);
CREATE INDEX IF NOT EXISTS idx_statistics_country_code ON subscription_statistics(country_code);
GRANT ALL PRIVILEGES ON TABLE subscription_statistics TO postgres;

CREATE TABLE IF NOT EXISTS subscription_topics (
    id SERIAL PRIMARY KEY,
    subscription_statistic_id INTEGER NOT NULL REFERENCES subscription_statistics(id) ON DELETE CASCADE,
    topic VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_topic_name ON subscription_topics(topic);
GRANT ALL PRIVILEGES ON TABLE subscription_topics TO postgres;

GRANT ALL PRIVILEGES ON TABLE subscriptions TO postgres;
GRANT USAGE, SELECT ON SEQUENCE subscriptions_id_seq TO postgres;