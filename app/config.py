from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FXBOT_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./fxbot.db"
    max_risk_per_trade_pct: float = 0.005
    max_daily_loss_pct: float = 0.02
    max_open_positions: int = 3
    default_order_units: int = 1000
    visualping_webhook_token: str = "change-me"


settings = Settings()
