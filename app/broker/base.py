from abc import ABC, abstractmethod
from app.schemas import OrderRequest


class Broker(ABC):
    @abstractmethod
    def place_market_order(self, order: OrderRequest) -> str:
        raise NotImplementedError
