# type: ignore


def describe(text, display):
    """Creates a screen reader-accessible description for the canvas.
    The first parameter, text, is the description of the canvas.
    The second parameter, display, is optional. It determines how the
    description is displayed. If LABEL is passed, as in
    describe('A description.', LABEL), the description will be visible in
    a div element next to the canvas. If FALLBACK is passed, as in
    describe('A description.', FALLBACK), the description will only be
    visible to screen readers. This is the default mode.
    Read
    How to label your p5.js code to
    learn more about making sketches accessible."""
    pass


def describeElement(name, text, display):
    """Creates a screen reader-accessible description for elements in the canvas.
    Elements are shapes or groups of shapes that create meaning together.
    The first parameter, name, is the name of the element.
    The second parameter, text, is the description of the element.
    The third parameter, display, is optional. It determines how the
    description is displayed. If LABEL is passed, as in
    describe('A description.', LABEL), the description will be visible in
    a div element next to the canvas. Using LABEL creates unhelpful
    duplicates for screen readers. Only use LABEL during development. If
    FALLBACK is passed, as in describe('A description.', FALLBACK), the
    description will only be visible to screen readers. This is the default
    mode.
    Read
    How to label your p5.js code to
    learn more about making sketches accessible."""
    pass


def textOutput(display):
    """Creates a screen reader-accessible description for shapes on the canvas.
    textOutput() adds a general description, list of shapes, and
    table of shapes to the web page.
    The general description includes the canvas size, canvas color, and number
    of shapes. For example,
    Your output is a, 100 by 100 pixels, gray canvas containing the following 2 shapes:.
    A list of shapes follows the general description. The list describes the
    color, location, and area of each shape. For example,
    a red circle at middle covering 3% of the canvas. Each shape can be
    selected to get more details.
    textOutput() uses its table of shapes as a list. The table describes the
    shape, color, location, coordinates and area. For example,
    red circle location = middle area = 3%. This is different from
    gridOutput(), which uses its table as a grid.
    The display parameter is optional. It determines how the description is
    displayed. If LABEL is passed, as in textOutput(LABEL), the description
    will be visible in a div element next to the canvas. Using LABEL creates
    unhelpful duplicates for screen readers. Only use LABEL during
    development. If FALLBACK is passed, as in textOutput(FALLBACK), the
    description will only be visible to screen readers. This is the default
    mode.
    Read
    How to label your p5.js code to
    learn more about making sketches accessible."""
    pass


def gridOutput(display):
    """Creates a screen reader-accessible description for shapes on the canvas.
    gridOutput() adds a general description, table of shapes, and list of
    shapes to the web page.
    The general description includes the canvas size, canvas color, and number of
    shapes. For example,
    gray canvas, 100 by 100 pixels, contains 2 shapes:  1 circle 1 square.
    gridOutput() uses its table of shapes as a grid. Each shape in the grid
    is placed in a cell whose row and column correspond to the shape's location
    on the canvas. The grid cells describe the color and type of shape at that
    location. For example, red circle. These descriptions can be selected
    individually to get more details. This is different from
    textOutput(), which uses its table as a list.
    A list of shapes follows the table. The list describes the color, type,
    location, and area of each shape. For example,
    red circle, location = middle, area = 3 %.
    The display parameter is optional. It determines how the description is
    displayed. If LABEL is passed, as in gridOutput(LABEL), the description
    will be visible in a div element next to the canvas. Using LABEL creates
    unhelpful duplicates for screen readers. Only use LABEL during
    development. If FALLBACK is passed, as in gridOutput(FALLBACK), the
    description will only be visible to screen readers. This is the default
    mode.
    Read
    How to label your p5.js code to
    learn more about making sketches accessible."""
    pass


def alpha(color):
    """Extracts the alpha (transparency) value from a
    p5.Color object, array of color components, or
    CSS color string."""
    pass


def blue(color):
    """Extracts the blue value from a p5.Color object,
    array of color components, or CSS color string."""
    pass


def brightness(color):
    """Extracts the HSB brightness value from a
    p5.Color object, array of color components, or
    CSS color string."""
    pass


def color(*args, **kwargs):
    """Creates a p5.Color object. By default, the
    parameters are interpreted as RGB values. Calling color(255, 204, 0) will
    return a bright yellow color. The way these parameters are interpreted may
    be changed with the colorMode() function.
    The version of color() with one parameter interprets the value one of two
    ways. If the parameter is a number, it's interpreted as a grayscale value.
    If the parameter is a string, it's interpreted as a CSS color string.
    The version of color() with two parameters interprets the first one as a
    grayscale value. The second parameter sets the alpha (transparency) value.
    The version of color() with three parameters interprets them as RGB, HSB,
    or HSL colors, depending on the current colorMode().
    The version of color() with four parameters interprets them as RGBA, HSBA,
    or HSLA colors, depending on the current colorMode(). The last parameter
    sets the alpha (transparency) value."""
    pass


def green(color):
    """Extracts the green value from a p5.Color object,
    array of color components, or CSS color string."""
    pass


def hue(color):
    """Extracts the hue value from a
    p5.Color object, array of color components, or
    CSS color string.
    Hue exists in both HSB and HSL. It describes a color's position on the
    color wheel. By default, this function returns the HSL-normalized hue. If
    the colorMode() is set to HSB, it returns the
    HSB-normalized hue."""
    pass


def lerpColor(c1, c2, amt):
    """Blends two colors to find a third color between them. The amt parameter
    specifies the amount to interpolate between the two values. 0 is equal to
    the first color, 0.1 is very near the first color, 0.5 is halfway between
    the two colors, and so on. Negative numbers are set to 0. Numbers greater
    than 1 are set to 1. This differs from the behavior of
    lerp. It's necessary because numbers outside of the
    interval [0, 1] will produce strange and unexpected colors.
    The way that colors are interpolated depends on the current
    colorMode()."""
    pass


def lightness(color):
    """Extracts the HSL lightness value from a
    p5.Color object, array of color components, or
    CSS color string."""
    pass


def red(color):
    """Extracts the red value from a
    p5.Color object, array of color components, or
    CSS color string."""
    pass


def saturation(color):
    """Extracts the saturation value from a
    p5.Color object, array of color components, or
    CSS color string.
    Saturation is scaled differently in HSB and HSL. By default, this function
    returns the HSL saturation. If the colorMode()
    is set to HSB, it returns the HSB saturation."""
    pass


def beginClip(options):
    """Start defining a shape that will mask subsequent things drawn to the canvas.
    Only opaque regions of the mask shape will allow content to be drawn.
    Any shapes drawn between this and endClip() will
    contribute to the mask shape.
    The mask will apply to anything drawn after this call. To draw without a mask, contain
    the code to apply the mask and to draw the masked content between
    push() and pop().
    Alternatively, rather than drawing the mask between this and
    endClip(), draw the mask in a callback function
    passed to clip().
    Options can include:

    invert: A boolean specifying whether or not to mask the areas not filled by the mask shape. Defaults to false.
    """
    pass


def endClip(*args, **kwargs):
    """Finishes defining a shape that will mask subsequent things drawn to the canvas.
    Only opaque regions of the mask shape will allow content to be drawn.
    Any shapes drawn between beginClip() and this
    will contribute to the mask shape."""
    pass


def clip(callback, options):
    """Use the shape drawn by a callback function to mask subsequent things drawn to the canvas.
    Only opaque regions of the mask shape will allow content to be drawn.
    The mask will apply to anything drawn after this call. To draw without a mask, contain
    the code to apply the mask and to draw the masked content between
    push() and pop().
    Alternatively, rather than drawing the mask shape in a function, draw the
    shape between beginClip() and endClip().
    Options can include:

    invert: A boolean specifying whether or not to mask the areas not filled by the mask shape. Defaults to false.
    """
    pass


def background(*args, **kwargs):
    """Sets the color used for the background of the canvas. By default, the
    background is transparent. This function is typically used within
    draw() to clear the display window at the beginning
    of each frame. It can also be used inside setup() to
    set the background on the first frame of animation.
    The version of background() with one parameter interprets the value one of four
    ways. If the parameter is a number, it's interpreted as a grayscale value.
    If the parameter is a string, it's interpreted as a CSS color string.  RGB, RGBA,
    HSL, HSLA, hex, and named color strings are supported. If the parameter is a
    p5.Color object, it will be used as the background color.
    If the parameter is a p5.Image object, it will be used as
    the background image.
    The version of background() with two parameters interprets the first one as a
    grayscale value. The second parameter sets the alpha (transparency) value.
    The version of background() with three parameters interprets them as RGB, HSB,
    or HSL colors, depending on the current colorMode().
    By default, colors are specified in RGB values. Calling background(255, 204, 0)
    sets the background a bright yellow color."""
    pass


def clear(r, g, b, a):
    """Clears the pixels on the canvas. This function makes every pixel 100%
    transparent. Calling clear() doesn't clear objects created by createX()
    functions such as createGraphics(),
    createVideo(), and
    createImg(). These objects will remain
    unchanged after calling clear() and can be redrawn.
    In WebGL mode, this function can clear the screen to a specific color. It
    interprets four numeric parameters as normalized RGBA color values. It also
    clears the depth buffer. If you are not using the WebGL renderer, these
    parameters will have no effect."""
    pass


def colorMode(*args, **kwargs):
    """Changes the way p5.js interprets color data. By default, the numeric
    parameters for fill(),
    stroke(),
    background(), and
    color() are defined by values between 0 and 255
    using the RGB color model. This is equivalent to calling
    colorMode(RGB, 255). Pure red is color(255, 0, 0) in this model.
    Calling colorMode(RGB, 100) sets colors to be interpreted as RGB color
    values between 0 and 100.  Pure red is color(100, 0, 0) in this model.
    Calling colorMode(HSB) or colorMode(HSL) changes to HSB or HSL system
    instead of RGB.
    p5.Color objects remember the mode that they were
    created in. Changing modes doesn't affect their appearance."""
    pass


def fill(*args, **kwargs):
    """Sets the color used to fill shapes. Calling fill(255, 165, 0) or
    fill('orange') means all shapes drawn after the fill command will be
    filled with the color orange.
    The version of fill() with one parameter interprets the value one of
    three ways. If the parameter is a number, it's interpreted as a grayscale
    value. If the parameter is a string, it's interpreted as a CSS color
    string. A p5.Color object can also be provided to
    set the fill color.
    The version of fill() with three parameters interprets them as RGB, HSB,
    or HSL colors, depending on the current
    colorMode(). The default color space is RGB,
    with each value in the range from 0 to 255."""
    pass


def noFill(*args, **kwargs):
    """Disables setting the interior color of shapes. This is the same as making
    the fill completely transparent. If both
    noStroke() and
    noFill() are called, nothing will be drawn to the
    screen."""
    pass


def noStroke(*args, **kwargs):
    """Disables drawing the stroke (outline). If both
    noStroke() and
    noFill() are called, nothing will be drawn to the
    screen."""
    pass


def stroke(*args, **kwargs):
    """Sets the color used to draw lines and borders around shapes. Calling
    stroke(255, 165, 0) or stroke('orange') means all shapes drawn after
    the stroke() command will be filled with the color orange. The way these
    parameters are interpreted may be changed with the
    colorMode() function.
    The version of stroke() with one parameter interprets the value one of
    three ways. If the parameter is a number, it's interpreted as a grayscale
    value. If the parameter is a string, it's interpreted as a CSS color
    string. A p5.Color object can also be provided to
    set the stroke color.
    The version of stroke() with two parameters interprets the first one as a
    grayscale value. The second parameter sets the alpha (transparency) value.
    The version of stroke() with three parameters interprets them as RGB, HSB,
    or HSL colors, depending on the current colorMode().
    The version of stroke() with four parameters interprets them as RGBA, HSBA,
    or HSLA colors, depending on the current colorMode(). The last parameter
    sets the alpha (transparency) value."""
    pass


def erase(strengthFill, strengthStroke):
    """All drawing that follows erase() will subtract
    from the canvas, revealing the web page underneath. The erased areas will
    become transparent, allowing the content behind the canvas to show through.
    The fill(), stroke(), and
    blendMode() have no effect once erase() is
    called.
    The erase() function has two optional parameters. The first parameter
    sets the strength of erasing by the shape's interior. A value of 0 means
    that no erasing will occur. A value of 255 means that the shape's interior
    will fully erase the content underneath. The default value is 255
    (full strength).
    The second parameter sets the strength of erasing by the shape's edge. A
    value of 0 means that no erasing will occur. A value of 255 means that the
    shape's edge will fully erase the content underneath. The default value is
    255 (full strength).
    To cancel the erasing effect, use the noErase()
    function.
    erase() has no effect on drawing done with the
    image() and
    background() functions."""
    pass


def noErase(*args, **kwargs):
    """Ends erasing that was started with erase().
    The fill(), stroke(), and
    blendMode() settings will return to what they
    were prior to calling erase()."""
    pass


def arc(x, y, w, h, start, stop, mode, detail):
    """Draws an arc to the canvas. Arcs are drawn along the outer edge of an ellipse
    (oval) defined by the x, y, w, and h parameters. Use the start and stop
    parameters to specify the angles (in radians) at which to draw the arc. Arcs are
    always drawn clockwise from start to stop. The origin of the arc's ellipse may
    be changed with the ellipseMode() function.
    The optional mode parameter determines the arc's fill style. The fill modes are
    a semi-circle (OPEN), a closed semi-circle (CHORD), or a closed pie segment (PIE).
    """
    pass


def ellipse(*args, **kwargs):
    """Draws an ellipse (oval) to the canvas. An ellipse with equal width and height
    is a circle. By default, the first two parameters set the location of the
    center of the ellipse. The third and fourth parameters set the shape's width
    and height, respectively. The origin may be changed with the
    ellipseMode() function.
    If no height is specified, the value of width is used for both the width and
    height. If a negative height or width is specified, the absolute value is
    taken."""
    pass


def circle(x, y, d):
    """Draws a circle to the canvas. A circle is a round shape. Every point on the
    edge of a circle is the same distance from its center. By default, the first
    two parameters set the location of the center of the circle. The third
    parameter sets the shape's width and height (diameter). The origin may be
    changed with the ellipseMode() function."""
    pass


def line(*args, **kwargs):
    """Draws a line, a straight path between two points. Its default width is one pixel.
    The version of line() with four parameters draws the line in 2D. To color a line,
    use the stroke() function. To change its width, use the
    strokeWeight() function. A line
    can't be filled, so the fill() function won't affect
    the color of a  line.
    The version of line() with six parameters allows the line to be drawn in 3D
    space. Doing so requires adding the WEBGL argument to
    createCanvas()."""
    pass


def point(*args, **kwargs):
    """Draws a point, a single coordinate in space. Its default size is one pixel. The first two
    parameters are the point's x- and y-coordinates, respectively. To color a point, use
    the stroke() function. To change its size, use the
    strokeWeight() function.
    The version of point() with three parameters allows the point to be drawn in 3D
    space. Doing so requires adding the WEBGL argument to
    createCanvas().
    The version of point() with one parameter allows the point's location to be set with
    a p5.Vector object."""
    pass


def quad(*args, **kwargs):
    """Draws a quad to the canvas. A quad is a quadrilateral, a four-sided
    polygon. Some examples of quads include rectangles, squares, rhombuses,
    and trapezoids. The first pair of parameters (x1,y1) sets the quad's
    first point. The following pairs of parameters set the coordinates for
    its next three points. Parameters should proceed clockwise or
    counter-clockwise around the shape.
    The version of quad() with twelve parameters allows the quad to be drawn
    in 3D space. Doing so requires adding the WEBGL argument to
    createCanvas()."""
    pass


def rect(*args, **kwargs):
    """Draws a rectangle to the canvas. A rectangle is a four-sided polygon with
    every angle at ninety degrees. By default, the first two parameters set the
    location of the rectangle's upper-left corner. The third and fourth set the
    shape's the width and height, respectively. The way these parameters are
    interpreted may be changed with the rectMode()
    function.
    The version of rect() with five parameters creates a rounded rectangle. The
    fifth parameter is used as the radius value for all four corners.
    The version of rect() with eight parameters also creates a rounded rectangle.
    When using eight parameters, the latter four set the radius of the arc at
    each corner separately. The radii start with the top-left corner and move
    clockwise around the rectangle. If any of these parameters are omitted, they
    are set to the value of the last specified corner radius."""
    pass


def square(x, y, s, tl, tr, br, bl):
    """Draws a square to the canvas. A square is a four-sided polygon with every
    angle at ninety degrees and equal side lengths. By default, the first two
    parameters set the location of the square's upper-left corner. The third
    parameter sets its side size. The way these parameters are interpreted may
    be changed with the rectMode() function.
    The version of square() with four parameters creates a rounded square. The
    fourth parameter is used as the radius value for all four corners.
    The version of square() with seven parameters also creates a rounded square.
    When using seven parameters, the latter four set the radius of the arc at
    each corner separately. The radii start with the top-left corner and move
    clockwise around the square. If any of these parameters are omitted, they
    are set to the value of the last specified corner radius."""
    pass


def triangle(x1, y1, x2, y2, x3, y3):
    """Draws a triangle to the canvas. A triangle is a three-sided polygon. The
    first two parameters specify the triangle's first point (x1,y1). The middle
    two parameters specify its second point (x2,y2). And the last two parameters
    specify its third point (x3, y3)."""
    pass


def ellipseMode(mode):
    """Modifies the location from which ellipses, circles, and arcs are drawn. By default, the
    first two parameters are the x- and y-coordinates of the shape's center. The next
    parameters are its width and height. This is equivalent to calling ellipseMode(CENTER).
    ellipseMode(RADIUS) also uses the first two parameters to set the x- and y-coordinates
    of the shape's center. The next parameters are half of the shapes's width and height.
    Calling ellipse(0, 0, 10, 15) draws a shape with a width of 20 and height of 30.
    ellipseMode(CORNER) uses the first two parameters as the upper-left corner of the
    shape. The next parameters are its width and height.
    ellipseMode(CORNERS) uses the first two parameters as the location of one corner
    of the ellipse's bounding box. The third and fourth parameters are the location of the
    opposite corner.
    The argument passed to ellipseMode() must be written in ALL CAPS because the constants
    CENTER, RADIUS, CORNER, and CORNERS are defined this way. JavaScript is a
    case-sensitive language."""
    pass


def noSmooth(*args, **kwargs):
    """Draws all geometry with jagged (aliased) edges.
    smooth() is active by default in 2D mode. It's necessary to call
    noSmooth() to disable smoothing of geometry, images, and fonts.
    In WebGL mode, noSmooth() is active by default. It's necessary
    to call smooth() to draw smooth (antialiased) edges."""
    pass


def rectMode(mode):
    """Modifies the location from which rectangles and squares are drawn. By default,
    the first two parameters are the x- and y-coordinates of the shape's upper-left
    corner. The next parameters are its width and height. This is equivalent to
    calling rectMode(CORNER).
    rectMode(CORNERS) also uses the first two parameters as the location of one of
    the corners. The third and fourth parameters are the location of the opposite
    corner.
    rectMode(CENTER) uses the first two parameters as the x- and y-coordinates of
    the shape's center. The next parameters are its width and height.
    rectMode(RADIUS) also uses the first two parameters as the x- and y-coordinates
    of the shape's center. The next parameters are half of the shape's width and
    height.
    The argument passed to rectMode() must be written in ALL CAPS because the
    constants CENTER, RADIUS, CORNER, and CORNERS are defined this way.
    JavaScript is a case-sensitive language."""
    pass


def smooth(*args, **kwargs):
    """Draws all geometry with smooth (anti-aliased) edges. smooth() will also
    improve image quality of resized images.
    smooth() is active by default in 2D mode. It's necessary to call
    noSmooth() to disable smoothing of geometry, images, and fonts.
    In WebGL mode, noSmooth() is active by default. It's necessary
    to call smooth() to draw smooth (antialiased) edges."""
    pass


def strokeCap(cap):
    """Sets the style for rendering line endings. These ends are either rounded
    (ROUND), squared (SQUARE), or extended (PROJECT). The default cap is
    ROUND.
    The argument passed to strokeCap() must be written in ALL CAPS because
    the constants ROUND, SQUARE, and PROJECT are defined this way.
    JavaScript is a case-sensitive language."""
    pass


def strokeJoin(join):
    """Sets the style of the joints which connect line segments. These joints are
    either mitered (MITER), beveled (BEVEL), or rounded (ROUND). The default
    joint is MITER in 2D mode and ROUND in WebGL mode.
    The argument passed to strokeJoin() must be written in ALL CAPS because
    the constants MITER, BEVEL, and ROUND are defined this way.
    JavaScript is a case-sensitive language."""
    pass


def strokeWeight(weight):
    """Sets the width of the stroke used for lines, points, and the border around
    shapes. All widths are set in units of pixels.
    Note that strokeWeight() is affected by any transformation or scaling that
    has been applied previously."""
    pass


def bezier(*args, **kwargs):
    """Draws a cubic Bezier curve on the screen. These curves are defined by a
    series of anchor and control points. The first two parameters specify
    the first anchor point and the last two parameters specify the other
    anchor point, which become the first and last points on the curve. The
    middle parameters specify the two control points which define the shape
    of the curve. Approximately speaking, control points "pull" the curve
    towards them.
    Bezier curves were developed by French automotive engineer Pierre Bezier,
    and are commonly used in computer graphics to define gently sloping curves.
    See also curve()."""
    pass


def bezierDetail(detail):
    """Sets the resolution at which Bezier's curve is displayed. The default value is 20.
    Note, This function is only useful when using the WEBGL renderer
    as the default canvas renderer does not use this information."""
    pass


def bezierPoint(a, b, c, d, t):
    """Given the x or y co-ordinate values of control and anchor points of a bezier
    curve, it evaluates the x or y coordinate of the bezier at position t. The
    parameters a and d are the x or y coordinates of first and last points on the
    curve while b and c are of the control points.The final parameter t is the
    position of the resultant point which is given between 0 and 1.
    This can be done once with the x coordinates and a second time
    with the y coordinates to get the location of a bezier curve at t."""
    pass


def bezierTangent(a, b, c, d, t):
    """Evaluates the tangent to the Bezier at position t for points a, b, c, d.
    The parameters a and d are the first and last points
    on the curve, and b and c are the control points.
    The final parameter t varies between 0 and 1."""
    pass


def curve(*args, **kwargs):
    """Draws a curved line on the screen between two points, given as the
    middle four parameters. The first two parameters are a control point, as
    if the curve came from this point even though it's not drawn. The last
    two parameters similarly describe the other control point.
    Longer curves can be created by putting a series of curve() functions
    together or using curveVertex(). An additional function called
    curveTightness() provides control for the visual quality of the curve.
    The curve() function is an implementation of Catmull-Rom splines."""
    pass


def curveDetail(resolution):
    """Sets the resolution at which curves display. The default value is 20 while
    the minimum value is 3.
    This function is only useful when using the WEBGL renderer
    as the default canvas renderer does not use this
    information."""
    pass


def curveTightness(amount):
    """Modifies the quality of forms created with curve()
    and curveVertex().The parameter tightness
    determines how the curve fits to the vertex points. The value 0.0 is the
    default value for tightness (this value defines the curves to be Catmull-Rom
    splines) and the value 1.0 connects all the points with straight lines.
    Values within the range -5.0 and 5.0 will deform the curves but will leave
    them recognizable and as values increase in magnitude, they will continue to deform.
    """
    pass


def curvePoint(a, b, c, d, t):
    """Evaluates the curve at position t for points a, b, c, d.
    The parameter t varies between 0 and 1, a and d are control points
    of the curve, and b and c are the start and end points of the curve.
    This can be done once with the x coordinates and a second time
    with the y coordinates to get the location of a curve at t."""
    pass


def curveTangent(a, b, c, d, t):
    """Evaluates the tangent to the curve at position t for points a, b, c, d.
    The parameter t varies between 0 and 1, a and d are points on the curve,
    and b and c are the control points."""
    pass


def beginContour(*args, **kwargs):
    """Use the beginContour() and
    endContour() functions to create negative shapes
    within shapes such as the center of the letter 'O'. beginContour()
    begins recording vertices for the shape and endContour() stops recording.
    The vertices that define a negative shape must "wind" in the opposite direction
    from the exterior shape. First draw vertices for the exterior clockwise order, then for internal shapes, draw vertices
    shape in counter-clockwise.
    These functions can only be used within a beginShape()/endShape() pair and
    transformations such as translate(), rotate(), and scale() do not work
    within a beginContour()/endContour() pair. It is also not possible to use
    other shapes, such as ellipse() or rect() within."""
    pass


def beginShape(kind):
    """Using the beginShape() and endShape() functions allow creating more
    complex forms. beginShape() begins recording vertices for a shape and
    endShape() stops recording. The value of the kind parameter tells it which
    types of shapes to create from the provided vertices. With no mode
    specified, the shape can be any irregular polygon.
    The parameters available for beginShape() are:
    POINTS
    Draw a series of points
    LINES
    Draw a series of unconnected line segments (individual lines)
    TRIANGLES
    Draw a series of separate triangles
    TRIANGLE_FAN
    Draw a series of connected triangles sharing the first vertex in a fan-like fashion
    TRIANGLE_STRIP
    Draw a series of connected triangles in strip fashion
    QUADS
    Draw a series of separate quads
    QUAD_STRIP
    Draw quad strip using adjacent edges to form the next quad
    TESS (WEBGL only)
    Handle irregular polygon for filling curve by explicit tessellation
    After calling the beginShape() function, a series of vertex() commands must follow. To stop
    drawing the shape, call endShape(). Each shape will be outlined with the
    current stroke color and filled with the fill color.
    Transformations such as translate(), rotate(), and scale() do not work
    within beginShape(). It is also not possible to use other shapes, such as
    ellipse() or rect() within beginShape()."""
    pass


def bezierVertex(*args, **kwargs):
    """Specifies vertex coordinates for Bezier curves. Each call to
    bezierVertex() defines the position of two control points and
    one anchor point of a Bezier curve, adding a new segment to a
    line or shape. For WebGL mode bezierVertex() can be used in 2D
    as well as 3D mode. 2D mode expects 6 parameters, while 3D mode
    expects 9 parameters (including z coordinates).
    The first time bezierVertex() is used within a beginShape()
    call, it must be prefaced with a call to vertex() to set the first anchor
    point. This function must be used between beginShape() and endShape()
    and only when there is no MODE or POINTS parameter specified to
    beginShape()."""
    pass


def curveVertex(*args, **kwargs):
    """Specifies vertex coordinates for curves. This function may only
    be used between beginShape() and endShape() and only when there
    is no MODE parameter specified to beginShape().
    For WebGL mode curveVertex() can be used in 2D as well as 3D mode.
    2D mode expects 2 parameters, while 3D mode expects 3 parameters.
    The first and last points in a series of curveVertex() lines will be used to
    guide the beginning and end of the curve. A minimum of four
    points is required to draw a tiny curve between the second and
    third points. Adding a fifth point with curveVertex() will draw
    the curve between the second, third, and fourth points. The
    curveVertex() function is an implementation of Catmull-Rom
    splines."""
    pass


def endContour(*args, **kwargs):
    """Use the beginContour() and endContour() functions to create negative
    shapes within shapes such as the center of the letter 'O'. beginContour()
    begins recording vertices for the shape and endContour() stops recording.
    The vertices that define a negative shape must "wind" in the opposite
    direction from the exterior shape. First draw vertices for the exterior
    clockwise order, then for internal shapes, draw vertices
    shape in counter-clockwise.
    These functions can only be used within a beginShape()/endShape() pair and
    transformations such as translate(), rotate(), and scale() do not work
    within a beginContour()/endContour() pair. It is also not possible to use
    other shapes, such as ellipse() or rect() within."""
    pass


def endShape(mode, count):
    """The endShape() function is the companion to beginShape() and may only be
    called after beginShape(). When endShape() is called, all of the image
    data defined since the previous call to beginShape() is written into the image
    buffer. The constant CLOSE is the value for the mode parameter to close
    the shape (to connect the beginning and the end).
    When using instancing with endShape() the instancing will not apply to the strokes.
    When the count parameter is used with a value greater than 1, it enables instancing for shapes built when in WEBGL mode. Instancing
    is a feature that allows the GPU to efficiently draw multiples of the same shape. It's often used for particle effects or other
    times when you need a lot of repetition. In order to take advantage of instancing, you will also need to write your own custom
    shader using the gl_InstanceID keyword. You can read more about instancing
    here or by working from the example on this
    page."""
    pass


def quadraticVertex(*args, **kwargs):
    """Specifies vertex coordinates for quadratic Bezier curves. Each call to
    quadraticVertex() defines the position of one control points and one
    anchor point of a Bezier curve, adding a new segment to a line or shape.
    The first time quadraticVertex() is used within a beginShape() call, it
    must be prefaced with a call to vertex() to set the first anchor point.
    For WebGL mode quadraticVertex() can be used in 2D as well as 3D mode.
    2D mode expects 4 parameters, while 3D mode expects 6 parameters
    (including z coordinates).
    This function must be used between beginShape() and endShape()
    and only when there is no MODE or POINTS parameter specified to
    beginShape()."""
    pass


def vertex(*args, **kwargs):
    """All shapes are constructed by connecting a series of vertices. vertex()
    is used to specify the vertex coordinates for points, lines, triangles,
    quads, and polygons. It is used exclusively within the beginShape() and
    endShape() functions."""
    pass


def normal(*args, **kwargs):
    """Sets the 3d vertex normal to use for subsequent vertices drawn with
    vertex(). A normal is a vector that is generally
    nearly perpendicular to a shape's surface which controls how much light will
    be reflected from that part of the surface."""
    pass


def print(contents):
    """Displays text in the web browser's console.
    print() is helpful for printing values while debugging. Each call to
    print() creates a new line of text.
    Note: Call print('\n') to print a blank line. Calling print() without
    an argument opens the browser's dialog for printing documents."""
    pass


def cursor(type, x, y):
    """Changes the cursor's appearance.
    The first parameter, type, sets the type of cursor to display. The
    built-in options are ARROW, CROSS, HAND, MOVE, TEXT, and WAIT.
    cursor() also recognizes standard CSS cursor properties passed as
    strings: 'help', 'wait', 'crosshair', 'not-allowed', 'zoom-in',
    and 'grab'. If the path to an image is passed, as in
    cursor('assets/target.png'), then the image will be used as the cursor.
    Images must be in .cur, .gif, .jpg, .jpeg, or .png format.
    The parameters x and y are optional. If an image is used for the
    cursor, x and y set the location pointed to within the image. They are
    both 0 by default, so the cursor points to the image's top-left corner. x
    and y must be less than the image's width and height, respectively."""
    pass


def frameRate(*args, **kwargs):
    """Sets the number of frames to draw per second.
    Calling frameRate() with one numeric argument, as in frameRate(30),
    attempts to draw 30 frames per second (FPS). The target frame rate may not
    be achieved depending on the sketch's processing needs. Most computers
    default to a frame rate of 60 FPS. Frame rates of 24 FPS and above are
    fast enough for smooth animations.
    Calling frameRate() without an argument returns the current frame rate.
    The value returned is an approximation."""
    pass


def getTargetFrameRate(*args, **kwargs):
    """Returns the target frame rate. The value is either the system frame rate or
    the last value passed to frameRate()."""
    pass


def noCursor(*args, **kwargs):
    """Hides the cursor from view."""
    pass


def windowResized(event):
    """The code in windowResized() is called once each time the browser window
    is resized. It's a good place to resize the canvas or make other
    adjustments to accommodate the new window size.
    The event parameter is optional. If added to the function definition, it
    can be used for debugging or other purposes."""
    pass


def fullscreen(val):
    """Toggles full-screen mode or returns the current mode.
    Calling fullscreen(true) makes the sketch full-screen. Calling
    fullscreen(false) makes the sketch its original size.
    Calling fullscreen() without an argument returns true if the sketch
    is in full-screen mode and false if not.
    Note: Due to browser restrictions, fullscreen() can only be called with
    user input such as a mouse press."""
    pass


def pixelDensity(*args, **kwargs):
    """Sets the pixel scaling for high pixel density displays.
    By default, the pixel density is set to match display density. Calling
    pixelDensity(1) turn this off.
    Calling pixelDensity() without an argument returns the current pixel
    density."""
    pass


def displayDensity(*args, **kwargs):
    """Returns the display's current pixel density."""
    pass


def getURL(*args, **kwargs):
    """Returns the sketch's current
    URL
    as a string."""
    pass


def getURLPath(*args, **kwargs):
    """Returns the current
    URL
    path as an array of strings.
    For example, consider a sketch hosted at the URL
    https://example.com/sketchbook. Calling getURLPath() returns
    ['sketchbook']. For a sketch hosted at the URL
    https://example.com/sketchbook/monday, getURLPath() returns
    ['sketchbook', 'monday']."""
    pass


def getURLParams(*args, **kwargs):
    """Returns the current
    URL parameters
    in an Object.
    For example, calling getURLParams() in a sketch hosted at the URL
    http://p5js.org?year=2014&month=May&day=15 returns
    { year: 2014, month: 'May', day: 15 }."""
    pass


def preload(*args, **kwargs):
    """Called directly before setup(), the preload() function is used to handle
    asynchronous loading of external files in a blocking way. If a preload
    function is defined, setup() will wait until any load calls within have
    finished. Nothing besides load calls (loadImage, loadJSON, loadFont,
    loadStrings, etc.) should be inside the preload function. If asynchronous
    loading is preferred, the load methods can instead be called in setup()
    or anywhere else with the use of a callback parameter.
    By default the text "loading..." will be displayed. To make your own
    loading page, include an HTML element with id "p5_loading" in your
    page. More information here."""
    pass


def setup(*args, **kwargs):
    """The setup() function is called once when the program starts. It's used to
    define initial environment properties such as screen size and background
    color and to load media such as images and fonts as the program starts.
    There can only be one setup() function for each program and it shouldn't
    be called again after its initial execution.
    Note: Variables declared within setup() are not accessible within other
    functions, including draw()."""
    pass


def draw(*args, **kwargs):
    """Called directly after setup(), the draw() function continuously executes
    the lines of code contained inside its block until the program is stopped
    or noLoop() is called. Note if noLoop() is called in setup(), draw() will
    still be executed once before stopping. draw() is called automatically and
    should never be called explicitly.
    It should always be controlled with noLoop(), redraw() and loop(). After
    noLoop() stops the code in draw() from executing, redraw() causes the
    code inside draw() to execute once, and loop() will cause the code
    inside draw() to resume executing continuously.
    The number of times draw() executes in each second may be controlled with
    the frameRate() function.
    There can only be one draw() function for each sketch, and draw() must
    exist if you want the code to run continuously, or to process events such
    as mousePressed(). Sometimes, you might have an empty call to draw() in
    your program, as shown in the above example.
    It is important to note that the drawing coordinate system will be reset
    at the beginning of each draw() call. If any transformations are performed
    within draw() (ex: scale, rotate, translate), their effects will be
    undone at the beginning of draw(), so transformations will not accumulate
    over time. On the other hand, styling applied (ex: fill, stroke, etc) will
    remain in effect."""
    pass


def remove(*args, **kwargs):
    """Removes the entire p5 sketch. This will remove the canvas and any
    elements created by p5.js. It will also stop the draw loop and unbind
    any properties or methods from the window global scope. It will
    leave a variable p5 in case you wanted to create a new p5 sketch.
    If you like, you can set p5 = null to erase it. While all functions and
    variables and objects created by the p5 library will be removed, any
    other global variables created by your code will remain."""
    pass


def createCanvas(*args, **kwargs):
    """Creates a canvas element in the document and sets its dimensions
    in pixels. This method should be called only once at the start of setup().
    Calling createCanvas more than once in a
    sketch will result in very unpredictable behavior. If you want more than
    one drawing canvas you could use createGraphics()
    (hidden by default but it can be shown).
    Important note: in 2D mode (i.e. when p5.Renderer is not set) the origin (0,0)
    is positioned at the top left of the screen. In 3D mode (i.e. when p5.Renderer
    is set to WEBGL), the origin is positioned at the center of the canvas.
    See this issue for more information.
    A WebGL canvas will use a WebGL2 context if it is supported by the browser.
    Check the webglVersion property to check what
    version is being used, or call setAttributes({ version: 1 })
    to create a WebGL1 context.
    The system variables width and height are set by the parameters passed to this
    function. If createCanvas() is not used, the
    window will be given a default size of 100×100 pixels.
    Optionally, an existing canvas can be passed using a selector, ie. document.getElementById('').
    If specified, avoid using setAttributes() afterwards, as this will remove and recreate the existing canvas.
    For more ways to position the canvas, see the

    positioning the canvas wiki page."""
    pass


def resizeCanvas(w, h, noRedraw):
    """Resizes the canvas to given width and height. The canvas will be cleared
    and draw will be called immediately, allowing the sketch to re-render itself
    in the resized canvas."""
    pass


def noCanvas(*args, **kwargs):
    """Removes the default canvas for a p5 sketch that doesn't require a canvas"""
    pass


def createGraphics(*args, **kwargs):
    """Creates and returns a new p5.Graphics object. Use this class if you need
    to draw into an off-screen graphics buffer. The two parameters define the
    width and height in pixels.
    A WebGL p5.Graphics will use a WebGL2 context if it is supported by the browser.
    Check the pg.webglVersion property of the renderer
    to check what version is being used, or call pg.setAttributes({ version: 1 })
    to create a WebGL1 context.
    Optionally, an existing canvas can be passed using a selector, ie. document.getElementById('').
    By default this canvas will be hidden (offscreen buffer), to make visible, set element's style to display:block;
    """
    pass


def createFramebuffer(options):
    """Creates and returns a new p5.Framebuffer, a
    high-performance WebGL object that you can draw to and then use as a texture.
    Options can include:

    format: The data format of the texture, either UNSIGNED_BYTE, FLOAT, or HALF_FLOAT. The default is UNSIGNED_BYTE.
    channels: What color channels to store, either RGB or RGBA. The default is to match the channels in the main canvas (with alpha unless disabled with setAttributes.)
    depth: A boolean, whether or not to include a depth buffer. Defaults to true.
    depthFormat: The data format for depth information, either UNSIGNED_INT or FLOAT. The default is FLOAT if available, or UNSIGNED_INT otherwise.
    stencil: A boolean, whether or not to include a stencil buffer, which can be used for masking. This may only be used if also using a depth buffer. Defaults to the value of depth, which is true if not provided.
    antialias: Boolean or Number, whether or not to render with antialiased edges, and if so, optionally the number of samples to use. Defaults to whether or not the main canvas is antialiased, using a default of 2 samples if so. Antialiasing is only supported when WebGL 2 is available.
    width: The width of the texture. Defaults to matching the main canvas.
    height: The height of the texture. Defaults to matching the main canvas.
    density: The pixel density of the texture. Defaults to the pixel density of the main canvas.
    textureFiltering: Either LINEAR (nearby pixels will be interpolated when reading values from the color texture) or NEAREST (no interpolation.) Generally, use LINEAR when using the texture as an image, and use NEAREST if reading the texture as data. Defaults to LINEAR.

    If width, height, or density are specified, then the framebuffer will
    keep that size until manually changed. Otherwise, it will be autosized, and
    it will update to match the main canvas's size and density when the main
    canvas changes."""
    pass


def blendMode(mode):
    """Blends the pixels in the display window according to the defined mode.
    There is a choice of the following modes to blend the source pixels (A)
    with the ones of pixels already in the display window (B):

    BLEND - linear interpolation of colours: C =
    A*factor + B. This is the default blending mode.
    ADD - sum of A and B
    DARKEST - only the darkest colour succeeds: C =
    min(A*factor, B).
    LIGHTEST - only the lightest colour succeeds: C =
    max(A*factor, B).
    DIFFERENCE - subtract colors from underlying image.
    (2D)
    EXCLUSION - similar to DIFFERENCE, but less
    extreme.
    MULTIPLY - multiply the colors, result will always be
    darker.
    SCREEN - opposite multiply, uses inverse values of the
    colors.
    REPLACE - the pixels entirely replace the others and
    don't utilize alpha (transparency) values.
    REMOVE - removes pixels from B with the alpha strength of A.
    OVERLAY - mix of MULTIPLY and SCREEN
    . Multiplies dark values, and screens light values. (2D)
    HARD_LIGHT - SCREEN when greater than 50%
    gray, MULTIPLY when lower. (2D)
    SOFT_LIGHT - mix of DARKEST and
    LIGHTEST. Works like OVERLAY, but not as harsh. (2D)

    DODGE - lightens light tones and increases contrast,
    ignores darks. (2D)
    BURN - darker areas are applied, increasing contrast,
    ignores lights. (2D)
    SUBTRACT - remainder of A and B (3D)

    (2D) indicates that this blend mode only works in the 2D renderer.
    (3D) indicates that this blend mode only works in the WEBGL renderer."""
    pass


def noLoop(*args, **kwargs):
    """Stops p5.js from continuously executing the code within draw().
    If loop() is called, the code in draw()
    begins to run continuously again. If using noLoop()
    in setup(), it should be the last line inside the block.
    When noLoop() is used, it's not possible to manipulate
    or access the screen inside event handling functions such as
    mousePressed() or
    keyPressed(). Instead, use those functions to
    call redraw() or loop(),
    which will run draw(), which can update the screen
    properly. This means that when noLoop() has been
    called, no drawing can happen, and functions like saveFrames()
    or loadPixels() may not be used.
    Note that if the sketch is resized, redraw() will
    be called to update the sketch, even after noLoop()
    has been specified. Otherwise, the sketch would enter an odd state until
    loop() was called.
    Use isLooping() to check the current state of loop()."""
    pass


def loop(*args, **kwargs):
    """By default, p5.js loops through draw() continuously, executing the code within
    it. However, the draw() loop may be stopped by calling
    noLoop(). In that case, the draw()
    loop can be resumed with loop().
    Avoid calling loop() from inside setup().
    Use isLooping() to check the current state of loop()."""
    pass


def isLooping(*args, **kwargs):
    """By default, p5.js loops through draw() continuously,
    executing the code within it. If the sketch is stopped with
    noLoop() or resumed with loop(),
    isLooping() returns the current state for use within custom event handlers."""
    pass


def push(*args, **kwargs):
    """The push() function saves the current drawing style
    settings and transformations, while pop() restores these
    settings. Note that these functions are always used together. They allow you to
    change the style and transformation settings and later return to what you had.
    When a new state is started with push(), it builds on
    the current style and transform information. The push()
    and pop() functions can be embedded to provide more
    control. (See the second example for a demonstration.)
    push() stores information related to the current transformation state
    and style settings controlled by the following functions:
    fill(),
    noFill(),
    noStroke(),
    stroke(),
    tint(),
    noTint(),
    strokeWeight(),
    strokeCap(),
    strokeJoin(),
    imageMode(),
    rectMode(),
    ellipseMode(),
    colorMode(),
    textAlign(),
    textFont(),
    textSize(),
    textLeading(),
    applyMatrix(),
    resetMatrix(),
    rotate(),
    scale(),
    shearX(),
    shearY(),
    translate(),
    noiseSeed().
    In WEBGL mode additional style settings are stored. These are controlled by the
    following functions: setCamera(),
    ambientLight(),
    directionalLight(),
    pointLight(), texture(),
    specularMaterial(),
    shininess(),
    normalMaterial()
    and shader()."""
    pass


def pop(*args, **kwargs):
    """The push() function saves the current drawing style
    settings and transformations, while pop() restores
    these settings. Note that these functions are always used together. They allow
    you to change the style and transformation settings and later return to what
    you had. When a new state is started with push(), it
    builds on the current style and transform information. The push()
    and pop() functions can be embedded to provide more
    control. (See the second example for a demonstration.)
    push() stores information related to the current transformation state
    and style settings controlled by the following functions:
    fill(),
    noFill(),
    noStroke(),
    stroke(),
    tint(),
    noTint(),
    strokeWeight(),
    strokeCap(),
    strokeJoin(),
    imageMode(),
    rectMode(),
    ellipseMode(),
    colorMode(),
    textAlign(),
    textFont(),
    textSize(),
    textLeading(),
    applyMatrix(),
    resetMatrix(),
    rotate(),
    scale(),
    shearX(),
    shearY(),
    translate(),
    noiseSeed().
    In WEBGL mode additional style settings are stored. These are controlled by
    the following functions:
    setCamera(),
    ambientLight(),
    directionalLight(),
    pointLight(),
    texture(),
    specularMaterial(),
    shininess(),
    normalMaterial() and
    shader()."""
    pass


def redraw(n):
    """Executes the code within draw() one time. This
    function allows the program to update the display window only when necessary,
    for example when an event registered by mousePressed()
    or keyPressed() occurs.
    In structuring a program, it only makes sense to call redraw()
    within events such as mousePressed(). This
    is because redraw() does not run
    draw() immediately (it only sets a flag that indicates
    an update is needed).
    The redraw() function does not work properly when
    called inside draw().To enable/disable animations,
    use loop() and noLoop().
    In addition you can set the number of redraws per method call. Just
    add an integer as single parameter for the number of redraws."""
    pass


def p5(sketch, node):
    """The p5() constructor enables you to activate "instance mode" instead of normal
    "global mode". This is an advanced topic. A short description and example is
    included below. Please see

    Dan Shiffman's Coding Train video tutorial or this
    tutorial page
    for more info.
    By default, all p5.js functions are in the global namespace (i.e. bound to the window
    object), meaning you can call them simply ellipse(), fill(), etc. However, this
    might be inconvenient if you are mixing with other JS libraries (synchronously or
    asynchronously) or writing long programs of your own. p5.js currently supports a
    way around this problem called "instance mode". In instance mode, all p5 functions
    are bound up in a single variable instead of polluting your global namespace.
    Optionally, you can specify a default container for the canvas and any other elements
    to append to with a second argument. You can give the ID of an element in your html,
    or an html node itself.
    Note that creating instances like this also allows you to have more than one p5 sketch on
    a single web page, as they will each be wrapped up with their own set up variables. Of
    course, you could also use iframes to have multiple sketches in global mode."""
    pass


def applyMatrix(*args, **kwargs):
    """Multiplies the current matrix by the one specified through the parameters.
    This is a powerful operation that can perform the equivalent of translate,
    scale, shear and rotate all at once. You can learn more about transformation
    matrices on
    Wikipedia.
    The naming of the arguments here follows the naming of the
    WHATWG specification and corresponds to a
    transformation matrix of the
    form:



    """
    pass


def resetMatrix(*args, **kwargs):
    """Replaces the current matrix with the identity matrix."""
    pass


def rotate(angle, axis):
    """Rotates a shape by the amount specified by the angle parameter. This
    function accounts for angleMode, so angles
    can be entered in either RADIANS or DEGREES.
    Objects are always rotated around their relative position to the
    origin and positive numbers rotate objects in a clockwise direction.
    Transformations apply to everything that happens after and subsequent
    calls to the function accumulate the effect. For example, calling
    rotate(HALF_PI) and then rotate(HALF_PI) is the same as rotate(PI).
    All transformations are reset when draw() begins again.
    Technically, rotate() multiplies the current transformation matrix
    by a rotation matrix. This function can be further controlled by
    push() and pop()."""
    pass


def rotateX(angle):
    """Rotates a shape around X axis by the amount specified in angle parameter.
    The angles can be entered in either RADIANS or DEGREES.
    Objects are always rotated around their relative position to the
    origin and positive numbers rotate objects in a clockwise direction.
    All transformations are reset when draw() begins again."""
    pass


def rotateY(angle):
    """Rotates a shape around Y axis by the amount specified in angle parameter.
    The angles can be entered in either RADIANS or DEGREES.
    Objects are always rotated around their relative position to the
    origin and positive numbers rotate objects in a clockwise direction.
    All transformations are reset when draw() begins again."""
    pass


def rotateZ(angle):
    """Rotates a shape around Z axis by the amount specified in angle parameter.
    The angles can be entered in either RADIANS or DEGREES.
    This method works in WEBGL mode only.
    Objects are always rotated around their relative position to the
    origin and positive numbers rotate objects in a clockwise direction.
    All transformations are reset when draw() begins again."""
    pass


def scale(*args, **kwargs):
    """Increases or decreases the size of a shape by expanding or contracting
    vertices. Objects always scale from their relative origin to the
    coordinate system. Scale values are specified as decimal percentages.
    For example, the function call scale(2.0) increases the dimension of a
    shape by 200%.
    Transformations apply to everything that happens after and subsequent
    calls to the function multiply the effect. For example, calling scale(2.0)
    and then scale(1.5) is the same as scale(3.0). If scale() is called
    within draw(), the transformation is reset when the loop begins again.
    Using this function with the z parameter is only available in WEBGL mode.
    This function can be further controlled with push() and pop()."""
    pass


def shearX(angle):
    """Shears a shape around the x-axis by the amount specified by the angle
    parameter. Angles should be specified in the current angleMode.
    Objects are always sheared around their relative position to the origin
    and positive numbers shear objects in a clockwise direction.
    Transformations apply to everything that happens after and subsequent
    calls to the function accumulates the effect. For example, calling
    shearX(PI/2) and then shearX(PI/2) is the same as shearX(PI).
    If shearX() is called within the draw(),
    the transformation is reset when the loop begins again.
    Technically, shearX() multiplies the current
    transformation matrix by a rotation matrix. This function can be further
    controlled by the push() and pop() functions."""
    pass


def shearY(angle):
    """Shears a shape around the y-axis the amount specified by the angle
    parameter. Angles should be specified in the current angleMode. Objects
    are always sheared around their relative position to the origin and
    positive numbers shear objects in a clockwise direction.
    Transformations apply to everything that happens after and subsequent
    calls to the function accumulates the effect. For example, calling
    shearY(PI/2) and then shearY(PI/2) is the same as shearY(PI). If
    shearY() is called within the draw(), the transformation is reset when
    the loop begins again.
    Technically, shearY() multiplies the current transformation matrix by a
    rotation matrix. This function can be further controlled by the
    push() and pop() functions."""
    pass


def translate(*args, **kwargs):
    """Specifies an amount to displace objects within the display window.
    The x parameter specifies left/right translation, the y parameter
    specifies up/down translation.
    Transformations are cumulative and apply to everything that happens after
    and subsequent calls to the function accumulates the effect. For example,
    calling translate(50, 0) and then translate(20, 0) is the same as
    translate(70, 0). If translate() is called within draw(), the
    transformation is reset when the loop begins again. This function can be
    further controlled by using push() and pop()."""
    pass


def storeItem(key, value):
    """Stores a value in local storage under the key name.
     Local storage is saved in the browser and persists
     between browsing sessions and page reloads.
     The key can be the name of the variable but doesn't
     have to be. To retrieve stored items
     see getItem.
    Sensitive data such as passwords or personal information
     should not be stored in local storage."""
    pass


def getItem(key):
    """Returns the value of an item that was stored in local storage
    using storeItem()"""
    pass


def clearStorage(*args, **kwargs):
    """Clears all local storage items set with storeItem()
    for the current domain."""
    pass


def removeItem(key):
    """Removes an item that was stored with storeItem()"""
    pass


def createStringDict(*args, **kwargs):
    """Creates a new instance of p5.StringDict using the key-value pair
    or the object you provide."""
    pass


def createNumberDict(*args, **kwargs):
    """Creates a new instance of p5.NumberDict using the key-value pair
    or object you provide."""
    pass


def select(selectors, container):
    """Searches the page for the first element that matches the given
    CSS selector string.
    The string can be an ID, class, tag name, or a combination. select()
    returns a p5.Element object if it finds a match
    and null otherwise.
    The second parameter, container, is optional. It specifies a container to
    search within. container can be CSS selector string, a
    p5.Element object, or an
    HTMLElement object."""
    pass


def selectAll(selectors, container):
    """Searches the page for all elements that matches the given
    CSS selector string.
    The string can be an ID, class, tag name, or a combination. selectAll()
    returns an array of p5.Element objects if it
    finds any matches and an empty array otherwise.
    The second parameter, container, is optional. It specifies a container to
    search within. container can be CSS selector string, a
    p5.Element object, or an
    HTMLElement object."""
    pass


def removeElements(*args, **kwargs):
    """Removes all elements created by p5.js, including any event handlers.
    There are two exceptions:
    canvas elements created by createCanvas
    and p5.Render objects created by
    createGraphics."""
    pass


def changed(fxn):
    """myElement.changed() sets a function to call when the value of the
    p5.Element object changes. Calling
    myElement.changed(false) disables the function."""
    pass


def input(fxn):
    """myElement.input() sets a function to call when input is detected within
    the p5.Element object. It's often used to with
    text inputs and sliders. Calling myElement.input(false) disables the
    function."""
    pass


def createDiv(html):
    """Creates a <div></div> element. It's commonly used as a
    container for other elements.
    The parameter html is optional. It accepts a string that sets the
    inner HTML of the new <div></div>."""
    pass


def createP(html):
    """Creates a <p></p> element. It's commonly used for
    paragraph-length text.
    The parameter html is optional. It accepts a string that sets the
    inner HTML of the new <p></p>."""
    pass


def createSpan(html):
    """Creates a <span></span> element. It's commonly used as a
    container for inline elements. For example, a <span></span>
    can hold part of a sentence that's a
    different style.
    The parameter html is optional. It accepts a string that sets the
    inner HTML of the new <span></span>."""
    pass


def createImg(*args, **kwargs):
    """Creates an <img> element that can appear outside of the canvas.
    The first parameter, src, is a string with the path to the image file.
    src should be a relative path, as in 'assets/image.png', or a URL, as
    in 'https://example.com/image.png'.
    The second parameter, alt, is a string with the
    alternate text
    for the image. An empty string '' can be used for images that aren't displayed.
    The third parameter, crossOrigin, is optional. It's a string that sets the
    crossOrigin property
    of the image. Use 'anonymous' or 'use-credentials' to fetch the image
    with cross-origin access.
    The fourth parameter, callback, is also optional. It sets a function to
    call after the image loads. The new image is passed to the callback
    function as a p5.Element object."""
    pass


def createA(href, html, target):
    """Creates an <a></a> element that links to another web page.
    The first parmeter, href, is a string that sets the URL of the linked
    page.
    The second parameter, html, is a string that sets the inner HTML of the
    link. It's common to use text, images, or buttons as links.
    The third parameter, target, is optional. It's a string that tells the
    web browser where to open the link. By default, links open in the current
    browser tab. Passing '_blank' will cause the link to open in a new
    browser tab. MDN describes a few
    other options."""
    pass


def createSlider(min, max, value, step):
    """Creates a slider <input></input> element. Range sliders are
    useful for quickly selecting numbers from a given range.
    The first two parameters, min and max, are numbers that set the
    slider's minimum and maximum.
    The third parameter, value, is optional. It's a number that sets the
    slider's default value.
    The fourth parameter, step, is also optional. It's a number that sets the
    spacing between each value in the slider's range. Setting step to 0
    allows the slider to move smoothly from min to max."""
    pass


def createButton(label, value):
    """Creates a <button></button> element.
    The first parameter, label, is a string that sets the label displayed on
    the button.
    The second parameter, value, is optional. It's a string that sets the
    button's value. See
    MDN
    for more details."""
    pass


def createCheckbox(label, value):
    """Creates a checkbox <input></input> element. Checkboxes extend
    the p5.Element class with a checked() method.
    Calling myBox.checked() returns true if it the box is checked and
    false otherwise.
    The first parameter, label, is optional. It's a string that sets the label
    to display next to the checkbox.
    The second parameter, value, is also optional. It's a boolean that sets the
    checkbox's value."""
    pass


def createSelect(*args, **kwargs):
    """Creates a dropdown menu <select></select> element.
    The parameter is optional. If true is passed, as in
    let mySelect = createSelect(true), then the dropdown will support
    multiple selections. If an existing <select></select> element
    is passed, as in let mySelect = createSelect(otherSelect), the existing
    element will be wrapped in a new p5.Element
    object.
    Dropdowns extend the p5.Element class with a few
    helpful methods for managing options:

    mySelect.option(name, [value]) adds an option to the menu. The first paremeter, name, is a string that sets the option's name and value. The second parameter, value, is optional. If provided, it sets the value that corresponds to the key name. If an option with name already exists, its value is changed to value.
    mySelect.value() returns the currently-selected option's value.
    mySelect.selected() returns the currently-selected option.
    mySelect.selected(option) selects the given option by default.
    mySelect.disable() marks the whole dropdown element as disabled.
    mySelect.disable(option) marks a given option as disabled.
    mySelect.enable() marks the whole dropdown element as enabled.
    mySelect.enable(option) marks a given option as enabled.
    """
    pass


def createRadio(*args, **kwargs):
    """Creates a radio button element.
    The parameter is optional. If a string is passed, as in
    let myRadio = createSelect('food'), then each radio option will
    have "food" as its name parameter: <input name="food"></input>.
    If an existing <div></div> or <span></span>
    element is passed, as in let myRadio = createSelect(container), it will
    become the radio button's parent element.
    Radio buttons extend the p5.Element class with a few
    helpful methods for managing options:

    myRadio.option(value, [label]) adds an option to the menu. The first paremeter, value, is a string that sets the option's value and label. The second parameter, label, is optional. If provided, it sets the label displayed for the value. If an option with value already exists, its label is changed and its value is returned.
    myRadio.value() returns the currently-selected option's value.
    myRadio.selected() returns the currently-selected option.
    myRadio.selected(value) selects the given option and returns it as an HTMLInputElement.
    myRadio.disable(shouldDisable) enables the entire radio button if true is passed and disables it if false is passed.
    """
    pass


def createColorPicker(value):
    """Creates a color picker element.
    The parameter, value, is optional. If a color string or
    p5.Color object is passed, it will set the default
    color.
    Color pickers extend the p5.Element class with a
    couple of helpful methods for managing colors:

    myPicker.value() returns the current color as a hex string in the format '#rrggbb'.
    myPicker.color() returns the current color as a p5.Color object.
    """
    pass


def createInput(*args, **kwargs):
    """Creates a text <input></input> element. Call myInput.size()
    to set the length of the text box.
    The first parameter, value, is optional. It's a string that sets the
    input's default value. The input is blank by default.
    The second parameter, type, is also optional. It's a string that
    specifies the type of text being input. See MDN for a full
    list of options.
    The default is 'text'."""
    pass


def createFileInput(callback, multiple):
    """Creates an <input></input> element of type 'file'.
    This allows users to select local files for use in a sketch.
    The first parameter, callback, is a function that's called when the file
    loads. The callback function should have one parameter, file, that's a
    p5.File object.
    The second parameter, multiple, is optional. It's a boolean value that
    allows loading multiple files if set to true. If true, callback
    will be called once per file."""
    pass


def createVideo(src, callback):
    """Creates a <video> element for simple audio/video playback.
    Returns a new p5.MediaElement object.
    Videos are shown by default. They can be hidden by calling video.hide()
    and drawn to the canvas using image().
    The first parameter, src, is the path the video. If a single string is
    passed, as in 'assets/topsecret.mp4', a single video is loaded. An array
    of strings can be used to load the same video in different formats. For
    example, ['assets/topsecret.mp4', 'assets/topsecret.ogv', 'assets/topsecret.webm'].
    This is useful for ensuring that the video can play across different browsers with
    different capabilities. See
    MDN
    for more information about supported formats.
    The second parameter, callback, is optional. It's a function to call once
    the video is ready to play."""
    pass


def createAudio(src, callback):
    """Creates a hidden <audio> element for simple audio playback.
    Returns a new p5.MediaElement object.
    The first parameter, src, is the path the video. If a single string is
    passed, as in 'assets/video.mp4', a single video is loaded. An array
    of strings can be used to load the same video in different formats. For
    example, ['assets/video.mp4', 'assets/video.ogv', 'assets/video.webm'].
    This is useful for ensuring that the video can play across different
    browsers with different capabilities. See
    MDN
    for more information about supported formats.
    The second parameter, callback, is optional. It's a function to call once
    the audio is ready to play."""
    pass


def createCapture(type, callback):
    """Creates a <video> element that "captures" the audio/video stream from
    the webcam and microphone. Returns a new
    p5.Element object.
    Videos are shown by default. They can be hidden by calling capture.hide()
    and drawn to the canvas using image().
    The first parameter, type, is optional. It sets the type of capture to
    use. By default, createCapture() captures both audio and video. If VIDEO
    is passed, as in createCapture(VIDEO), only video will be captured.
    If AUDIO is passed, as in createCapture(AUDIO), only audio will be
    captured. A constraints object can also be passed to customize the stream.
    See the
    W3C documentation for possible properties. Different browsers support different
    properties.
    The second parameter, callback, is optional. It's a function to call once
    the capture is ready for use. The callback function should have one
    parameter, stream, that's a
    MediaStream object.
    Note: createCapture() only works when running a sketch locally or using HTTPS. Learn more
    here
    and here."""
    pass


def createElement(tag, content):
    """Creates a new p5.Element object.
    The first parameter, tag, is a string an HTML tag such as 'h5'.
    The second parameter, content, is optional. It's a string that sets the
    HTML content to insert into the new element. New elements have no content
    by default."""
    pass


def setMoveThreshold(value):
    """The setMoveThreshold() function is used to set the movement threshold for
    the deviceMoved() function. The default threshold is set to 0.5."""
    pass


def setShakeThreshold(value):
    """The setShakeThreshold() function is used to set the movement threshold for
    the deviceShaken() function. The default threshold is set to 30."""
    pass


def deviceMoved(*args, **kwargs):
    """The deviceMoved() function is called when the device is moved by more than
    the threshold value along X, Y or Z axis. The default threshold is set to 0.5.
    The threshold value can be changed using setMoveThreshold()."""
    pass


def deviceTurned(*args, **kwargs):
    """The deviceTurned() function is called when the device rotates by
    more than 90 degrees continuously.
    The axis that triggers the deviceTurned() method is stored in the turnAxis
    variable. The deviceTurned() method can be locked to trigger on any axis:
    X, Y or Z by comparing the turnAxis variable to 'X', 'Y' or 'Z'."""
    pass


def deviceShaken(*args, **kwargs):
    """The deviceShaken() function is called when the device total acceleration
    changes of accelerationX and accelerationY values is more than
    the threshold value. The default threshold is set to 30.
    The threshold value can be changed using setShakeThreshold()."""
    pass


def keyPressed(event):
    """The keyPressed() function is called once every time a key is pressed. The
    keyCode for the key that was pressed is stored in the keyCode variable.
    For non-ASCII keys, use the keyCode variable. You can check if the keyCode
    equals BACKSPACE, DELETE, ENTER, RETURN, TAB, ESCAPE, SHIFT, CONTROL,
    OPTION, ALT, UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW.
    For ASCII keys, the key that was pressed is stored in the key variable. However, it
    does not distinguish between uppercase and lowercase. For this reason, it
    is recommended to use keyTyped() to read the key variable, in which the
    case of the variable will be distinguished.
    Because of how operating systems handle key repeats, holding down a key
    may cause multiple calls to keyTyped() (and keyReleased() as well). The
    rate of repeat is set by the operating system and how each computer is
    configured.
    Browsers may have different default
    behaviors attached to various key events. To prevent any default
    behavior for this event, add "return false" to the end of the method."""
    pass


def keyReleased(event):
    """The keyReleased() function is called once every time a key is released.
    See key and keyCode for more information.
    Browsers may have different default
    behaviors attached to various key events. To prevent any default
    behavior for this event, add "return false" to the end of the function."""
    pass


def keyTyped(event):
    """The keyTyped() function is called once every time a key is pressed, but
    action keys such as Backspace, Delete, Ctrl, Shift, and Alt are ignored. If you are trying to detect
    a keyCode for one of these keys, use the keyPressed() function instead.
    The most recent key typed will be stored in the key variable.
    Because of how operating systems handle key repeats, holding down a key
    will cause multiple calls to keyTyped() (and keyReleased() as well). The
    rate of repeat is set by the operating system and how each computer is
    configured.
    Browsers may have different default behaviors attached to various key
    events. To prevent any default behavior for this event, add "return false"
    to the end of the function."""
    pass


def keyIsDown(code):
    """The keyIsDown() function checks if the key is currently down, i.e. pressed.
    It can be used if you have an object that moves, and you want several keys
    to be able to affect its behaviour simultaneously, such as moving a
    sprite diagonally. You can put in any number representing the keyCode of
    the key, or use any of the variable keyCode names listed
    here."""
    pass


def mouseMoved(event):
    """The mouseMoved() function is called every time the mouse moves and a mouse
    button is not pressed.
    Browsers may have different default
    behaviors attached to various mouse events. To prevent any default
    behavior for this event, add "return false" to the end of the method."""
    pass


def mouseDragged(event):
    """The mouseDragged() function is called once every time the mouse moves and
    a mouse button is pressed. If no mouseDragged() function is defined, the
    touchMoved() function will be called instead if it is defined.
    Browsers may have different default
    behaviors attached to various mouse events. To prevent any default
    behavior for this event, add "return false" to the end of the function."""
    pass


def mousePressed(event):
    """The mousePressed() function is called once after every time a mouse button
    is pressed. The mouseButton variable (see the related reference entry)
    can be used to determine which button has been pressed. If no
    mousePressed() function is defined, the touchStarted() function will be
    called instead if it is defined.
    Browsers may have different default
    behaviors attached to various mouse events. To prevent any default
    behavior for this event, add "return false" to the end of the function."""
    pass


def mouseReleased(event):
    """The mouseReleased() function is called every time a mouse button is
    released. If no mouseReleased() function is defined, the touchEnded()
    function will be called instead if it is defined.
    Browsers may have different default
    behaviors attached to various mouse events. To prevent any default
    behavior for this event, add "return false" to the end of the function."""
    pass


def mouseClicked(event):
    """The mouseClicked() function is called once after a mouse button has been
    pressed and then released.
    Browsers handle clicks differently, so this function is only guaranteed to be
    run when the left mouse button is clicked. To handle other mouse buttons
    being pressed or released, see mousePressed() or mouseReleased().
    Browsers may have different default
    behaviors attached to various mouse events. To prevent any default
    behavior for this event, add "return false" to the end of the function."""
    pass


def doubleClicked(event):
    """The doubleClicked() function is executed every time a event
    listener has detected a dblclick event which is a part of the
    DOM L3 specification. The doubleClicked event is fired when a
    pointing device button (usually a mouse's primary button)
    is clicked twice on a single element. For more info on the
    dblclick event refer to mozilla's documentation here:
    https://developer.mozilla.org/en-US/docs/Web/Events/dblclick"""
    pass


def mouseWheel(event):
    """The function mouseWheel() is executed every time a vertical mouse wheel
    event is detected either triggered by an actual mouse wheel or by a
    touchpad.
    The event.delta property returns the amount the mouse wheel
    have scrolled. The values can be positive or negative depending on the
    scroll direction (on macOS with "natural" scrolling enabled, the signs
    are inverted).
    Browsers may have different default behaviors attached to various
    mouse events. To prevent any default behavior for this event, add
    "return false" to the end of the method.
    Due to the current support of the "wheel" event on Safari, the function
    may only work as expected if "return false" is included while using Safari."""
    pass


def requestPointerLock(*args, **kwargs):
    """The function requestPointerLock()
    locks the pointer to its current position and makes it invisible.
    Use movedX and movedY to get the difference the mouse was moved since
    the last call of draw.
    Note that not all browsers support this feature.
    This enables you to create experiences that aren't limited by the mouse moving out of the screen
    even if it is repeatedly moved into one direction.
    For example, a first person perspective experience."""
    pass


def exitPointerLock(*args, **kwargs):
    """The function exitPointerLock()
    exits a previously triggered pointer Lock
    for example to make ui elements usable etc"""
    pass


def touchStarted(event):
    """The touchStarted() function is called once after every time a touch is
    registered. If no touchStarted() function is defined, the mousePressed()
    function will be called instead if it is defined.
    Browsers may have different default behaviors attached to various touch
    events. To prevent any default behavior for this event, add "return false"
    to the end of the method."""
    pass


def touchMoved(event):
    """The touchMoved() function is called every time a touch move is registered.
    If no touchMoved() function is defined, the mouseDragged() function will
    be called instead if it is defined.
    Browsers may have different default behaviors attached to various touch
    events. To prevent any default behavior for this event, add "return false"
    to the end of the method."""
    pass


def touchEnded(event):
    """The touchEnded() function is called every time a touch ends. If no
    touchEnded() function is defined, the mouseReleased() function will be
    called instead if it is defined.
    Browsers may have different default behaviors attached to various touch
    events. To prevent any default behavior for this event, add "return false"
    to the end of the method."""
    pass


def createImage(width, height):
    """Creates a new p5.Image object. The new image is
    transparent by default.
    createImage() uses the width and height paremeters to set the new
    p5.Image object's dimensions in pixels. The new
    p5.Image can be modified by updating its
    pixels array or by calling its
    get() and
    set() methods. The
    loadPixels() method must be called
    before reading or modifying pixel values. The
    updatePixels() method must be called
    for updates to take effect."""
    pass


def saveCanvas(*args, **kwargs):
    """Saves the current canvas as an image. The browser will either save the
    file immediately or prompt the user with a dialogue window."""
    pass


def saveFrames(filename, extension, duration, framerate, callback):
    """Captures a sequence of frames from the canvas that can be used to create a
    movie. Frames are downloaded as individual image files by default.
    The first parameter, filename, sets the prefix for the file names. For
    example, setting the prefix to 'frame' would generate the image files
    frame0.png, frame1.png, and so on. The second parameter, extension,
    sets the file type to either 'png' or 'jpg'.
    The third parameter, duration, sets the duration to record in seconds.
    The maximum duration is 15 seconds. The fourth parameter, framerate, sets
    the number of frames to record per second. The maximum frame rate value is
    22. Limits are placed on duration and framerate to avoid using too much
    memory. Recording large canvases can easily crash sketches or even web
    browsers.
    The fifth parameter, callback, is optional. If a function is passed,
    image files won't be saved by default. The callback function can be used
    to process an array containing the data for each captured frame. The array
    of image data contains a sequence of objects with three properties for each
    frame: imageData, filename, and extension."""
    pass


def loadImage(path, successCallback, failureCallback):
    """Loads an image to create a p5.Image object.
    loadImage() interprets the first parameter one of three ways. If the path
    to an image file is provided, loadImage() will load it. Paths to local
    files should be relative, such as 'assets/thundercat.jpg'. URLs such as
    'https://example.com/thundercat.jpg' may be blocked due to browser
    security. Raw image data can also be passed as a base64 encoded image in
    the form 'data:image/png;base64,arandomsequenceofcharacters'.
    The second parameter is optional. If a function is passed, it will be
    called once the image has loaded. The callback function can optionally use
    the new p5.Image object.
    The third parameter is also optional. If a function is passed, it will be
    called if the image fails to load. The callback function can optionally use
    the event error.
    Images can take time to load. Calling loadImage() in
    preload() ensures images load before they're
    used in setup() or draw()."""
    pass


def saveGif(filename, duration, options):
    """Generates a gif from a sketch and saves it to a file. saveGif() may be
    called in setup() or at any point while a sketch
    is running.
    The first parameter, fileName, sets the gif's file name. The second
    parameter, duration, sets the gif's duration in seconds.
    The third parameter, options, is optional. If an object is passed,
    saveGif() will use its properties to customize the gif. saveGif()
    recognizes the properties delay, units, silent,
    notificationDuration, and notificationID."""
    pass


def image(*args, **kwargs):
    """Draws a source image to the canvas.
    The first parameter, img, is the source image to be drawn. The second and
    third parameters, dx and dy, set the coordinates of the destination
    image's top left corner. See imageMode() for
    other ways to position images.
    Here's a diagram that explains how optional parameters work in image():

    The fourth and fifth parameters, dw and dh, are optional. They set the
    the width and height to draw the destination image. By default, image()
    draws the full source image at its original size.
    The sixth and seventh parameters, sx and sy, are also optional.
    These coordinates define the top left corner of a subsection to draw from
    the source image.
    The eighth and ninth parameters, sw and sh, are also optional.
    They define the width and height of a subsection to draw from the source
    image. By default, image() draws the full subsection that begins at
    (sx, sy) and extends to the edges of the source image.
    The ninth parameter, fit, is also optional. It enables a subsection of
    the source image to be drawn without affecting its aspect ratio. If
    CONTAIN is passed, the full subsection will appear within the destination
    rectangle. If COVER is passed, the subsection will completely cover the
    destination rectangle. This may have the effect of zooming into the
    subsection.
    The tenth and eleventh paremeters, xAlign and yAlign, are also
    optional. They determine how to align the fitted subsection. xAlign can
    be set to either LEFT, RIGHT, or CENTER. yAlign can be set to
    either TOP, BOTTOM, or CENTER. By default, both xAlign and yAlign
    are set to CENTER."""
    pass


def tint(*args, **kwargs):
    """Tints images using a specified color.
    The version of tint() with one parameter interprets it one of four ways.
    If the parameter is a number, it's interpreted as a grayscale value. If the
    parameter is a string, it's interpreted as a CSS color string. An array of
    [R, G, B, A] values or a p5.Color object can
    also be used to set the tint color.
    The version of tint() with two parameters uses the first one as a
    grayscale value and the second as an alpha value. For example, calling
    tint(255, 128) will make an image 50% transparent.
    The version of tint() with three parameters interprets them as RGB or
    HSB values, depending on the current
    colorMode(). The optional fourth parameter
    sets the alpha value. For example, tint(255, 0, 0, 100) will give images
    a red tint and make them transparent."""
    pass


def noTint(*args, **kwargs):
    """Removes the current tint set by tint() and restores
    images to their original colors."""
    pass


def imageMode(mode):
    """Changes the location from which images are drawn when
    image() is called.
    By default, the first
    two parameters of image() are the x- and
    y-coordinates of the image's upper-left corner. The next parameters are
    its width and height. This is the same as calling imageMode(CORNER).
    imageMode(CORNERS) also uses the first two parameters of
    image() as the x- and y-coordinates of the image's
    top-left corner. The third and fourth parameters are the coordinates of its
    bottom-right corner.
    imageMode(CENTER) uses the first two parameters of
    image() as the x- and y-coordinates of the image's
    center. The next parameters are its width and height."""
    pass


def blend(*args, **kwargs):
    """Copies a region of pixels from one image to another. The blendMode
    parameter blends the images' colors to create different effects."""
    pass


def copy(*args, **kwargs):
    """Copies pixels from a source image to a region of the canvas. The source
    image can be the canvas itself or a p5.Image
    object. copy() will scale pixels from the source region if it isn't the
    same size as the destination region."""
    pass


def filter(*args, **kwargs):
    """Applies an image filter to the canvas. The preset options are:
    INVERT
    Inverts the colors in the image. No parameter is used.
    GRAY
    Converts the image to grayscale. No parameter is used.
    THRESHOLD
    Converts the image to black and white. Pixels with a grayscale value
    above a given threshold are converted to white. The rest are converted to
    black. The threshold must be between 0.0 (black) and 1.0 (white). If no
    value is specified, 0.5 is used.
    OPAQUE
    Sets the alpha channel to entirely opaque. No parameter is used.
    POSTERIZE
    Limits the number of colors in the image. Each color channel is limited to
    the number of colors specified. Values between 2 and 255 are valid, but
    results are most noticeable with lower values. The default value is 4.
    BLUR
    Blurs the image. The level of blurring is specified by a blur radius. Larger
    values increase the blur. The default value is 4. A gaussian blur is used
    in P2D mode. A box blur is used in WEBGL mode.
    ERODE
    Reduces the light areas. No parameter is used.
    DILATE
    Increases the light areas. No parameter is used.
    filter() uses WebGL in the background by default because it's faster.
    This can be disabled in P2D mode by adding a false argument, as in
    filter(BLUR, false). This may be useful to keep computation off the GPU
    or to work around a lack of WebGL support.
    In WEBGL mode, filter() can also use custom shaders. See
    createFilterShader() for more
    information."""
    pass


def get(*args, **kwargs):
    """Gets a pixel or a region of pixels from the canvas.
    get() is easy to use but it's not as fast as
    pixels. Use pixels
    to read many pixel values.
    The version of get() with no parameters returns the entire canvas.
    The version of get() with two parameters interprets them as
    coordinates. It returns an array with the [R, G, B, A] values of the
    pixel at the given point.
    The version of get() with four parameters interprets them as coordinates
    and dimensions. It returns a subsection of the canvas as a
    p5.Image object. The first two parameters are the
    coordinates for the upper-left corner of the subsection. The last two
    parameters are the width and height of the subsection.
    Use p5.Image.get() to work directly with
    p5.Image objects."""
    pass


def loadPixels(*args, **kwargs):
    """Loads the current value of each pixel on the canvas into the
    pixels array. This
    function must be called before reading from or writing to
    pixels."""
    pass


def set(x, y, c):
    """Sets the color of a pixel or draws an image to the canvas.
    set() is easy to use but it's not as fast as
    pixels. Use pixels
    to set many pixel values.
    set() interprets the first two parameters as x- and y-coordinates. It
    interprets the last parameter as a grayscale value, a [R, G, B, A] pixel
    array, a p5.Color object, or a
    p5.Image object. If an image is passed, the first
    two parameters set the coordinates for the image's upper-left corner,
    regardless of the current imageMode().
    updatePixels() must be called after using
    set() for changes to appear."""
    pass


def updatePixels(x, y, w, h):
    """Updates the canvas with the RGBA values in the
    pixels array.
    updatePixels() only needs to be called after changing values in the
    pixels array. Such changes can be made directly
    after calling loadPixels() or by calling
    set()."""
    pass


def loadJSON(*args, **kwargs):
    """Loads a JSON file from a file or a URL, and returns an Object.
    Note that even if the JSON file contains an Array, an Object will be
    returned with index numbers as keys.
    This method is asynchronous, meaning it may not finish before the next
    line in your sketch is executed. JSONP is supported via a polyfill and you
    can pass in as the second argument an object with definitions of the json
    callback following the syntax specified here.
    This method is suitable for fetching files up to size of 64MB."""
    pass


def loadStrings(filename, callback, errorCallback):
    """Reads the contents of a file and creates a String array of its individual
    lines. If the name of the file is used as the parameter, as in the above
    example, the file must be located in the sketch directory/folder.
    Alternatively, the file may be loaded from anywhere on the local
    computer using an absolute path (something that starts with / on Unix and
    Linux, or a drive letter on Windows), or the filename parameter can be a
    URL for a file found on a network.
    This method is asynchronous, meaning it may not finish before the next
    line in your sketch is executed.
    This method is suitable for fetching files up to size of 64MB."""
    pass


def loadTable(filename, extension, header, callback, errorCallback):
    """Reads the contents of a file or URL and creates a p5.Table object with
    its values. If a file is specified, it must be located in the sketch's
    "data" folder. The filename parameter can also be a URL to a file found
    online. By default, the file is assumed to be comma-separated (in CSV
    format). Table only looks for a header row if the 'header' option is
    included.
    This method is asynchronous, meaning it may not finish before the next
    line in your sketch is executed. Calling loadTable() inside preload()
    guarantees to complete the operation before setup() and draw() are called.
    Outside of preload(), you may supply a callback function to handle the
    object:
    All files loaded and saved use UTF-8 encoding. This method is suitable for fetching files up to size of 64MB.
    """
    pass


def loadXML(filename, callback, errorCallback):
    """Reads the contents of a file and creates an XML object with its values.
    If the name of the file is used as the parameter, as in the above example,
    the file must be located in the sketch directory/folder.
    Alternatively, the file maybe be loaded from anywhere on the local
    computer using an absolute path (something that starts with / on Unix and
    Linux, or a drive letter on Windows), or the filename parameter can be a
    URL for a file found on a network.
    This method is asynchronous, meaning it may not finish before the next
    line in your sketch is executed. Calling loadXML() inside preload()
    guarantees to complete the operation before setup() and draw() are called.
    Outside of preload(), you may supply a callback function to handle the
    object.
    This method is suitable for fetching files up to size of 64MB."""
    pass


def loadBytes(file, callback, errorCallback):
    """This method is suitable for fetching files up to size of 64MB."""
    pass


def httpGet(*args, **kwargs):
    """Method for executing an HTTP GET request. If data type is not specified,
    p5 will try to guess based on the URL, defaulting to text. This is equivalent to
    calling httpDo(path, 'GET'). The 'binary' datatype will return
    a Blob object, and the 'arrayBuffer' datatype will return an ArrayBuffer
    which can be used to initialize typed arrays (such as Uint8Array)."""
    pass


def httpPost(*args, **kwargs):
    """Method for executing an HTTP POST request. If data type is not specified,
    p5 will try to guess based on the URL, defaulting to text. This is equivalent to
    calling httpDo(path, 'POST')."""
    pass


def httpDo(*args, **kwargs):
    """Method for executing an HTTP request. If data type is not specified,
    p5 will try to guess based on the URL, defaulting to text.
    For more advanced use, you may also pass in the path as the first argument
    and a object as the second argument, the signature follows the one specified
    in the Fetch API specification.
    This method is suitable for fetching files up to size of 64MB when "GET" is used."""
    pass


def createWriter(name, extension):
    """"""
    pass


def save(objectOrFilename, filename, options):
    """Saves a given element(image, text, json, csv, wav, or html) to the client's
    computer. The first parameter can be a pointer to element we want to save.
    The element can be one of p5.Element,an Array of
    Strings, an Array of JSON, a JSON object, a p5.Table
    , a p5.Image, or a p5.SoundFile (requires
    p5.sound). The second parameter is a filename (including extension).The
    third parameter is for options specific to this type of object. This method
    will save a file that fits the given parameters.
    If it is called without specifying an element, by default it will save the
    whole canvas as an image file. You can optionally specify a filename as
    the first parameter in such a case.
    Note that it is not recommended to
    call this method within draw, as it will open a new save dialog on every
    render."""
    pass


def saveJSON(json, filename, optimize):
    """Writes the contents of an Array or a JSON object to a .json file.
    The file saving process and location of the saved file will
    vary between web browsers."""
    pass


def saveStrings(list, filename, extension, isCRLF):
    """Writes an array of Strings to a text file, one line per String.
    The file saving process and location of the saved file will
    vary between web browsers."""
    pass


def saveTable(Table, filename, options):
    """Writes the contents of a Table object to a file. Defaults to a
    text file with comma-separated-values ('csv') but can also
    use tab separation ('tsv'), or generate an HTML table ('html').
    The file saving process and location of the saved file will
    vary between web browsers."""
    pass


def abs(n):
    """Calculates the absolute value of a number. A number's absolute value is its
    distance from zero on the number line. -5 and 5 are both five units away
    from zero, so calling abs(-5) and abs(5) both return 5. The absolute
    value of a number is always positive."""
    pass


def ceil(n):
    """Calculates the closest integer value that is greater than or equal to the
    parameter's value. For example, calling ceil(9.03) returns the value
    10."""
    pass


def constrain(n, low, high):
    """Constrains a number between a minimum and maximum value."""
    pass


def dist(*args, **kwargs):
    """Calculates the distance between two points.
    The version of dist() with four parameters calculates distance in two
    dimensions.
    The version of dist() with six parameters calculates distance in three
    dimensions.
    Use p5.Vector.dist() to calculate the
    distance between two p5.Vector objects."""
    pass


def exp(n):
    """Returns Euler's number e (2.71828...) raised to the power of the n
    parameter."""
    pass


def floor(n):
    """Calculates the closest integer value that is less than or equal to the
    value of the n parameter."""
    pass


def lerp(start, stop, amt):
    """Calculates a number between two numbers at a specific increment. The amt
    parameter is the amount to interpolate between the two numbers. 0.0 is
    equal to the first number, 0.1 is very near the first number, 0.5 is
    half-way in between, and 1.0 is equal to the second number. The lerp()
    function is convenient for creating motion along a straight path and for
    drawing dotted lines.
    If the value of amt is less than 0 or more than 1, lerp() will return a
    number outside of the original interval. For example, calling
    lerp(0, 10, 1.5) will return 15."""
    pass


def log(n):
    """Calculates the natural logarithm (the base-e logarithm) of a number. This
    function expects the n parameter to be a value greater than 0.0."""
    pass


def mag(x, y):
    """Calculates the magnitude, or length, of a vector. A vector is like an arrow
    pointing in space. Vectors are commonly used for programming motion.
    Vectors don't have a "start" position because the same arrow can be drawn
    anywhere. A vector's magnitude can be thought of as the distance from the
    origin (0, 0) to its tip at (x, y). mag(x, y) is a shortcut for calling
    dist(0, 0, x, y)."""
    pass


def map(value, start1, stop1, start2, stop2, withinBounds):
    """Re-maps a number from one range to another.
    For example, calling map(2, 0, 10, 0, 100) returns 20. The first three
    arguments set the original value to 2 and the original range from 0 to 10.
    The last two arguments set the target range from 0 to 100. 20's position
    in the target range [0, 100] is proportional to 2's position in the
    original range [0, 10]."""
    pass


def max(*args, **kwargs):
    """Returns the largest value in a sequence of numbers.
    The version of max() with one parameter interprets it as an array of
    numbers and returns the largest number.
    The version of max() with two or more parameters interprets them as
    individual numbers and returns the largest number."""
    pass


def min(*args, **kwargs):
    """Returns the smallest value in a sequence of numbers.
    The version of min() with one parameter interprets it as an array of
    numbers and returns the smallest number.
    The version of min() with two or more parameters interprets them as
    individual numbers and returns the smallest number."""
    pass


def norm(value, start, stop):
    """Maps a number from one range to a value between 0 and 1.
    For example, norm(2, 0, 10) returns 0.2. 2's position in the original
    range [0, 10] is proportional to 0.2's position in the range [0, 1]. This
    is equivalent to calling map(2, 0, 10, 0, 1).
    Numbers outside of the original range are not constrained between 0 and 1.
    Out-of-range values are often intentional and useful."""
    pass


def pow(n, e):
    """Calculates exponential expressions such as 2^3.
    For example, pow(2, 3) is equivalent to the expression
    2 × 2 × 2. pow(2, -3) is equivalent to 1 ÷
    (2 × 2 × 2)."""
    pass


def round(n, decimals):
    """Calculates the integer closest to the n parameter. For example,
    round(133.8) returns the value 134."""
    pass


def sq(n):
    """Squares a number, which means multiplying the number by itself. The value
    returned is always a positive number.
    For example, sq(3) evaluates 3 × 3  which is 9. sq(-3) evaluates
    -3 × -3 which is also 9.  Multiplying two negative numbers produces
    a positive number."""
    pass


def sqrt(n):
    """Calculates the square root of a number. A number's square root can be
    multiplied by itself to produce the original number.
    For example, sqrt(9) returns 3 because 3 × 3 = 9. sqrt() always
    returns a positive value. sqrt() doesn't work with negative arguments
    such as sqrt(-9)."""
    pass


def fract(n):
    """Calculates the fractional part of a number. For example,
    fract(12.34) returns 0.34."""
    pass


def createVector(x, y, z):
    """Creates a new p5.Vector object. A vector is like
    an arrow pointing in space. Vectors have both magnitude (length)
    and direction. Calling createVector() without arguments sets the new
    vector's components to 0.
    p5.Vector objects are often used to program
    motion because they simplify the math. For example, a moving ball has a
    position and a velocity. Position describes where the ball is in space. The
    ball's position vector extends from the origin to the ball's center.
    Velocity describes the ball's speed and the direction it's moving. If the
    ball is moving straight up, its velocity vector points straight up. Adding
    the ball's velocity vector to its position vector moves it, as in
    pos.add(vel). Vector math relies on methods inside the
    p5.Vector class."""
    pass


def noise(x, y, z):
    """Returns random numbers that can be tuned to feel more organic. The values
    returned will always be between 0 and 1.
    Values returned by random() and
    randomGaussian() can change by large
    amounts between function calls. By contrast, values returned by noise()
    can be made "smooth". Calls to noise() with similar inputs will produce
    similar outputs. noise() is used to create textures, motion, shapes,
    terrains, and so on. Ken Perlin invented noise() while animating the
    original Tron film in the 1980s.
    noise() returns the same value for a given input while a sketch is
    running. It produces different results each time a sketch runs. The
    noiseSeed() function can be used to generate
    the same sequence of Perlin noise values each time a sketch runs.
    The character of the noise can be adjusted in two ways. The first way is to
    scale the inputs. noise() interprets inputs as coordinates. The sequence
    of noise values will be smoother when the input coordinates are closer. The
    second way is to use the noiseDetail()
    function.
    The version of noise() with one parameter computes noise values in one
    dimension. This dimension can be thought of as space, as in noise(x), or
    time, as in noise(t).
    The version of noise() with two parameters computes noise values in two
    dimensions. These dimensions can be thought of as space, as in
    noise(x, y), or space and time, as in noise(x, t).
    The version of noise() with three parameters computes noise values in
    three dimensions. These dimensions can be thought of as space, as in
    noise(x, y, z), or space and time, as in noise(x, y, t)."""
    pass


def noiseDetail(lod, falloff):
    """Adjusts the character of the noise produced by the
    noise() function.
    Perlin noise values are created by adding layers of noise together. The
    noise layers, called octaves, are similar to harmonics in music. Lower
    octaves contribute more to the output signal. They define the overall
    intensity of the noise. Higher octaves create finer-grained details.
    By default, noise values are created by combining four octaves. Each higher
    octave contributes half as much (50% less) compared to its predecessor.
    noiseDetail() changes the number of octaves and the falloff amount. For
    example, calling noiseDetail(6, 0.25) ensures that
    noise() will use six octaves. Each higher octave
    will contribute 25% as much (75% less) compared to its predecessor. Falloff
    values between 0 and 1 are valid. However, falloff values greater than 0.5
    might result in noise values greater than 1."""
    pass


def noiseSeed(seed):
    """Sets the seed value for noise(). By default,
    noise() produces different results each time
    a sketch is run. Calling noiseSeed() with a constant
    argument, such as noiseSeed(99), makes noise()
    produce the same results each time a sketch is run."""
    pass


def randomSeed(seed):
    """Sets the seed value for random() and
    randomGaussian(). By default,
    random() and
    randomGaussian() produce different
    results each time a sketch is run. Calling randomSeed() with a constant
    argument, such as randomSeed(99), makes these functions produce the same
    results each time a sketch is run."""
    pass


def random(*args, **kwargs):
    """Returns a random number or a random element from an array.
    random() follows uniform distribution, which means that all outcomes are
    equally likely. When random() is used to generate numbers, all
    numbers in the output range are equally likely to be returned. When
    random() is used to select elements from an array, all elements are
    equally likely to be chosen.
    By default, random() produces different results each time a sketch runs.
    The randomSeed() function can be used to
    generate the same sequence of numbers or choices each time a sketch runs.
    The version of random() with no parameters returns a random number from 0
    up to but not including 1.
    The version of random() with one parameter works one of two ways. If the
    argument passed is a number, random() returns a random number from 0 up
    to but not including the number. For example, calling random(5) returns
    values between 0 and 5. If the argument passed is an array, random()
    returns a random element from that array. For example, calling
    random(['🦁', '🐯', '🐻']) returns either a lion, tiger, or bear emoji.
    The version of random() with two parameters returns a random number from
    a given range. The arguments passed set the range's lower and upper bounds.
    For example, calling random(-5, 10.2) returns values from -5 up to but
    not including 10.2."""
    pass


def randomGaussian(mean, sd):
    """Returns a random number fitting a Gaussian, or normal, distribution. Normal
    distributions look like bell curves when plotted. Values from a normal
    distribution cluster around a central value called the mean. The cluster's
    standard deviation describes its spread.
    By default, randomGaussian() produces different results each time a
    sketch runs. The randomSeed() function can be
    used to generate the same sequence of numbers each time a sketch runs.
    There's no minimum or maximum value that randomGaussian() might return.
    Values far from the mean are very unlikely and values near the mean are
    very likely.
    The version of randomGaussian() with no parameters returns values with a
    mean of 0 and standard deviation of 1.
    The version of randomGaussian() with one parameter interprets the
    argument passed as the mean. The standard deviation is 1.
    The version of randomGaussian() with two parameters interprets the first
    argument passed as the mean and the second as the standard deviation."""
    pass


def acos(value):
    """The inverse of cos(), returns the arc cosine of a
    value. This function expects arguments in the range -1 to 1. By default,
    acos() returns values in the range 0 to π (about 3.14). If the
    angleMode() is DEGREES, then values are
    returned in the range 0 to 180."""
    pass


def asin(value):
    """The inverse of sin(), returns the arc sine of a
    value. This function expects input values in the range of -1 to 1. By
    default, asin() returns values in the range -π ÷ 2
    (about -1.57) to π ÷ 2 (about 1.57). If the
    angleMode() is DEGREES then values are
    returned in the range -90 to 90."""
    pass


def atan(value):
    """The inverse of tan(), returns the arc tangent of a
    value. This function expects input values in the range of -Infinity to
    Infinity. By default, atan() returns values in the range -π ÷ 2
    (about -1.57) to π ÷ 2 (about 1.57). If the
    angleMode() is DEGREES then values are
    returned in the range -90 to 90."""
    pass


def atan2(y, x):
    """Calculates the angle formed by a specified point, the origin, and the
    positive x-axis. By default, atan2() returns values in the range
    -π (about -3.14) to π (3.14). If the
    angleMode() is DEGREES, then values are
    returned in the range -180 to 180. The atan2() function is most often
    used for orienting geometry to the mouse's position.
    Note: The y-coordinate of the point is the first parameter and the
    x-coordinate is the second parameter."""
    pass


def cos(angle):
    """Calculates the cosine of an angle. cos() is useful for many geometric
    tasks in creative coding. The values returned oscillate between -1 and 1
    as the input angle increases. cos() takes into account the current
    angleMode."""
    pass


def sin(angle):
    """Calculates the sine of an angle. sin() is useful for many geometric tasks
    in creative coding. The values returned oscillate between -1 and 1 as the
    input angle increases. sin() takes into account the current
    angleMode."""
    pass


def tan(angle):
    """Calculates the tangent of an angle. tan() is useful for many geometric
    tasks in creative coding. The values returned range from -Infinity
    to Infinity and repeat periodically as the input angle increases. tan()
    takes into account the current angleMode."""
    pass


def degrees(radians):
    """Converts an angle measurement in radians to its corresponding value in
    degrees. Degrees and radians are two ways of measuring the same thing.
    There are 360 degrees in a circle and 2 × π (about 6.28)
    radians in a circle. For example, 90° = π ÷ 2 (about 1.57)
    radians. This function doesn't take into account the current
    angleMode()."""
    pass


def radians(degrees):
    """Converts an angle measurement in degrees to its corresponding value in
    radians. Degrees and radians are two ways of measuring the same thing.
    There are 360 degrees in a circle and 2 × π (about 6.28)
    radians in a circle. For example, 90° = π ÷ 2 (about 1.57)
    radians. This function doesn't take into account the current
    angleMode()."""
    pass


def angleMode(*args, **kwargs):
    """Changes the way trigonometric functions interpret angle values. By default,
    the mode is RADIANS.
    Calling angleMode() with no arguments returns current angle mode."""
    pass


def textAlign(*args, **kwargs):
    """Sets the way text is aligned when text() is called.
    By default, calling text('hi', 10, 20) places the bottom-left corner of
    the text's bounding box at (10, 20).
    The first parameter, horizAlign, changes the way
    text() interprets x-coordinates. By default, the
    x-coordinate sets the left edge of the bounding box. textAlign() accepts
    the following values for horizAlign: LEFT, CENTER, or RIGHT.
    The second parameter, vertAlign, is optional. It changes the way
    text() interprets y-coordinates. By default, the
    y-coordinate sets the bottom edge of the bounding box. textAlign()
    accepts the following values for vertAlign: TOP, BOTTOM, CENTER,
    or BASELINE."""
    pass


def textLeading(*args, **kwargs):
    """Sets the spacing between lines of text when
    text() is called. Spacing is measured in pixels.
    Calling textLeading() without an argument returns the current spacing."""
    pass


def textSize(*args, **kwargs):
    """Sets the font size when
    text() is called. Font size is measured in pixels.
    Calling textSize() without an arugment returns the current size."""
    pass


def textStyle(*args, **kwargs):
    """Sets the style for system fonts when
    text() is called. textStyle() accepts the
    following values: NORMAL, ITALIC, BOLD or BOLDITALIC.
    textStyle() may be overridden by CSS styling. This function doesn't
    affect fonts loaded with loadFont()."""
    pass


def textWidth(str):
    """Returns the maximum width of a string of text drawn when
    text() is called."""
    pass


def textAscent(*args, **kwargs):
    """Returns the ascent of the current font at its current size. The ascent
    represents the distance, in pixels, of the tallest character above
    the baseline."""
    pass


def textDescent(*args, **kwargs):
    """Returns the descent of the current font at its current size. The descent
    represents the distance, in pixels, of the character with the longest
    descender below the baseline."""
    pass


def textWrap(style):
    """Sets the style for wrapping text when
    text() is called. textWrap() accepts the
    following values:
    WORD starts new lines of text at spaces. If a string of text doesn't
    have spaces, it may overflow the text box and the canvas. This is the
    default style.
    CHAR starts new lines as needed to stay within the text box.
    textWrap() only works when the maximum width is set for a text box. For
    example, calling text('Have a wonderful day', 0, 10, 100) sets the
    maximum width to 100 pixels.
    Calling textWrap() without an argument returns the current style."""
    pass


def loadFont(path, successCallback, failureCallback):
    """Loads a font and creates a p5.Font object.
    loadFont() can load fonts in either .otf or .ttf format. Loaded fonts can
    be used to style text on the canvas and in HTML elements.
    The first parameter, path, is the path to a font file.
    Paths to local files should be relative. For example,
    'assets/inconsolata.otf'. The Inconsolata font used in the following
    examples can be downloaded for free
    here.
    Paths to remote files should be URLs. For example,
    'https://example.com/inconsolata.otf'. URLs may be blocked due to browser
    security.
    The second parameter, successCallback, is optional. If a function is
    passed, it will be called once the font has loaded. The callback function
    may use the new p5.Font object if needed.
    The third parameter, failureCallback, is also optional. If a function is
    passed, it will be called if the font fails to load. The callback function
    may use the error
    Event
    object if needed.
    Fonts can take time to load. Calling loadFont() in
    preload() ensures fonts load before they're
    used in setup() or
    draw()."""
    pass


def text(str, x, y, maxWidth, maxHeight):
    """Draws text to the canvas.
    The first parameter, str, is the text to be drawn. The second and third
    parameters, x and y, set the coordinates of the text's bottom-left
    corner. See textAlign() for other ways to
    align text.
    The fourth and fifth parameters, maxWidth and maxHeight, are optional.
    They set the dimensions of the invisible rectangle containing the text. By
    default, they set its  maximum width and height. See
    rectMode() for other ways to define the
    rectangular text box. Text will wrap to fit within the text box. Text
    outside of the box won't be drawn.
    Text can be styled a few ways. Call the fill()
    function to set the text's fill color. Call
    stroke() and
    strokeWeight() to set the text's outline.
    Call textSize() and
    textFont() to set the text's size and font,
    respectively.
    Note: WEBGL mode only supports fonts loaded with
    loadFont(). Calling
    stroke() has no effect in WEBGL mode."""
    pass


def textFont(*args, **kwargs):
    """Sets the font used by the text() function.
    The first parameter, font, sets the font. textFont() recognizes either
    a p5.Font object or a string with the name of a
    system font. For example, 'Courier New'.
    The second parameter, size, is optional. It sets the font size in pixels.
    This has the same effect as calling textSize().
    Note: WEBGL mode only supports fonts loaded with
    loadFont()."""
    pass


def shuffle(array, bool):
    """Randomizes the order of the elements of an array. Implements

    Fisher-Yates Shuffle Algorithm."""
    pass


def float(str):
    """Converts a string to its floating point representation. The contents of a
    string must resemble a number, or NaN (not a number) will be returned.
    For example, float("1234.56") evaluates to 1234.56, but float("giraffe")
    will return NaN.
    When an array of values is passed in, then an array of floats of the same
    length is returned."""
    pass


def int(*args, **kwargs):
    """Converts a boolean, string, or float to its integer representation.
    When an array of values is passed in, then an int array of the same length
    is returned."""
    pass


def str(n):
    """Converts a boolean, string or number to its string representation.
    When an array of values is passed in, then an array of strings of the same
    length is returned."""
    pass


def boolean(n):
    """Converts a number or string to its boolean representation.
    For a number, any non-zero value (positive or negative) evaluates to true,
    while zero evaluates to false. For a string, the value "true" evaluates to
    true, while any other value evaluates to false. When an array of number or
    string values is passed in, then a array of booleans of the same length is
    returned."""
    pass


def byte(*args, **kwargs):
    """Converts a number, string representation of a number, or boolean to its byte
    representation. A byte can be only a whole number between -128 and 127, so
    when a value outside of this range is converted, it wraps around to the
    corresponding byte representation. When an array of number, string or boolean
    values is passed in, then an array of bytes the same length is returned."""
    pass


def char(*args, **kwargs):
    """Converts a number or string to its corresponding single-character
    string representation. If a string parameter is provided, it is first
    parsed as an integer and then translated into a single-character string.
    When an array of number or string values is passed in, then an array of
    single-character strings of the same length is returned."""
    pass


def unchar(*args, **kwargs):
    """Converts a single-character string to its corresponding integer
    representation. When an array of single-character string values is passed
    in, then an array of integers of the same length is returned."""
    pass


def hex(*args, **kwargs):
    """Converts a number to a string in its equivalent hexadecimal notation. If a
    second parameter is passed, it is used to set the number of characters to
    generate in the hexadecimal notation. When an array is passed in, an
    array of strings in hexadecimal notation of the same length is returned."""
    pass


def unhex(*args, **kwargs):
    """Converts a string representation of a hexadecimal number to its equivalent
    integer value. When an array of strings in hexadecimal notation is passed
    in, an array of integers of the same length is returned."""
    pass


def join(list, separator):
    """Combines an array of Strings into one String, each separated by the
    character(s) used for the separator parameter. To join arrays of ints or
    floats, it's necessary to first convert them to Strings using nf() or
    nfs()."""
    pass


def match(str, regexp):
    """This function is used to apply a regular expression to a piece of text,
    and return matching groups (elements found inside parentheses) as a
    String array. If there are no matches, a null value will be returned.
    If no groups are specified in the regular expression, but the sequence
    matches, an array of length 1 (with the matched text as the first element
    of the array) will be returned.
    To use the function, first check to see if the result is null. If the
    result is null, then the sequence did not match at all. If the sequence
    did match, an array is returned.
    If there are groups (specified by sets of parentheses) in the regular
    expression, then the contents of each will be returned in the array.
    Element [0] of a regular expression match returns the entire matching
    string, and the match groups start at element [1] (the first group is [1],
    the second [2], and so on)."""
    pass


def matchAll(str, regexp):
    """This function is used to apply a regular expression to a piece of text,
    and return a list of matching groups (elements found inside parentheses)
    as a two-dimensional String array. If there are no matches, a null value
    will be returned. If no groups are specified in the regular expression,
    but the sequence matches, a two dimensional array is still returned, but
    the second dimension is only of length one.
    To use the function, first check to see if the result is null. If the
    result is null, then the sequence did not match at all. If the sequence
    did match, a 2D array is returned.
    If there are groups (specified by sets of parentheses) in the regular
    expression, then the contents of each will be returned in the array.
    Assuming a loop with counter variable i, element [i][0] of a regular
    expression match returns the entire matching string, and the match groups
    start at element [i][1] (the first group is [i][1], the second [i][2],
    and so on)."""
    pass


def nf(*args, **kwargs):
    """Utility function for formatting numbers into strings. There are two
    versions: one for formatting floats, and one for formatting ints.
    The values for the digits, left, and right parameters should always
    be positive integers.
    (NOTE): Be cautious when using left and right parameters as it prepends numbers of 0's if the parameter
    if greater than the current length of the number.
    For example if number is 123.2 and left parameter passed is 4 which is greater than length of 123
    (integer part) i.e 3 than result will be 0123.2. Same case for right parameter i.e. if right is 3 than
    the result will be 123.200."""
    pass


def nfc(*args, **kwargs):
    """Utility function for formatting numbers into strings and placing
    appropriate commas to mark units of 1000. There are two versions: one
    for formatting ints, and one for formatting an array of ints. The value
    for the right parameter should always be a positive integer."""
    pass


def nfp(*args, **kwargs):
    """Utility function for formatting numbers into strings. Similar to nf() but
    puts a "+" in front of positive numbers and a "-" in front of negative
    numbers. There are two versions: one for formatting floats, and one for
    formatting ints. The values for left, and right parameters
    should always be positive integers."""
    pass


def nfs(*args, **kwargs):
    """Utility function for formatting numbers into strings. Similar to nf() but
    puts an additional "_" (space) in front of positive numbers just in case to align it with negative
    numbers which includes "-" (minus) sign.
    The main usecase of nfs() can be seen when one wants to align the digits (place values) of a non-negative
    number with some negative number (See the example to get a clear picture).
    There are two versions: one for formatting float, and one for formatting int.
    The values for the digits, left, and right parameters should always be positive integers.
    (IMP): The result on the canvas basically the expected alignment can vary based on the typeface you are using.
    (NOTE): Be cautious when using left and right parameters as it prepends numbers of 0's if the parameter
    if greater than the current length of the number.
    For example if number is 123.2 and left parameter passed is 4 which is greater than length of 123
    (integer part) i.e 3 than result will be 0123.2. Same case for right parameter i.e. if right is 3 than
    the result will be 123.200."""
    pass


def split(value, delim):
    """The split() function maps to String.split(), it breaks a String into
    pieces using a character or string as the delimiter. The delim parameter
    specifies the character or characters that mark the boundaries between
    each piece. A String[] array is returned that contains each of the pieces.
    The splitTokens() function works in a similar fashion, except that it
    splits using a range of characters instead of a specific character or
    sequence."""
    pass


def splitTokens(value, delim):
    """The splitTokens() function splits a String at one or many character
    delimiters or "tokens." The delim parameter specifies the character or
    characters to be used as a boundary.
    If no delim characters are specified, any whitespace character is used to
    split. Whitespace characters include tab (\t), line feed (\n), carriage
    return (\r), form feed (\f), and space."""
    pass


def trim(*args, **kwargs):
    """Removes whitespace characters from the beginning and end of a String. In
    addition to standard whitespace characters such as space, carriage return,
    and tab, this function also removes the Unicode "nbsp" character."""
    pass


def day(*args, **kwargs):
    """p5.js communicates with the clock on your computer. The day() function
    returns the current day as a value from 1 - 31."""
    pass


def hour(*args, **kwargs):
    """p5.js communicates with the clock on your computer. The hour() function
    returns the current hour as a value from 0 - 23."""
    pass


def minute(*args, **kwargs):
    """p5.js communicates with the clock on your computer. The minute() function
    returns the current minute as a value from 0 - 59."""
    pass


def millis(*args, **kwargs):
    """Returns the number of milliseconds (thousandths of a second) since
    starting the sketch (when setup() is called). This information is often
    used for timing events and animation sequences."""
    pass


def month(*args, **kwargs):
    """p5.js communicates with the clock on your computer. The month() function
    returns the current month as a value from 1 - 12."""
    pass


def second(*args, **kwargs):
    """p5.js communicates with the clock on your computer. The second() function
    returns the current second as a value from 0 - 59."""
    pass


def year(*args, **kwargs):
    """p5.js communicates with the clock on your computer. The year() function
    returns the current year as an integer (2014, 2015, 2016, etc)."""
    pass


def beginGeometry(*args, **kwargs):
    """Starts creating a new p5.Geometry. Subsequent shapes drawn will be added
    to the geometry and then returned when
    endGeometry() is called. One can also use
    buildGeometry() to pass a function that
    draws shapes.
    If you need to draw complex shapes every frame which don't change over time,
    combining them upfront with beginGeometry() and endGeometry() and then
    drawing that will run faster than repeatedly drawing the individual pieces."""
    pass


def endGeometry(*args, **kwargs):
    """Finishes creating a new p5.Geometry that was
    started using beginGeometry(). One can also
    use buildGeometry() to pass a function that
    draws shapes."""
    pass


def buildGeometry(callback):
    """Creates a new p5.Geometry that contains all
    the shapes drawn in a provided callback function. The returned combined shape
    can then be drawn all at once using model().
    If you need to draw complex shapes every frame which don't change over time,
    combining them with buildGeometry() once and then drawing that will run
    faster than repeatedly drawing the individual pieces.
    One can also draw shapes directly between
    beginGeometry() and
    endGeometry() instead of using a callback
    function."""
    pass


def freeGeometry(geometry):
    """Clears the resources of a model to free up browser memory. A model whose
    resources have been cleared can still be drawn, but the first time it is
    drawn again, it might take longer.
    This method works on models generated with
    buildGeometry() as well as those loaded
    from loadModel()."""
    pass


def plane(width, height, detailX, detailY):
    """Draw a plane with given a width and height"""
    pass


def box(width, height, depth, detailX, detailY):
    """Draw a box with given width, height and depth"""
    pass


def sphere(radius, detailX, detailY):
    """Draw a sphere with given radius.
    DetailX and detailY determines the number of subdivisions in the x-dimension
    and the y-dimension of a sphere. More subdivisions make the sphere seem
    smoother. The recommended maximum values are both 24. Using a value greater
    than 24 may cause a warning or slow down the browser."""
    pass


def cylinder(radius, height, detailX, detailY, bottomCap, topCap):
    """Draw a cylinder with given radius and height
    DetailX and detailY determines the number of subdivisions in the x-dimension
    and the y-dimension of a cylinder. More subdivisions make the cylinder seem smoother.
    The recommended maximum value for detailX is 24. Using a value greater than 24
    may cause a warning or slow down the browser."""
    pass


def cone(radius, height, detailX, detailY, cap):
    """Draw a cone with given radius and height
    DetailX and detailY determine the number of subdivisions in the x-dimension and
    the y-dimension of a cone. More subdivisions make the cone seem smoother. The
    recommended maximum value for detailX is 24. Using a value greater than 24
    may cause a warning or slow down the browser."""
    pass


def ellipsoid(radiusx, radiusy, radiusz, detailX, detailY):
    """Draw an ellipsoid with given radius
    DetailX and detailY determine the number of subdivisions in the x-dimension and
    the y-dimension of a cone. More subdivisions make the ellipsoid appear to be smoother.
    Avoid detail number above 150, it may crash the browser."""
    pass


def torus(radius, tubeRadius, detailX, detailY):
    """Draw a torus with given radius and tube radius
    DetailX and detailY determine the number of subdivisions in the x-dimension and
    the y-dimension of a torus. More subdivisions make the torus appear to be smoother.
    The default and maximum values for detailX and detailY are 24 and 16, respectively.
    Setting them to relatively small values like 4 and 6 allows you to create new
    shapes other than a torus."""
    pass


def orbitControl(sensitivityX, sensitivityY, sensitivityZ, options):
    """Allows movement around a 3D sketch using a mouse or trackpad or touch.
    Left-clicking and dragging or swipe motion will rotate the camera position
    about the center of the sketch, right-clicking and dragging or multi-swipe
    will pan the camera position without rotation, and using the mouse wheel
    (scrolling) or pinch in/out will move the camera further or closer
    from the center of the sketch. This function can be called with parameters
    dictating sensitivity to mouse/touch movement along the X and Y axes.
    Calling this function without parameters is equivalent to calling
    orbitControl(1,1). To reverse direction of movement in either axis,
    enter a negative number for sensitivity."""
    pass


def debugMode(*args, **kwargs):
    """debugMode() helps visualize 3D space by adding a grid to indicate where the
    ‘ground’ is in a sketch and an axes icon which indicates the +X, +Y, and +Z
    directions. This function can be called without parameters to create a
    default grid and axes icon, or it can be called according to the examples
    above to customize the size and position of the grid and/or axes icon.  The
    grid is drawn using the most recently set stroke color and weight.  To
    specify these parameters, add a call to stroke() and strokeWeight()
    just before the end of the draw() loop.
    By default, the grid will run through the origin (0,0,0) of the sketch
    along the XZ plane
    and the axes icon will be offset from the origin.  Both the grid and axes
    icon will be sized according to the current canvas size.  Note that because the
    grid runs parallel to the default camera view, it is often helpful to use
    debugMode along with orbitControl to allow full view of the grid."""
    pass


def noDebugMode(*args, **kwargs):
    """Turns off debugMode() in a 3D sketch."""
    pass


def ambientLight(*args, **kwargs):
    """Creates an ambient light with the given color.
    Ambient light does not come from a specific direction.
    Objects are evenly lit from all sides. Ambient lights are
    almost always used in combination with other types of lights.
    Note: lights need to be called (whether directly or indirectly)
    within draw() to remain persistent in a looping program.
    Placing them in setup() will cause them to only have an effect
    the first time through the loop."""
    pass


def specularColor(*args, **kwargs):
    """Sets the color of the specular highlight of a non-ambient light
    (i.e. all lights except ambientLight()).
    specularColor() affects only the lights which are created after
    it in the code.
    This function is used in combination with
    specularMaterial().
    If a geometry does not use specularMaterial(), this function
    will have no effect.
    The default color is white (255, 255, 255), which is used if
    specularColor() is not explicitly called.
    Note: specularColor is equivalent to the Processing function
    lightSpecular."""
    pass


def directionalLight(*args, **kwargs):
    """Creates a directional light with the given color and direction.
    Directional light comes from one direction.
    The direction is specified as numbers inclusively between -1 and 1.
    For example, setting the direction as (0, -1, 0) will cause the
    geometry to be lit from below (since the light will be facing
    directly upwards). Similarly, setting the direction as (1, 0, 0)
    will cause the geometry to be lit from the left (since the light
    will be facing directly rightwards).
    Directional lights do not have a specific point of origin, and
    therefore cannot be positioned closer or farther away from a geometry.
    A maximum of 5 directional lights can be active at once.
    Note: lights need to be called (whether directly or indirectly)
    within draw() to remain persistent in a looping program.
    Placing them in setup() will cause them to only have an effect
    the first time through the loop."""
    pass


def pointLight(*args, **kwargs):
    """Creates a point light with the given color and position.
    A point light emits light from a single point in all directions.
    Because the light is emitted from a specific point (position),
    it has a different effect when it is positioned farther vs. nearer
    an object.
    A maximum of 5 point lights can be active at once.
    Note: lights need to be called (whether directly or indirectly)
    within draw() to remain persistent in a looping program.
    Placing them in setup() will cause them to only have an effect
    the first time through the loop."""
    pass


def imageLight(img):
    """Creates an image light with the given image.
    The image light simulates light from all the directions.
    This is done by using the image as a texture for an infinitely
    large sphere light. This sphere contains
    or encapsulates the whole scene/drawing.
    It will have different effect for varying shininess of the
    object in the drawing.
    Under the hood it is mainly doing 2 types of calculations,
    the first one is creating an irradiance map the
    environment map of the input image.
    The second one is managing reflections based on the shininess
    or roughness of the material used in the scene.
    Note: The image's diffuse light will be affected by fill()
    and the specular reflections will be affected by specularMaterial()
    and shininess()."""
    pass


def lights(*args, **kwargs):
    """Places an ambient and directional light in the scene.
    The lights are set to ambientLight(128, 128, 128) and
    directionalLight(128, 128, 128, 0, 0, -1).
    Note: lights need to be called (whether directly or indirectly)
    within draw() to remain persistent in a looping program.
    Placing them in setup() will cause them to only have an effect
    the first time through the loop."""
    pass


def lightFalloff(constant, linear, quadratic):
    """Sets the falloff rate for pointLight()
    and spotLight().
    lightFalloff() affects only the lights which are created after it
    in the code.
    The constant, linear, an quadratic parameters are used to calculate falloff as follows:
    d = distance from light position to vertex position
    falloff = 1 / (CONSTANT + d * LINEAR + (d * d) * QUADRATIC)"""
    pass


def spotLight(*args, **kwargs):
    """Creates a spot light with the given color, position,
    light direction, angle, and concentration.
    Like a pointLight(), a spotLight()
    emits light from a specific point (position). It has a different effect
    when it is positioned farther vs. nearer an object.
    However, unlike a pointLight(), the light is emitted in one direction
    along a conical shape. The shape of the cone can be controlled using
    the angle and concentration parameters.
    The angle parameter is used to
    determine the radius of the cone. And the concentration
    parameter is used to focus the light towards the center of
    the cone. Both parameters are optional, however if you want
    to specify concentration, you must also specify angle.
    The minimum concentration value is 1.
    A maximum of 5 spot lights can be active at once.
    Note: lights need to be called (whether directly or indirectly)
    within draw() to remain persistent in a looping program.
    Placing them in setup() will cause them to only have an effect
    the first time through the loop."""
    pass


def noLights(*args, **kwargs):
    """Removes all lights present in a sketch.
    All subsequent geometry is rendered without lighting (until a new
    light is created with a call to one of the lighting functions
    (lights(),
    ambientLight(),
    directionalLight(),
    pointLight(),
    spotLight())."""
    pass


def loadModel(*args, **kwargs):
    """Load a 3d model from an OBJ or STL file.
    loadModel() should be placed inside of preload().
    This allows the model to load fully before the rest of your code is run.
    One of the limitations of the OBJ and STL format is that it doesn't have a built-in
    sense of scale. This means that models exported from different programs might
    be very different sizes. If your model isn't displaying, try calling
    loadModel() with the normalized parameter set to true. This will resize the
    model to a scale appropriate for p5. You can also make additional changes to
    the final size of your model with the scale() function.
    Also, the support for colored STL files is not present. STL files with color will be
    rendered without color properties."""
    pass


def model(model):
    """Render a 3d model to the screen."""
    pass


def loadShader(vertFilename, fragFilename, callback, errorCallback):
    """Creates a new p5.Shader object
    from the provided vertex and fragment shader files.
    The shader files are loaded asynchronously in the
    background, so this method should be used in preload().
    Shaders can alter the positioning of shapes drawn with them.
    To ensure consistency in rendering, it's recommended to use the vertex shader in the createShader example.
    Note, shaders can only be used in WEBGL mode."""
    pass


def createShader(vertSrc, fragSrc):
    """Creates a new p5.Shader object
    from the provided vertex and fragment shader code.
    Note, shaders can only be used in WEBGL mode.
    Shaders can alter the positioning of shapes drawn with them.
    To ensure consistency in rendering, it's recommended to use the vertex shader shown in the example below.
    """
    pass


def createFilterShader(fragSrc):
    """Creates a new p5.Shader using only a fragment shader, as a convenience method for creating image effects.
    It's like createShader() but with a default vertex shader included.
    createFilterShader() is intended to be used along with filter() for filtering the contents of a canvas.
    A filter shader will not be applied to any geometries.
    The fragment shader receives some uniforms:

    sampler2D tex0, which contains the canvas contents as a texture
    vec2 canvasSize, which is the p5 width and height of the canvas (not including pixel density)
    vec2 texelSize, which is the size of a physical pixel including pixel density (1.0/(width*density), 1.0/(height*density))

    For more info about filters and shaders, see Adam Ferriss' repo of shader examples
    or the introduction to shaders page."""
    pass


def shader(s):
    """Sets the p5.Shader object to
    be used to render subsequent shapes.
    Shaders can alter the positioning of shapes drawn with them.
    To ensure consistency in rendering, it's recommended to use the vertex shader in the createShader example.
    Custom shaders can be created using the
    createShader() and
    loadShader() functions.
    Use resetShader() to
    restore the default shaders.
    Note, shaders can only be used in WEBGL mode."""
    pass


def resetShader(*args, **kwargs):
    """Restores the default shaders. Code that runs after resetShader()
    will not be affected by the shader previously set by
    shader()"""
    pass


def texture(tex):
    """Sets the texture that will be used to render subsequent shapes.
    A texture is like a "skin" that wraps around a 3D geometry. Currently
    supported textures are images, video, and offscreen renders.
    To texture a geometry created with beginShape(),
    you will need to specify uv coordinates in vertex().
    Note, texture() can only be used in WEBGL mode.
    You can view more materials in this
    example."""
    pass


def textureMode(mode):
    """Sets the coordinate space for texture mapping. The default mode is IMAGE
    which refers to the actual coordinates of the image.
    NORMAL refers to a normalized space of values ranging from 0 to 1.
    With IMAGE, if an image is 100×200 pixels, mapping the image onto the entire
    size of a quad would require the points (0,0) (100, 0) (100,200) (0,200).
    The same mapping in NORMAL is (0,0) (1,0) (1,1) (0,1)."""
    pass


def textureWrap(wrapX, wrapY):
    """Sets the global texture wrapping mode. This controls how textures behave
    when their uv's go outside of the 0 to 1 range. There are three options:
    CLAMP, REPEAT, and MIRROR.
    CLAMP causes the pixels at the edge of the texture to extend to the bounds.
    REPEAT causes the texture to tile repeatedly until reaching the bounds.
    MIRROR works similarly to REPEAT but it flips the texture with every new tile.
    REPEAT & MIRROR are only available if the texture
    is a power of two size (128, 256, 512, 1024, etc.).
    This method will affect all textures in your sketch until a subsequent
    textureWrap() call is made.
    If only one argument is provided, it will be applied to both the
    horizontal and vertical axes."""
    pass


def normalMaterial(*args, **kwargs):
    """Sets the current material as a normal material.
    A normal material is not affected by light. It is often used as
    a placeholder material when debugging.
    Surfaces facing the X-axis become red, those facing the Y-axis
    become green, and those facing the Z-axis become blue.
    You can view more materials in this
    example."""
    pass


def ambientMaterial(*args, **kwargs):
    """Sets the ambient color of the material.
    The ambientMaterial() color represents the components
    of the ambientLight() color that the object reflects.
    Consider an ambientMaterial() with the color yellow (255, 255, 0).
    If the ambientLight() emits the color white (255, 255, 255), then the object
    will appear yellow as it will reflect the red and green components
    of the light. If the ambientLight() emits the color red (255, 0, 0), then
    the object will appear red as it will reflect the red component
    of the light. If the ambientLight() emits the color blue (0, 0, 255),
    then the object will appear black, as there is no component of
    the light that it can reflect.
    You can view more materials in this
    example."""
    pass


def emissiveMaterial(*args, **kwargs):
    """Sets the emissive color of the material.
    An emissive material will display the emissive color at
    full strength regardless of lighting. This can give the
    appearance that the object is glowing.
    Note, "emissive" is a misnomer in the sense that the material
    does not actually emit light that will affect surrounding objects.
    You can view more materials in this
    example."""
    pass


def specularMaterial(*args, **kwargs):
    """Sets the specular color of the material.
    A specular material is reflective (shiny). The shininess can be
    controlled by the shininess() function.
    Like ambientMaterial(),
    the specularMaterial() color is the color the object will reflect
    under ambientLight().
    However unlike ambientMaterial(), for all other types of lights
    (directionalLight(),
    pointLight(),
    spotLight()),
    a specular material will reflect the color of the light source.
    This is what gives it its "shiny" appearance.
    You can view more materials in this
    example."""
    pass


def shininess(shine):
    """Sets the amount of gloss ("shininess") of a
    specularMaterial().
    The default and minimum value is 1."""
    pass


def camera(x, y, z, centerX, centerY, centerZ, upX, upY, upZ):
    """Sets the position of the current camera in a 3D sketch.
    Parameters for this function define the camera's position,
    the center of the sketch (where the camera is pointing),
    and an up direction (the orientation of the camera).
    This function simulates the movements of the camera, allowing objects to be
    viewed from various angles. Remember, it does not move the objects themselves
    but the camera instead. For example when the centerX value is positive,
    and the camera is rotating to the right side of the sketch,
    the object will seem like it's moving to the left.
    See this example
    to view the position of your camera.
    If no parameters are given, the following default is used:
    camera(0, 0, (height/2) / tan(PI/6), 0, 0, 0, 0, 1, 0)"""
    pass


def perspective(fovy, aspect, near, far):
    """Sets a perspective projection for the current camera in a 3D sketch.
    This projection represents depth through foreshortening: objects
    that are close to the camera appear their actual size while those
    that are further away from the camera appear smaller.
    The parameters to this function define the viewing frustum
    (the truncated pyramid within which objects are seen by the camera) through
    vertical field of view, aspect ratio (usually width/height), and near and far
    clipping planes.
    If no parameters are given, the default values are used as:

    fov : The default field of view for the camera is such that the full height of renderer is visible when it is positioned at a default distance of 800 units from the camera.
    aspect : The default aspect ratio is the ratio of renderer's width to renderer's height.
    near : The default value for the near clipping plane is 80, which is 0.1 times the default distance from the camera to its subject.
    far : The default value for the far clipping plane is 8000, which is 10 times the default distance from the camera to its subject.

    If you prefer a fixed field of view, follow these steps:

    Choose your desired field of view angle (fovy). This is how wide the camera can see.
    To ensure that you can see the entire width across horizontally and height across vertically, place the camera a distance of (height / 2) / tan(fovy / 2) back from its subject.
    Call perspective with the chosen field of view, canvas aspect ratio, and near/far values:
    perspective(fovy, width / height, cameraDistance / 10, cameraDistance * 10);
    """
    pass


def ortho(left, right, bottom, top, near, far):
    """Sets an orthographic projection for the current camera in a 3D sketch
    and defines a box-shaped viewing frustum within which objects are seen.
    In this projection, all objects with the same dimension appear the same
    size, regardless of whether they are near or far from the camera.
    The parameters to this function specify the viewing frustum where
    left and right are the minimum and maximum x values, top and bottom are
    the minimum and maximum y values, and near and far are the minimum and
    maximum z values.
    If no parameters are given, the following default is used:
    ortho(-width/2, width/2, -height/2, height/2)."""
    pass


def frustum(left, right, bottom, top, near, far):
    """Sets the frustum of the current camera as defined by
    the parameters.
    A frustum is a geometric form: a pyramid with its top
    cut off. With the viewer's eye at the imaginary top of
    the pyramid, the six planes of the frustum act as clipping
    planes when rendering a 3D view. Thus, any form inside the
    clipping planes is visible; anything outside
    those planes is not visible.
    Setting the frustum changes the perspective of the scene being rendered.
    This can be achieved more simply in many cases by using
    perspective().
    If no parameters are given, the following default is used:
    frustum(-width/20, width/20, height/20, -height/20, eyeZ/10, eyeZ*10),
    where eyeZ is equal to ((height/2) / tan(PI/6))."""
    pass


def createCamera(*args, **kwargs):
    """Creates a new p5.Camera object and sets it
    as the current (active) camera.
    The new camera is initialized with a default position
    (see camera())
    and a default perspective projection
    (see perspective()).
    Its properties can be controlled with the p5.Camera
    methods.
    Note: Every 3D sketch starts with a default camera initialized.
    This camera can be controlled with the global methods
    camera(),
    perspective(), ortho(),
    and frustum() if it is the only camera
    in the scene."""
    pass


def setCamera(cam):
    """Sets the current (active) camera of a 3D sketch.
    Allows for switching between multiple cameras."""
    pass


def vertexNormal(x, y, z, v):
    """Sets the normal to use for subsequent vertices."""
    pass


def setAttributes(*args, **kwargs):
    """Set attributes for the WebGL Drawing context.
    This is a way of adjusting how the WebGL
    renderer works to fine-tune the display and performance.
    Note that this will reinitialize the drawing context
    if called after the WebGL canvas is made.
    If an object is passed as the parameter, all attributes
    not declared in the object will be set to defaults.
    The available attributes are:

    alpha - indicates if the canvas contains an alpha buffer
    default is true
    depth - indicates whether the drawing buffer has a depth buffer
    of at least 16 bits - default is true
    stencil - indicates whether the drawing buffer has a stencil buffer
    of at least 8 bits
    antialias - indicates whether or not to perform anti-aliasing
    default is false (true in Safari)
    premultipliedAlpha - indicates that the page compositor will assume
    the drawing buffer contains colors with pre-multiplied alpha
    default is true
    preserveDrawingBuffer - if true the buffers will not be cleared and
    and will preserve their values until cleared or overwritten by author
    (note that p5 clears automatically on draw loop)
    default is true
    perPixelLighting - if true, per-pixel lighting will be used in the
    lighting shader otherwise per-vertex lighting is used.
    default is true.
    version - either 1 or 2, to specify which WebGL version to ask for. By
    default, WebGL 2 will be requested. If WebGL2 is not available, it will
    fall back to WebGL 1. You can check what version is used with by looking at
    the global webglVersion property."""
    pass


VERSION = None
P2D = None
WEBGL = None
WEBGL2 = None
ARROW = None
CROSS = None
HAND = None
MOVE = None
TEXT = None
WAIT = None
HALF_PI = None
PI = None
QUARTER_PI = None
TAU = None
TWO_PI = None
DEGREES = None
RADIANS = None
CORNER = None
CORNERS = None
RADIUS = None
RIGHT = None
LEFT = None
CENTER = None
TOP = None
BOTTOM = None
BASELINE = None
POINTS = None
LINES = None
LINE_STRIP = None
LINE_LOOP = None
TRIANGLES = None
TRIANGLE_FAN = None
TRIANGLE_STRIP = None
QUADS = None
QUAD_STRIP = None
TESS = None
CLOSE = None
OPEN = None
CHORD = None
PIE = None
PROJECT = None
SQUARE = None
ROUND = None
BEVEL = None
MITER = None
RGB = None
HSB = None
HSL = None
AUTO = None
ALT = None
BACKSPACE = None
CONTROL = None
DELETE = None
DOWN_ARROW = None
ENTER = None
ESCAPE = None
LEFT_ARROW = None
OPTION = None
RETURN = None
RIGHT_ARROW = None
SHIFT = None
TAB = None
UP_ARROW = None
BLEND = None
REMOVE = None
ADD = None
DARKEST = None
LIGHTEST = None
DIFFERENCE = None
SUBTRACT = None
EXCLUSION = None
MULTIPLY = None
SCREEN = None
REPLACE = None
OVERLAY = None
HARD_LIGHT = None
SOFT_LIGHT = None
DODGE = None
BURN = None
THRESHOLD = None
GRAY = None
OPAQUE = None
INVERT = None
POSTERIZE = None
DILATE = None
ERODE = None
BLUR = None
NORMAL = None
ITALIC = None
BOLD = None
BOLDITALIC = None
CHAR = None
WORD = None
LINEAR = None
QUADRATIC = None
BEZIER = None
CURVE = None
STROKE = None
FILL = None
TEXTURE = None
IMMEDIATE = None
IMAGE = None
NEAREST = None
REPEAT = None
CLAMP = None
MIRROR = None
FLAT = None
SMOOTH = None
LANDSCAPE = None
PORTRAIT = None
GRID = None
AXES = None
LABEL = None
FALLBACK = None
CONTAIN = None
COVER = None
UNSIGNED_BYTE = None
UNSIGNED_INT = None
FLOAT = None
HALF_FLOAT = None
RGBA = None
frameCount = None
deltaTime = None
focused = None
webglVersion = None
displayWidth = None
displayHeight = None
windowWidth = None
windowHeight = None
width = None
height = None
disableFriendlyErrors = None
drawingContext = None
deviceOrientation = None
accelerationX = None
accelerationY = None
accelerationZ = None
pAccelerationX = None
pAccelerationY = None
pAccelerationZ = None
rotationX = None
rotationY = None
rotationZ = None
pRotationX = None
pRotationY = None
pRotationZ = None
turnAxis = None
keyIsPressed = None
key = None
keyCode = None
movedX = None
movedY = None
mouseX = None
mouseY = None
pmouseX = None
pmouseY = None
winMouseX = None
winMouseY = None
pwinMouseX = None
pwinMouseY = None
mouseButton = None
mouseIsPressed = None
touches = None
pixels = None
