from datetime import datetime
from app.broker.base import Broker
from app.schemas import OrderRequest


class PaperBroker(Broker):
    def place_market_order(self, order: OrderRequest) -> str:
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"PAPER-{order.pair}-{order.side}-{ts}"
