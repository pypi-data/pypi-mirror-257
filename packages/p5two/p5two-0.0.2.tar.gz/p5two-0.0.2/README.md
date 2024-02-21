Write your p5js sketches with python and automatically launch them in a new window just by running your script.
* no html
* no javascript
* just python

Also included: autoreload on save!

# Installation
`pip install p5two`


# Usage

open your favourite editor and create a new file `<script.py>` and save it wherever you want

```
from p52 import *

def setup():
    createCanvas(windowWidth, windowHeight)
    stroke(100, 100, 100, 100)
    noFill()


def draw():
    background(51)
    ellipse(mouseX, mouseY, 30, 30)
```

open a terminal, move to the folder where you saved the script and run it with `python3 <script.py>` or just use your editor "run" button if available.

A new window should popup with your sketch!

Bonus: try changing your code and saving, the changes should automatically be reflected in the sketch.


# Extra functionalities
I decided to put some extra functionalities that diverge from standard python and p5js practices because I found them more convenient:
## magic `self`
Tired of having to define vars before `setup()` in order to have them available inside `draw()`? now you can define vars inside a "fake" `self` object like this:
```
from p52 import *

def setup():
    createCanvas(windowWidth, windowHeight)
    stroke(100, 100, 100, 100)
    noFill()
    self.point = (100, 100)


def draw():
    background(51)
    line(0, 0, *self.point)
```

## sketch saving and reloading
when viewing your sketch you can press "s" to save a screenshot of it inside the current folder. Likewise you can press "r" to reload the sketch.

## utility functions
- `canvas()`
creates a canvas without having to specify its dimensions, defaulting to full window size
- `center()`
changes the coordinate system: (0, 0) is now in the center of the sketch and the y-coordinates go upwards

more to come...

## inject js libraries (experimental!)
if you have a js library that you would like to use inside the sketch you can download it and put it into the same folder as your python sketch and use `injectJs('library.js')`. Doing so automatically include the library inside the generated html file.




# How does it work?
This package is heavily inspired by the library pyp5js and leverages transcrypt to compile python to javascript behind the scenes.