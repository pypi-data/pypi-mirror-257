import webview
import sys
import base64
import datetime


class App:
    def __init__(self, sketch):
        self.sketch = sketch

    def save(self, data):
        timestamp = datetime.datetime.now().timestamp()
        fileName = f"{self.sketch.barename}_{timestamp:.0f}.png"

        imgdata = base64.b64decode(data.replace("data:image/png;base64,", ""))
        with open(self.sketch.folder / fileName, "wb") as f:
            f.write(imgdata)


def launchViewer(sketch):
    def on_closing():
        # minimize traceback output as it is a 'fake' exception
        sys.tracebacklimit = 0
        raise Exception("Quitting!")

    # optional window size read from command line
    try:
        width, height = int(sys.argv[1]), int(sys.argv[2])
    except:
        width, height = 1200, 800

    window = webview.create_window(sketch.barename, url=str(sketch.indexFile), js_api=App(sketch), width=width, height=height)
    window.events.closing = window.events.closing + on_closing
    webview.start(debug=True, http_server=True)
