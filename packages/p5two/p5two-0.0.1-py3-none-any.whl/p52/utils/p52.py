# type: ignore

# here I can define or import those names
# that are modified by the transcrypt compiler
# or that I want to be available inside the sketch without importing
# ie: pop, map, center, etc


# this works because js_pop is defined inside transcrypt itseld
def pop():
    window.js_pop()


def canvas():
    createCanvas(windowWidth, windowHeight)


def center():
    translate(windowWidth / 2, windowHeight / 2)


def map(t, a, b, x, y):
    return (t - a) / (b - a) * (y - x) + x


# empty 'definition' of the injectJs function, which is actually implemented inside the compiler logic
def injectJs(name):
    print(f"injecting {name}")
