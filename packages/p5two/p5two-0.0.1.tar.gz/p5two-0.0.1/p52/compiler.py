import time
import subprocess
import pathlib
import re
import shutil

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from websockets.sync.client import connect


package_dir = pathlib.Path(__file__).parent.resolve()  # the folder containing the installed package
importPath = package_dir / "utils"  # the folder from which transcrypt can import file
indexFile = package_dir / "static" / "index.html"  # index.html template file

SOCKET_URI = "ws://localhost:8765"


def getJSModules(sketch):
    "return the path of the js modules to inject into the html"
    with open(sketch.path) as src:
        lines = src.readlines()
        injectLines = [l for l in lines if "injectJs" in l and "#" not in l]
        return [re.findall("\((.+)\)", l)[0][1:-1] for l in injectLines]


def injectModules(sketch):
    # copy js modules inside the new folder and prepare the <src> tags to inject inside index.html
    # and return the tags to inject
    modules = getJSModules(sketch)
    moduleSrcTagsList = []
    for module in modules:
        shutil.copy2(sketch.folder / module, sketch.targetFolder)
        moduleSrcTagsList.append(f'<script src="{module}"></script>')

    return "\n".join(moduleSrcTagsList)


def compileSketch(sketch):

    command = f"transcrypt -b -n -m -xr -k {sketch.path} -xp {importPath} -od {sketch.outputFolder}"
    subprocess.run(command, shell=True)

    # copy js modules inside the new folder and prepare the <src> tags to inject inside index.html
    modulesSrcTags = injectModules(sketch)

    with open(indexFile) as inputFile, open(sketch.indexFile, "w") as outputFile:
        index = inputFile.read()
        index = index.replace("{{sketch}}", sketch.namejs)
        index = index.replace("{{scripts}}", modulesSrcTags)
        outputFile.write(index)


class RecompileHandler(FileSystemEventHandler):
    def __init__(self, sketch, function):
        self.last_trigger_time = time.time()
        self.sketch = sketch
        self.function = function

    def on_modified(self, event):
        trigger_time = time.time()
        if trigger_time - self.last_trigger_time > 2:
            self.function(self.sketch)
            with connect(SOCKET_URI) as websocket:
                websocket.send("RELOAD")
            self.last_trigger_time = trigger_time


def launchRecompilerObserver(sketch):
    observer = Observer()
    observer.schedule(RecompileHandler(sketch, compileSketch), sketch.folder, recursive=False)
    observer.start()
