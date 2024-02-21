from colorism import Converter
import colorsys

if __name__ == '__main__':
    C = Converter()
    
    print(f"{'#'*40} RGB - HEX {'#'*40}")
    print(C.rgb2hex(255, 255, 255), C.num2rgb(C.rgb2num(255, 255, 255)))
    print(C.rgb2hex(135,255,215), C.num2rgb(C.rgb2num(135,255,215)))
    print(C.rgb2hex(95,255,215), C.num2rgb(C.rgb2num(95,255,215)))
    print(C.rgb2hex(95,215,175), C.num2rgb(C.rgb2num(95,215,175)))
    print(C.rgb2hex(0,0,215), C.num2rgb(C.rgb2num(0,0,215)))
    print(C.rgb2hex(0,0,175), C.num2rgb(C.rgb2num(0,0,175)))
    print(C.rgb2hex(95,0,255), C.num2rgb(C.rgb2num(95,0,255)))
    print(C.rgb2hex(95,175,135), C.num2rgb(C.rgb2num(95,175,135)))
    
    print(f"{'#'*40} RGB - NUM {'#'*40}")
    print(C.rgb2num(255, 255, 255))
    print(C.rgb2num(135,255,215))
    print(C.rgb2num(95,255,215))
    print(C.rgb2num(95,215,175))
    print(C.rgb2num(0,0,215))
    print(C.rgb2num(0,0,175))
    print(C.rgb2num(95,0,255))
    print(C.rgb2num(95,175,135))
    
    print(f"{'#'*40} RGB - HSL {'#'*40}")
    print(C.rgb2hsl(255, 255, 255), colorsys.rgb_to_hls(255, 255, 255))
    print(C.rgb2hsl(135,255,215), colorsys.rgb_to_hls(135,255,215))
    print(C.rgb2hsl(95,255,215), colorsys.rgb_to_hls(95,255,215))
    print(C.rgb2hsl(95,215,175), colorsys.rgb_to_hls(95,215,175))
    print(C.rgb2hsl(0,0,215), colorsys.rgb_to_hls(0,0,215))
    print(C.rgb2hsl(0,0,175), colorsys.rgb_to_hls(0,0,175))
    print(C.rgb2hsl(95,0,255), colorsys.rgb_to_hls(95,0,255))
    print(C.rgb2hsl(95,175,135), colorsys.rgb_to_hls(95,175,135))
    
    print(f"{'#'*40} RGB - HSV {'#'*40}")
    print(C.rgb2hsv(255, 255, 255), colorsys.rgb_to_hsv(255, 255, 255))
    print(C.rgb2hsv(135,255,215), colorsys.rgb_to_hsv(135,255,215))
    print(C.rgb2hsv(95,255,215), colorsys.rgb_to_hsv(95,255,215))
    print(C.rgb2hsv(95,215,175), colorsys.rgb_to_hsv(95,215,175))
    print(C.rgb2hsv(0,0,215), colorsys.rgb_to_hsv(0,0,215))
    print(C.rgb2hsv(0,0,175), colorsys.rgb_to_hsv(0,0,175))
    print(C.rgb2hsv(95,0,255), colorsys.rgb_to_hsv(95,0,255))
    print(C.rgb2hsv(95,175,135), colorsys.rgb_to_hsv(95,175,135))
    
    print(f"{'#'*40} 2 NUM {'#'*40}")
    print(C.rgb2num(95,175,135), C.hex2num("#5faf87"))
    print(C.rgb2num(95,0,255), C.hex2num("#5f00ff"))
    print(C.rgb2num(0,0,175), C.hex2num("#0000af"))
    print(C.rgb2num(0,0,215), C.hex2num("#0000d7"))
    print(C.rgb2num(95,215,175), C.hex2num("#5fd7af"))
    print(C.rgb2num(95,255,215), C.hex2num("#5fffd7"))
    print(C.rgb2num(135,255,215), C.hex2num("#87ffd7"))
    print(C.rgb2num(255, 255, 255), C.hex2num("#ffffff"))
    
    print(C.color(45))
 