# this is the entry point of the entire package.
# when you `import` this module from the python sketch you end up here
# this script is then responsible to compile to javascript the sketch it was imported from
# and launch the viewer


import inspect
import pathlib

from .compiler import compileSketch, launchRecompilerObserver
from .viewer import launchViewer
from .sketchClass import SketchInfo
from .reloader import launchReloadServer


# get the path of the sketch this script is imported from
importFile = inspect.stack()[-1]
sketchPath = pathlib.Path(importFile.filename).resolve()

# store useful info inside a sketch class (folder, name, temp folder to hold de compiled js and so on)
sketch = SketchInfo(sketchPath)

# launch the compile process
compileSketch(sketch)

# launch the services responsible for auto reload and recompile on save
launchReloadServer()
launchRecompilerObserver(sketch)

# launch the viever
launchViewer(sketch)


# import definition file just to have autocomplete work in the sketch file
from .static.allDefinition import *

# ----

# TODO:
# come far funzionare "pop", "map" e simili (al momento sono metodi di python, non di p5js)?
#    sono riuscito a fare qualcosa dentro utils.p52.
#    al momento ho reimplementato map, ma in questo modo sovrascrivo pymap
#    continuare a testare per capire  se si rompe qualcos'altro

# come integrare eventuali altre librerie javascript??
#    da testare, ma dovrebbe bastare importare il file (import file.js)
#    facendo solo import non funzionerà mai con file js fatti per essere messi in un tag <script>, ma
#    solo con file che fanno export dei loro attributi....

# come modificare comportamenti di p5js direttamente a runtime (ad esempio cambiare le coordinate)?
#    BOH, penso impossibile, bisognerebbe accedere al runtime di p5js... che però mentre sto compilando
#    ancora non esiste...
