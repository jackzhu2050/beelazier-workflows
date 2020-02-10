import sys
from libs.workflow import Workflow, ICON_WEB, web
from libs.alpha_vantage.timeseries import TimeSeries

API_KEY = 'your-pinboard-api-key'


def main(wf):

    ts = TimeSeries(key=API_KEY)
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_intraday('GOOGL')

    for post in posts:
        wf.add_item(title=post['description'],
                    subtitle=post['href'],
                    icon=ICON_WEB)

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))