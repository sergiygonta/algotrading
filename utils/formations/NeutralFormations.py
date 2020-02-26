from historical_data.Quote import Quote


class NeutralFormations:
    # длинноногий доджи
    def isLeggyDoji(quote: Quote):
        body_length = abs(quote.open_price - quote.close_price)
        body_top = max(quote.open_price, quote.close_price)
        body_bottom = min(quote.open_price, quote.close_price)
        if quote.high_price > body_top and \
                quote.low_price < body_bottom and \
                (body_length == 0 or
                 (min(quote.high_price - body_top, body_bottom - quote.low_price) / body_length > 3)):
            return True
        return False

    # доджи 4 цен
    def isDoji4prices(quote: Quote):
        return quote.low_price == quote.open_price == quote.close_price == quote.high_price
