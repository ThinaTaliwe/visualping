from app.schemas import TradeDecision, VisualpingEvent


KEYWORD_MAP = {
    "hawkish": ("EUR_USD", "SELL", 0.65),
    "dovish": ("EUR_USD", "BUY", 0.65),
    "inflation rises": ("USD_JPY", "BUY", 0.60),
    "inflation falls": ("USD_JPY", "SELL", 0.60),
}


def classify_event(event: VisualpingEvent) -> TradeDecision | None:
    text = (event.new_text or "").lower()
    for keyword, (pair, side, confidence) in KEYWORD_MAP.items():
        if keyword in text:
            return TradeDecision(
                pair=pair,
                side=side,
                confidence=confidence,
                reason=f"Keyword matched: {keyword}",
            )
    return None
