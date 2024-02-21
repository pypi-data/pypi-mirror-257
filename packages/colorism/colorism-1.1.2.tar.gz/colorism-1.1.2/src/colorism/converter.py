import math

from .color import Color


class Converter(Color):
    def __init__(self):
        super().__init__()
        
    def rgb2hex(self, r: int, g: int, b: int) -> str:
        return '#%02x%02x%02x' % (r, g, b)
    
    def rgb2hsl(self, r: int, g: int, b: int) -> tuple[int, int, int]:
        r /= 255
        g /= 255
        b /= 255

        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        if delta == 0:
            h = 0
        elif cmax == r:
            h = ((g - b) / delta) % 6
        elif cmax == g:
            h = ((b - r) / delta) + 2
        elif cmax == b:
            h = ((r - g) / delta) + 4

        h = round(h * 60)

        if h < 0:
            h += 360

        l = (cmax + cmin) / 2

        if delta == 0:
            s = 0
        else:
            s = delta / (1 - abs(2 * l - 1))

        s = round(s * 100)
        l = math.floor(l * 100)

        return h, s, l

    def rgb2hsv(self, r: int, g: int, b: int) -> tuple[float, float, float]:
        r /= 255
        g /= 255
        b /= 255

        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        if delta == 0:
            h = 0
        elif cmax == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif cmax == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        elif cmax == b:
            h = (60 * ((r - g) / delta) + 240) % 360

        if cmax == 0:
            s = 0
        else:
            s = (delta / cmax) * 100

        v = cmax * 100

        return tuple(round(x, 1) for x in (h, s, v))

    def rgb2num(self, r: int, g: int, b: int) -> int:
        return (r << 16) + (g << 8) + b
 
    
    def hex2rgb(self, hex: str) -> tuple[int, int, int]:
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

    def hex2hsl(self, hex: str) -> tuple[int, int, int]:
        r, g, b = self.hex2rgb(hex)
        return self.rgb2hsl(r, g, b)

    def hex2hsv(self, hex: str) -> tuple[float, float, float]:
        r, g, b = self.hex2rgb(hex)
        return self.rgb2hsv(r, g, b)

    def hex2num(self, hex: str) -> int:
        return int(hex.lstrip('#'), 16)


    def hsl2rgb(self, h: int, s: int, l: int) -> tuple[int, int, int]:
        h /= 360
        s /= 100
        l /= 100

        if s == 0:
            return tuple(round(l * 255) for _ in range(3))

        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2

        if 0 <= h < 60:
            rgb = (c, x, 0)
        elif 60 <= h < 120:
            rgb = (x, c, 0)
        elif 120 <= h < 180:
            rgb = (0, c, x)
        elif 180 <= h < 240:
            rgb = (0, x, c)
        elif 240 <= h < 300:
            rgb = (x, 0, c)
        else:
            rgb = (c, 0, x)

        return tuple(round((val + m) * 255) for val in rgb)

    def hsl2hex(self, h: int, s: int, l: int) -> str:
        rgb = self.hsl2rgb(h, s, l)
        return self.rgb2hex(*rgb)

    def hsl2hsv(self, h: int, s: int, l: int) -> tuple[float, float, float]:
        rgb = self.hsl2rgb(h, s, l)
        return self.rgb2hsv(*rgb)

    def hsl2num(self, h: int, s: int, l: int) -> int:
        rgb = self.hsl2rgb(h, s, l)
        return self.rgb2num(*rgb)


    def hsv2rgb(self, h: float, s: float, v: float) -> tuple[int, int, int]:
        h /= 60
        s /= 100
        v /= 100

        c = v * s
        x = c * (1 - abs((h % 2) - 1))
        m = v - c

        if 0 <= h < 1:
            rgb = (c, x, 0)
        elif 1 <= h < 2:
            rgb = (x, c, 0)
        elif 2 <= h < 3:
            rgb = (0, c, x)
        elif 3 <= h < 4:
            rgb = (0, x, c)
        elif 4 <= h < 5:
            rgb = (x, 0, c)
        else:
            rgb = (c, 0, x)

        return tuple(round((val + m) * 255) for val in rgb)

    def hsv2hex(self, h: float, s: float, v: float) -> str:
        rgb = self.hsv2rgb(h, s, v)
        return self.rgb2hex(*rgb)

    def hsv2hsl(self, h: float, s: float, v: float) -> tuple[int, int, int]:
        rgb = self.hsv2rgb(h, s, v)
        return self.rgb2hsl(*rgb)

    def hsv2num(self, h: float, s: float, v: float) -> int:
        rgb = self.hsv2rgb(h, s, v)
        return self.rgb2num(*rgb)


    def num2rgb(self, num: int) -> tuple[int, int, int]:
        return (num >> 16, (num >> 8) & 0xFF, num & 0xFF)

    def num2hex(self, num: int) -> str:
        return '#{0:06x}'.format(num)

    def num2hsl(self, num: int) -> tuple[int, int, int]:
        rgb = self.num2rgb(num)
        return self.rgb2hsl(*rgb)

    def num2hsv(self, num: int) -> tuple[int, int, int]:
        rgb = self.num2rgb(num)
        return self.rgb2hsv(*rgb)
   
