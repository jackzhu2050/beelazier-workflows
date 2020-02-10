import sys
from workflow import Workflow, ICON_WEB, web
import workflow
import os

API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')


def get_exchange_rate(symbol):
    from_symbol, to_symbol = symbol[:3], symbol[3:]
    params = {
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "API_KEY": API_KEY,
    }
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_symbol}&to_currency={to_symbol}&apikey={API_KEY}".format(
        **params)
    r = web.get(url)
    r.raise_for_status()
    result = r.json()["Realtime Currency Exchange Rate"]
    # sample response
    # {
    #     "Realtime Currency Exchange Rate": {
    #         "1. From_Currency Code": "BTC",
    #         "2. From_Currency Name": "Bitcoin",
    #         "3. To_Currency Code": "CNY",
    #         "4. To_Currency Name": "Chinese Yuan",
    #         "5. Exchange Rate": "69454.92875200",
    #         "6. Last Refreshed": "2020-02-10 07:11:06",
    #         "7. Time Zone": "UTC",
    #         "8. Bid Price": "69447.11014400",
    #         "9. Ask Price": "69454.71932500"
    #     }
    # }
    return {
        'from':
        from_symbol,
        "to":
        to_symbol,
        "rate":
        result["5. Exchange Rate"],
        "updated_at":
        '{} {}'.format(result["6. Last Refreshed"], result["7. Time Zone"]),
    }


def get_results(pairs=None):
    # when there's no argument fed, we show a list of pairs
    if pairs is None:
        pairs = ['USDCNY', 'BTCUSD', 'BTCETH']
    else:
        pairs = [pairs]
    return [get_exchange_rate(pair) for pair in pairs]


def main(wf):
    if len(wf.args):
        symbol = wf.args[0]
        if "null" in symbol:
            symbol = None
    else:
        symbol = None
    if symbol is not None:
        rates = get_results(symbol)
    else:
        rates = wf.cached_data("rates", get_results, max_age=600)
    for rate in rates:
        from_symbol = rate['from'].upper()
        to_symbol = rate['to'].upper()
        wf.add_item(title="1{from}={rate}{to}".format(**rate).upper(),
                    subtitle=rate['updated_at'],
                    arg="https://finance.yahoo.com/quote/{}-{}/".format(
                        from_symbol, to_symbol),
                    valid=True,
                    icon=ICON_WEB)

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
    # print(get_exchange_rate('BTCCNY'))
    # print(get_results())