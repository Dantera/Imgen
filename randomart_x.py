import random, math
from PIL import Image

random.seed()


class X:
    def eval(self, x, y):
        return x

    def __str__(self):
        return "x"


class Y:
    def eval(self, x, y):
        return y

    def __str__(self):
        return "y"


class SinPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "sin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.sin(math.pi * self.arg.eval(x, y))


class CosPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "cos(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.cos(math.pi * self.arg.eval(x, y))


class Times:
    def __init__(self, prob):
        self.lhs = buildExpr(prob * prob)
        self.rhs = buildExpr(prob * prob)

    def __str__(self):
        return str(self.lhs) + "*" + str(self.rhs)

    def eval(self, x, y):
        return self.lhs.eval(x, y) * self.rhs.eval(x, y)


def buildExpr(prob=0.99):
    if random.random() < prob:
        return random.choice([SinPi, CosPi, Times])(prob)
    else:
        return random.choice([X, Y])()


def plotIntensity(exp, width, height):
    canvas = Image.new("L", (width, height))

    for py in range(height):
        for px in range(width):
            # Convert pixel location to [-1,1] coordinates
            x = float(px - width) / width
            y = -float(py - height) / height
            z = exp.eval(x, y)

            # Scale [-1,1] result to [0,255].
            intensity = int(z * 127.5 + 127.5)
            canvas.putpixel((px, py), intensity)

    return canvas


def plotColor(redExp, greenExp, blueExp, width, height):
    redPlane = plotIntensity(redExp, width, height)
    greenPlane = plotIntensity(greenExp, width, height)
    bluePlane = plotIntensity(blueExp, width, height)
    image = Image.merge("RGB", (redPlane, greenPlane, bluePlane))
    return image.convert("RGBA")


def makeImage(numPics=20):
    with open("eqns.txt", 'w') as eqnsFile:
        for i in range(numPics):
            redExp = buildExpr()
            greenExp = buildExpr()
            blueExp = buildExpr()

            eqnsFile.write("img" + str(i) + ":\n")
            eqnsFile.write("red = " + str(redExp) + "\n")
            eqnsFile.write("green = " + str(greenExp) + "\n")
            eqnsFile.write("blue = " + str(blueExp) + "\n\n")

            image = plotColor(redExp, greenExp, blueExp)
            image.save("img" + str(i) + ".png", "PNG")


def gen_randomart(width, height):
    redExp = buildExpr()
    greenExp = buildExpr()
    blueExp = buildExpr()
    alphaExp = buildExpr()
    image = plotColor(redExp, greenExp, blueExp, width, height)
    return image


def test():
    image = gen_randomart(250, 500)
    image.show()
    print(image.size)
