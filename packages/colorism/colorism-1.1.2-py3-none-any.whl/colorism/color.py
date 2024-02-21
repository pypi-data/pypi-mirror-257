import re

class Color():
    BLACK, Grey31        		= 0, 16                # #000000 rgb(0,0,0) hsl(0,0%,0%)
    BLUE                 		= 4                    # #000080 rgb(0,0,128) hsl(240,100%,25%)
    CYAN                 		= 6                    # #008080 rgb(0,128,128) hsl(180,100%,25%)
    GREEN                		= 2                    # #008000 rgb(0,128,0) hsl(120,100%,25%)
    MAGENTA              		= 5                    # #800080 rgb(128,0,128) hsl(300,100%,25%)
    RED                  		= 1                    # #800000 rgb(128,0,0) hsl(0,100%,25%)
    YELLOW               		= 3                    # #808000 rgb(128,128,0) hsl(60,100%,25%)
    WHITE                		= 7                    # #c0c0c0 rgb(192,192,192) hsl(0,0%,75%)
    
    LIGHTBLACK, Grey12    		= 8, 244               # #808080 rgb(128,128,128) hsl(0,0%,50%)
    LIGHTBLUE, Blue     		= 12, 21               # #0000ff rgb(0,0,255) hsl(240,100%,50%)
    LIGHTCYAN, Cyan     		= 14, 51               # #00ffff rgb(0,255,255) hsl(180,100%,50%)
    LIGHTGREEN, Green   		= 10, 46               # #00ff00 rgb(0,255,0) hsl(120,100%,50%)
    LIGHTMAGENTA, Magenta 		= 13, 201              # #ff00ff rgb(255,0,255) hsl(300,100%,50%)
    LIGHTRED, Red       		= 9, 196               # #ff0000 rgb(255,0,0) hsl(0,100%,50%)
    LIGHTYELLOW, Yellow 		= 11, 226              # #ffff00 rgb(255,255,0) hsl(60,100%,50%)
    LIGHTWHITE, Grey25   		= 15, 231              # #ffffff rgb(255,255,255) hsl(0,0%,100%)

    Aquamarine          		= 122                  # #87ffd7 rgb(135,255,215) hsl(160,100%,76%)
    Aquamarine2          		= 86                   # #5fffd7 rgb(95,255,215) hsl(165,100%,68%)
    Aquamarine3          		= 79                   # #5fd7af rgb(95,215,175) hsl(160,60%,60%)
    Blue2                		= 20                   # #0000d7 rgb(0,0,215) hsl(240,100%,42%)
    Blue3                		= 19                   # #0000af rgb(0,0,175) hsl(240,100%,34%)
    BlueViolet           		= 57                   # #5f00ff rgb(95,0,255) hsl(62,100%,50%)
    CadetBlue            		= 73                   # #5fafaf rgb(95,175,175) hsl(180,33%,52%)
    CadetBlue2            		= 72                   # #5faf87 rgb(95,175,135) hsl(150,33%,52%)
    Chartreuse          		= 118                  # #87ff00 rgb(135,255,0) hsl(8,100%,50%)
    Chartreuse2          		= 112                  # #87d700 rgb(135,215,0) hsl(2,100%,42%)
    Chartreuse3          		= 82                   # #5fff00 rgb(95,255,0) hsl(7,100%,50%)
    Chartreuse4          		= 76                   # #5fd700 rgb(95,215,0) hsl(3,100%,42%)
    Chartreuse5          		= 70                   # #5faf00 rgb(95,175,0) hsl(7,100%,34%)
    Chartreuse6          		= 64                   # #5f8700 rgb(95,135,0) hsl(7,100%,26%)
    CornflowerBlue       		= 69                   # #5f87ff rgb(95,135,255) hsl(225,100%,68%)
    Cornsilk            		= 230                  # #ffffd7 rgb(255,255,215) hsl(60,100%,92%)
    Cyan2                		= 50                   # #00ffd7 rgb(0,255,215) hsl(70,100%,50%)
    Cyan3                		= 43                   # #00d7af rgb(0,215,175) hsl(68,100%,42%)
    DarkBlue             		= 18                   # #000087 rgb(0,0,135) hsl(240,100%,26%)
    DarkCyan             		= 36                   # #00af87 rgb(0,175,135) hsl(66,100%,34%)
    DarkGoldenrod        		= 136                  # #af8700 rgb(175,135,0) hsl(6,100%,34%)
    DarkGreen            		= 22                   # #005f00 rgb(0,95,0) hsl(120,100%,18%)
    DarkKhaki            		= 143                  # #afaf5f rgb(175,175,95) hsl(60,33%,52%)
    DarkMagenta          		= 91                   # #8700af rgb(135,0,175) hsl(86,100%,34%)
    DarkMagenta2          		= 90                   # #870087 rgb(135,0,135) hsl(300,100%,26%)
    DarkOliveGreen      		= 192                  # #d7ff87 rgb(215,255,135) hsl(80,100%,76%)
    DarkOliveGreen2      		= 191                  # #d7ff5f rgb(215,255,95) hsl(75,100%,68%)
    DarkOliveGreen3      		= 155                  # #afff5f rgb(175,255,95) hsl(90,100%,68%)
    DarkOliveGreen4      		= 149                  # #afd75f rgb(175,215,95) hsl(80,60%,60%)
    DarkOliveGreen5      		= 113                  # #87d75f rgb(135,215,95) hsl(100,60%,60%)
    DarkOliveGreen6      		= 107                  # #87af5f rgb(135,175,95) hsl(90,33%,52%)
    DarkOrange           		= 208                  # #ff8700 rgb(255,135,0) hsl(1,100%,50%)
    DarkOrange2          		= 166                  # #d75f00 rgb(215,95,0) hsl(6,100%,42%)
    DarkOrange3          		= 130                  # #af5f00 rgb(175,95,0) hsl(2,100%,34%)
    DarkRed              		= 88                   # #870000 rgb(135,0,0) hsl(0,100%,26%)
    DarkRed2              		= 52                   # #5f0000 rgb(95,0,0) hsl(0,100%,18%)
    DarkSeaGreen        		= 193                  # #d7ffaf rgb(215,255,175) hsl(90,100%,84%)
    DarkSeaGreen2        		= 158                  # #afffd7 rgb(175,255,215) hsl(150,100%,84%)
    DarkSeaGreen3        		= 157                  # #afffaf rgb(175,255,175) hsl(120,100%,84%)
    DarkSeaGreen4        		= 151                  # #afd7af rgb(175,215,175) hsl(120,33%,76%)
    DarkSeaGreen5        		= 150                  # #afd787 rgb(175,215,135) hsl(90,50%,68%)
    DarkSeaGreen6        		= 115                  # #87d7af rgb(135,215,175) hsl(150,50%,68%)
    DarkSeaGreen7         		= 108                  # #87af87 rgb(135,175,135) hsl(120,20%,60%)
    DarkSeaGreen8        		= 71                   # #5faf5f rgb(95,175,95) hsl(120,33%,52%)
    DarkSeaGreen9        		= 65                   # #5f875f rgb(95,135,95) hsl(120,17%,45%)
    DarkSlateGray       		= 123                  # #87ffff rgb(135,255,255) hsl(180,100%,76%)
    DarkSlateGray2       		= 116                  # #87d7d7 rgb(135,215,215) hsl(180,50%,68%)
    DarkSlateGray3       		= 87                   # #5fffff rgb(95,255,255) hsl(180,100%,68%)
    DarkTurquoise        		= 44                   # #00d7d7 rgb(0,215,215) hsl(180,100%,42%)
    DarkViolet           		= 128                  # #af00d7 rgb(175,0,215) hsl(88,100%,42%)
    DarkViolet2           		= 92                   # #8700d7 rgb(135,0,215) hsl(77,100%,42%)
    DeepPink            		= 199                  # #ff00af rgb(255,0,175) hsl(18,100%,50%)
    DeepPink2            		= 198                  # #ff0087 rgb(255,0,135) hsl(28,100%,50%)
    DeepPink3            		= 197                  # #ff005f rgb(255,0,95) hsl(37,100%,50%)
    DeepPink4            		= 162                  # #d70087 rgb(215,0,135) hsl(22,100%,42%)
    DeepPink5            		= 161                  # #d7005f rgb(215,0,95) hsl(33,100%,42%)
    DeepPink6            		= 125                  # #af005f rgb(175,0,95) hsl(27,100%,34%)
    DeepPink7            		= 89                   # #87005f rgb(135,0,95) hsl(17,100%,26%)
    DeepPink8            		= 53                   # #5f005f rgb(95,0,95) hsl(300,100%,18%)
    DeepSkyBlue         		= 39                   # #00afff rgb(0,175,255) hsl(98,100%,50%)
    DeepSkyBlue2         		= 38                   # #00afd7 rgb(0,175,215) hsl(91,100%,42%)
    DeepSkyBlue3         		= 32                   # #0087d7 rgb(0,135,215) hsl(02,100%,42%)
    DeepSkyBlue4         		= 31                   # #0087af rgb(0,135,175) hsl(93,100%,34%)
    DeepSkyBlue5         		= 25                   # #005faf rgb(0,95,175) hsl(07,100%,34%)
    DeepSkyBlue6         		= 24                   # #005f87 rgb(0,95,135) hsl(97,100%,26%)
    DeepSkyBlue7         		= 23                   # #005f5f rgb(0,95,95) hsl(180,100%,18%)
    DodgerBlue          		= 33                   # #0087ff rgb(0,135,255) hsl(08,100%,50%)
    DodgerBlue2          		= 27                   # #005fff rgb(0,95,255) hsl(17,100%,50%)
    DodgerBlue3          		= 26                   # #005fd7 rgb(0,95,215) hsl(13,100%,42%)
    Gold                		= 220                  # #ffd700 rgb(255,215,0) hsl(0,100%,50%)
    Gold2                		= 178                  # #d7af00 rgb(215,175,0) hsl(8,100%,42%)
    Gold3                		= 142                  # #afaf00 rgb(175,175,0) hsl(60,100%,34%)
    Green2               		= 40                   # #00d700 rgb(0,215,0) hsl(120,100%,42%)
    Green3               		= 34                   # #00af00 rgb(0,175,0) hsl(120,100%,34%)
    Green4               		= 28                   # #008700 rgb(0,135,0) hsl(120,100%,26%)
    GreenYellow          		= 154                  # #afff00 rgb(175,255,0) hsl(8,100%,50%)
    Grey                		= 255                  # #eeeeee rgb(238,238,238) hsl(0,0%,93%)
    Grey2                		= 254                  # #e4e4e4 rgb(228,228,228) hsl(0,0%,89%)
    Grey3                		= 253                  # #dadada rgb(218,218,218) hsl(0,0%,85%)
    Grey4                		= 252                  # #d0d0d0 rgb(208,208,208) hsl(0,0%,81%)
    Grey5                		= 251                  # #c6c6c6 rgb(198,198,198) hsl(0,0%,77%)
    Grey6                		= 250                  # #bcbcbc rgb(188,188,188) hsl(0,0%,73%)
    Grey7                		= 249                  # #b2b2b2 rgb(178,178,178) hsl(0,0%,69%)
    Grey8                		= 248                  # #a8a8a8 rgb(168,168,168) hsl(0,0%,65%)
    Grey9                		= 247                  # #9e9e9e rgb(158,158,158) hsl(0,0%,61%)
    Grey10               		= 246                  # #949494 rgb(148,148,148) hsl(0,0%,58%)
    Grey11               		= 245                  # #8a8a8a rgb(138,138,138) hsl(0,0%,54%)
    Grey13               		= 243                  # #767676 rgb(118,118,118) hsl(0,0%,46%)
    Grey14               		= 242                  # #6c6c6c rgb(108,108,108) hsl(0,0%,40%)
    Grey15               		= 241                  # #626262 rgb(98,98,98) hsl(0,0%,37%)
    Grey16               		= 240                  # #585858 rgb(88,88,88) hsl(0,0%,34%)
    Grey17               		= 239                  # #4e4e4e rgb(78,78,78) hsl(0,0%,30%)
    Grey18               		= 238                  # #444444 rgb(68,68,68) hsl(0,0%,26%)
    Grey19               		= 237                  # #3a3a3a rgb(58,58,58) hsl(0,0%,22%)
    Grey20               		= 236                  # #303030 rgb(48,48,48) hsl(0,0%,18%)
    Grey21               		= 235                  # #262626 rgb(38,38,38) hsl(0,0%,14%)
    Grey22               		= 234                  # #1c1c1c rgb(28,28,28) hsl(0,0%,10%)
    Grey23               		= 233                  # #121212 rgb(18,18,18) hsl(0,0%,7%)
    Grey24               		= 232                  # #080808 rgb(8,8,8) hsl(0,0%,3%)
    Grey26               		= 188                  # #d7d7d7 rgb(215,215,215) hsl(0,0%,84%)
    Grey27               		= 145                  # #afafaf rgb(175,175,175) hsl(0,0%,68%)
    Grey28               		= 139                  # #af87af rgb(175,135,175) hsl(300,20%,60%)
    Grey29               		= 102                  # #878787 rgb(135,135,135) hsl(0,0%,52%)
    Grey30               		= 59                   # #5f5f5f rgb(95,95,95) hsl(0,0%,37%)
    Honeydew            		= 194                  # #d7ffd7 rgb(215,255,215) hsl(120,100%,92%)
    HotPink              		= 206                  # #ff5fd7 rgb(255,95,215) hsl(315,100%,68%)
    HotPink2              		= 205                  # #ff5faf rgb(255,95,175) hsl(330,100%,68%)
    HotPink3             		= 169                  # #d75faf rgb(215,95,175) hsl(320,60%,60%)
    HotPink4             		= 168                  # #d75f87 rgb(215,95,135) hsl(340,60%,60%)
    HotPink5             		= 132                  # #af5f87 rgb(175,95,135) hsl(330,33%,52%)
    IndianRed           		= 204                  # #ff5f87 rgb(255,95,135) hsl(345,100%,68%)
    IndianRed2           		= 203                  # #ff5f5f rgb(255,95,95) hsl(0,100%,68%)
    IndianRed3            		= 167                  # #d75f5f rgb(215,95,95) hsl(0,60%,60%)
    IndianRed4            		= 131                  # #af5f5f rgb(175,95,95) hsl(0,33%,52%)
    Khaki               		= 228                  # #ffff87 rgb(255,255,135) hsl(60,100%,76%)
    Khaki2               		= 185                  # #d7d75f rgb(215,215,95) hsl(60,60%,60%)
    LightCoral           		= 210                  # #ff8787 rgb(255,135,135) hsl(0,100%,76%)
    LightCyan           		= 195                  # #d7ffff rgb(215,255,255) hsl(180,100%,92%)
    LightCyan2           		= 152                  # #afd7d7 rgb(175,215,215) hsl(180,33%,76%)
    LightGoldenrod      		= 227                  # #ffff5f rgb(255,255,95) hsl(60,100%,68%)
    LightGoldenrod2      		= 222                  # #ffd787 rgb(255,215,135) hsl(40,100%,76%)
    LightGoldenrod3      		= 221                  # #ffd75f rgb(255,215,95) hsl(45,100%,68%)
    LightGoldenrod4      		= 186                  # #d7d787 rgb(215,215,135) hsl(60,50%,68%)
    LightGoldenrod5      		= 179                  # #d7af5f rgb(215,175,95) hsl(40,60%,60%)
    LightGreen           		= 120                  # #87ff87 rgb(135,255,135) hsl(120,100%,76%)
    LightGreen2           		= 119                  # #87ff5f rgb(135,255,95) hsl(105,100%,68%)
    LightPink           		= 217                  # #ffafaf rgb(255,175,175) hsl(0,100%,84%)
    LightPink2           		= 174                  # #d78787 rgb(215,135,135) hsl(0,50%,68%)
    LightPink3           		= 95                   # #875f5f rgb(135,95,95) hsl(0,17%,45%)
    LightSalmon         		= 216                  # #ffaf87 rgb(255,175,135) hsl(20,100%,76%)
    LightSalmon2         		= 173                  # #d7875f rgb(215,135,95) hsl(20,60%,60%)
    LightSalmon3         		= 137                  # #af875f rgb(175,135,95) hsl(30,33%,52%)
    LightSeaGreen        		= 37                   # #00afaf rgb(0,175,175) hsl(180,100%,34%)
    LightSkyBlue        		= 153                  # #afd7ff rgb(175,215,255) hsl(210,100%,84%)
    LightSkyBlue2        		= 110                  # #87afd7 rgb(135,175,215) hsl(210,50%,68%)
    LightSkyBlue3        		= 109                  # #87afaf rgb(135,175,175) hsl(180,20%,60%)
    LightSlateBlue       		= 105                  # #8787ff rgb(135,135,255) hsl(240,100%,76%)
    LightSlateGrey       		= 103                  # #8787af rgb(135,135,175) hsl(240,20%,60%)
    LightSteelBlue      		= 189                  # #d7d7ff rgb(215,215,255) hsl(240,100%,92%)
    LightSteelBlue2       		= 147                  # #afafff rgb(175,175,255) hsl(240,100%,84%)
    LightSteelBlue3      		= 146                  # #afafd7 rgb(175,175,215) hsl(240,33%,76%)
    LightYellow         		= 187                  # #d7d7af rgb(215,215,175) hsl(60,33%,76%)
    Magenta2             		= 200                  # #ff00d7 rgb(255,0,215) hsl(09,100%,50%)
    Magenta3             		= 165                  # #d700ff rgb(215,0,255) hsl(90,100%,50%)
    Magenta4             		= 164                  # #d700d7 rgb(215,0,215) hsl(300,100%,42%)
    Magenta5             		= 163                  # #d700af rgb(215,0,175) hsl(11,100%,42%)
    Magenta6             		= 127                  # #af00af rgb(175,0,175) hsl(300,100%,34%)
    MediumOrchid        		= 207                  # #ff5fff rgb(255,95,255) hsl(300,100%,68%)
    MediumOrchid2        		= 171                  # #d75fff rgb(215,95,255) hsl(285,100%,68%)
    MediumOrchid3         		= 134                  # #af5fd7 rgb(175,95,215) hsl(280,60%,60%)
    MediumOrchid4        		= 133                  # #af5faf rgb(175,95,175) hsl(300,33%,52%)
    MediumPurple        		= 141                  # #af87ff rgb(175,135,255) hsl(260,100%,76%)
    MediumPurple2        		= 140                  # #af87d7 rgb(175,135,215) hsl(270,50%,68%)
    MediumPurple3        		= 135                  # #af5fff rgb(175,95,255) hsl(270,100%,68%)
    MediumPurple4         		= 104                  # #8787d7 rgb(135,135,215) hsl(240,50%,68%)
    MediumPurple5        		= 98                   # #875fd7 rgb(135,95,215) hsl(260,60%,60%)
    MediumPurple6        		= 97                   # #875faf rgb(135,95,175) hsl(270,33%,52%)
    MediumPurple7        		= 60                   # #5f5f87 rgb(95,95,135) hsl(240,17%,45%)
    MediumSpringGreen    		= 49                   # #00ffaf rgb(0,255,175) hsl(61,100%,50%)
    MediumTurquoise      		= 80                   # #5fd7d7 rgb(95,215,215) hsl(180,60%,60%)
    MediumVioletRed      		= 126                  # #af0087 rgb(175,0,135) hsl(13,100%,34%)
    MistyRose           		= 224                  # #ffd7d7 rgb(255,215,215) hsl(0,100%,92%)
    MistyRose2           		= 181                  # #d7afaf rgb(215,175,175) hsl(0,33%,76%)
    NavajoWhite         		= 223                  # #ffd7af rgb(255,215,175) hsl(30,100%,84%)
    NavajoWhite2         		= 144                  # #afaf87 rgb(175,175,135) hsl(60,20%,60%)
    NavyBlue             		= 17                   # #00005f rgb(0,0,95) hsl(240,100%,18%)
    Orange              		= 214                  # #ffaf00 rgb(255,175,0) hsl(1,100%,50%)
    Orange2              		= 172                  # #d78700 rgb(215,135,0) hsl(7,100%,42%)
    Orange3              		= 94                   # #875f00 rgb(135,95,0) hsl(2,100%,26%)
    Orange4              		= 58                   # #5f5f00 rgb(95,95,0) hsl(60,100%,18%)
    OrangeRed           		= 202                  # #ff5f00 rgb(255,95,0) hsl(2,100%,50%)
    Orchid              		= 213                  # #ff87ff rgb(255,135,255) hsl(300,100%,76%)
    Orchid2              		= 212                  # #ff87d7 rgb(255,135,215) hsl(320,100%,76%)
    Orchid3               		= 170                  # #d75fd7 rgb(215,95,215) hsl(300,60%,60%)
    PaleGreen           		= 156                  # #afff87 rgb(175,255,135) hsl(100,100%,76%)
    PaleGreen2           		= 121                  # #87ffaf rgb(135,255,175) hsl(140,100%,76%)
    PaleGreen3           		= 114                  # #87d787 rgb(135,215,135) hsl(120,50%,68%)
    PaleGreen4           		= 77                   # #5fd75f rgb(95,215,95) hsl(120,60%,60%)
    PaleTurquoise       		= 159                  # #afffff rgb(175,255,255) hsl(180,100%,84%)
    PaleTurquoise2       		= 66                   # #5f8787 rgb(95,135,135) hsl(180,17%,45%)
    PaleVioletRed       		= 211                  # #ff87af rgb(255,135,175) hsl(340,100%,76%)
    Pink                		= 218                  # #ffafd7 rgb(255,175,215) hsl(330,100%,84%)
    Pink2                		= 175                  # #d787af rgb(215,135,175) hsl(330,50%,68%)
    Plum                		= 219                  # #ffafff rgb(255,175,255) hsl(300,100%,84%)
    Plum2                		= 183                  # #d7afff rgb(215,175,255) hsl(270,100%,84%)
    Plum3                		= 176                  # #d787d7 rgb(215,135,215) hsl(300,50%,68%)
    Plum4                		= 96                   # #875f87 rgb(135,95,135) hsl(300,17%,45%)
    Purple               		= 129                  # #af00ff rgb(175,0,255) hsl(81,100%,50%)
    Purple2               		= 93                   # #8700ff rgb(135,0,255) hsl(71,100%,50%)
    Purple3              		= 56                   # #5f00d7 rgb(95,0,215) hsl(66,100%,42%)
    Purple4              		= 55                   # #5f00af rgb(95,0,175) hsl(72,100%,34%)
    Purple5              		= 54                   # #5f0087 rgb(95,0,135) hsl(82,100%,26%)
    Red2                 		= 160                  # #d70000 rgb(215,0,0) hsl(0,100%,42%)
    Red3                 		= 124                  # #af0000 rgb(175,0,0) hsl(0,100%,34%)
    RosyBrown            		= 138                  # #af8787 rgb(175,135,135) hsl(0,20%,60%)
    RoyalBlue           		= 63                   # #5f5fff rgb(95,95,255) hsl(240,100%,68%)
    Salmon              		= 209                  # #ff875f rgb(255,135,95) hsl(15,100%,68%)
    SandyBrown           		= 215                  # #ffaf5f rgb(255,175,95) hsl(30,100%,68%)
    SeaGreen            		= 85                   # #5fffaf rgb(95,255,175) hsl(150,100%,68%)
    SeaGreen2            		= 84                   # #5fff87 rgb(95,255,135) hsl(135,100%,68%)
    SeaGreen3            		= 83                   # #5fff5f rgb(95,255,95) hsl(120,100%,68%)
    SeaGreen4            		= 78                   # #5fd787 rgb(95,215,135) hsl(140,60%,60%)
    SkyBlue             		= 117                  # #87d7ff rgb(135,215,255) hsl(200,100%,76%)
    SkyBlue2             		= 111                  # #87afff rgb(135,175,255) hsl(220,100%,76%)
    SkyBlue3             		= 74                   # #5fafd7 rgb(95,175,215) hsl(200,60%,60%)
    SlateBlue           		= 99                   # #875fff rgb(135,95,255) hsl(255,100%,68%)
    SlateBlue2           		= 62                   # #5f5fd7 rgb(95,95,215) hsl(240,60%,60%)
    SlateBlue3           		= 61                   # #5f5faf rgb(95,95,175) hsl(240,33%,52%)
    SpringGreen         		= 48                   # #00ff87 rgb(0,255,135) hsl(51,100%,50%)
    SpringGreen2         		= 47                   # #00ff5f rgb(0,255,95) hsl(42,100%,50%)
    SpringGreen3         		= 42                   # #00d787 rgb(0,215,135) hsl(57,100%,42%)
    SpringGreen4         		= 41                   # #00d75f rgb(0,215,95) hsl(46,100%,42%)
    SpringGreen5         		= 35                   # #00af5f rgb(0,175,95) hsl(52,100%,34%)
    SpringGreen6         		= 29                   # #00875f rgb(0,135,95) hsl(62,100%,26%)
    SteelBlue           		= 81                   # #5fd7ff rgb(95,215,255) hsl(195,100%,68%)
    SteelBlue2           		= 75                   # #5fafff rgb(95,175,255) hsl(210,100%,68%)
    SteelBlue3           		= 68                   # #5f87d7 rgb(95,135,215) hsl(220,60%,60%)
    SteelBlue4            		= 67                   # #5f87af rgb(95,135,175) hsl(210,33%,52%)
    Tan                  		= 180                  # #d7af87 rgb(215,175,135) hsl(30,50%,68%)
    Thistle             		= 225                  # #ffd7ff rgb(255,215,255) hsl(300,100%,92%)
    Thistle2             		= 182                  # #d7afd7 rgb(215,175,215) hsl(300,33%,76%)
    Turquoise           		= 45                   # #00d7ff rgb(0,215,255) hsl(89,100%,50%)
    Turquoise2           		= 30                   # #008787 rgb(0,135,135) hsl(180,100%,26%)
    Violet               		= 177                  # #d787ff rgb(215,135,255) hsl(280,100%,76%)
    Wheat               		= 229                  # #ffffaf rgb(255,255,175) hsl(60,100%,84%)
    Wheat2               		= 101                  # #87875f rgb(135,135,95) hsl(60,17%,45%)
    Yellow2              		= 190                  # #d7ff00 rgb(215,255,0) hsl(9,100%,50%)
    Yellow3              		= 184                  # #d7d700 rgb(215,215,0) hsl(60,100%,42%)
    Yellow4              		= 148                  # #afd700 rgb(175,215,0) hsl(1,100%,42%)
    Yellow5              		= 106                  # #87af00 rgb(135,175,0) hsl(3,100%,34%)
    Yellow6              		= 100                  # #878700 rgb(135,135,0) hsl(60,100%,26%)
        
    def __init__(self) -> None:
        pass

    def color(self, num: int) -> str:
        attributes = vars(Color).get(num, None)
        if attributes is None:
            raise ValueError(f"Invalid color number: {num}. Number must be between 0 and 255.")
        return attributes

class TextStyle(Color):
    def __init__(self, escape8b: str, escape24b:str, reset: str) -> None:
        super().__init__()
        self.escape8 = escape8b
        self.escape24 = escape24b
        self.reset = reset
        
        for name in dir(Color):
            if not name.startswith('_') and "RESET" not in name:
                value = getattr(self, name)
                if not callable(value):
                    setattr(self, name, self.to_ansi_8(value))
    
    @property
    def _palette(self) -> None:
        matrix = [
            [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
            52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
            88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99],

            [124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135,
            160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
            196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207],

            [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
            64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75,
            100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111],

            [136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147,
            172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183,
            208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219],

            [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
            76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87,
            112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123],

            [148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
            184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195,
            220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231]
        ]
        
        print(f"{'-' * 25} Palette {'-' * 25}\n")

        print(f"Standard:{'':<4}", end="")
        for i in range(8):
            print(f"{self.to_ansi_8(i)} {i:3} {self.reset}", end="")
        print()

        print(f"Intense:{'':<5}", end="")
        for i in range(8, 16):
            print(f"{self.to_ansi_8(i)} {i:3} {self.reset}", end="")
        print()

        for row in matrix:
            for i, num in enumerate(row):
                if i % 12 == 0:
                    print()
                print(f"{self.to_ansi_8(num)} {num:3} {self.reset}", end="")
        print("\n")

        print("Grayscale:")
        for i in range(232, 256, 12):
            for j in range(i, i + 12):
                print(f"{self.to_ansi_8(j)} {j:3} {self.reset}", end="")
            print()
        print("\n")
        
    @property
    def _rainbow_palette(self) -> None:
        matrix = [
            [16, 52, 88, 124, 160, 196, 203, 210, 217, 224, 231],
            [16, 52, 88, 124, 160, 202, 209, 216, 223, 230, 231],
            [16, 52, 88, 124, 166, 208, 215, 222, 229, 230, 231],
            [16, 52, 88, 130, 172, 214, 221, 228, 229, 230, 231],
            [16, 52, 94, 136, 178, 220, 227, 228, 229, 230, 231],
            [16, 58, 100, 142, 184, 226, 227, 228, 229, 230, 231],
            [16, 22, 64, 106, 148, 190, 227, 228, 229, 230, 231],
            [16, 22, 28, 70, 112, 154, 191, 228, 229, 230, 231],
            [16, 22, 28, 34, 76, 118, 155, 192, 229, 230, 231],
            [16, 22, 28, 34, 40, 82, 119, 156, 193, 230, 231],
            [16, 22, 28, 34, 40, 46, 83, 120, 157, 194, 231],
            [16, 22, 28, 34, 40, 47, 84, 121, 158, 195, 231],
            [16, 22, 28, 34, 41, 48, 85, 122, 159, 195, 231],
            [16, 22, 28, 35, 42, 49, 86, 123, 159, 195, 231],
            [16, 22, 29, 36, 43, 50, 87, 123, 159, 195, 231],
            [16, 23, 30, 37, 44, 51, 87, 123, 159, 195, 231],
            [16, 17, 24, 31, 38, 45, 87, 123, 159, 195, 231],
            [16, 17, 18, 25, 32, 39, 81, 123, 159, 195, 231],
            [16, 17, 18, 19, 26, 33, 75, 117, 159, 195, 231],
            [16, 17, 18, 19, 20, 27, 69, 111, 153, 195, 231],
            [16, 17, 18, 19, 20, 21, 63, 105, 147, 189, 231],
            [16, 17, 18, 19, 20, 57, 99, 141, 183, 225, 231],
            [16, 17, 18, 19, 56, 93, 135, 177, 219, 225, 231],
            [16, 17, 18, 55, 92, 129, 171, 213, 219, 225, 231],
            [16, 17, 54, 91, 128, 165, 207, 213, 219, 225, 231],
            [16, 53, 90, 127, 164, 201, 207, 213, 219, 225, 231],
            [16, 52, 89, 126, 163, 200, 207, 213, 219, 225, 231],
            [16, 52, 88, 125, 162, 199, 206, 213, 219, 225, 231],
            [16, 52, 88, 124, 161, 198, 205, 212, 219, 225, 231]
        ]

        print(f"{'-' * 25} Raimbow Palette {'-' * 25}\n")
        for row in matrix:
            for num in row:
                print(f"{self.to_ansi_8(num)} {num:3} {self.reset}", end="")
            print()
        print()
    
    @property
    def _color_legend(self) -> None:
        print(f"{'-' * 25} 8-Bit Legend {'-' * 25}\n")
        for attribute, value in self.__dict__.items():
            num = re.match(fr'{re.escape(self.escape8)}(\d+)m', value)
            if not num:
                continue
            num = num.group(1)
            print(f"- {attribute:<20}{self.to_ansi_8(num)} {num:4}{self.reset:10}")
            print("-" * 30)

    def to_ansi_8(self, value: int) -> str:
        return f"{self.escape8}{value}m"
            
    def to_ansi_24(self, r: int, g: int, b: int) -> str:
        return f"{self.escape24}{r};{g};{b}m"

    def color(self, num: int) -> str:
        assert 0 <= num <= 255, "(color) Invalid color number. Number must be between 0 and 255."
        return super().color(num)
        
    def num2escape(self, value: int) -> str:
        assert 0 <= value <= 255, "(num2escape) Invalid color number. Number must be between 0 and 255."
        
        return self.to_ansi_8(value)
    
    def rgb2escape(self, r: int, g: int, b: int) -> str:
        assert 0 <= r <= 255, "(rgb2escape) Invalid red value. Red must be between 0 and 255."
        assert 0 <= g <= 255, "(rgb2escape) Invalid green value. Green must be between 0 and 255."
        assert 0 <= b <= 255, "(rgb2escape) Invalid blue value. Blue must be between 0 and 255."
        
        return self.to_ansi_24(r, g, b)
    
    def hex2escape(self, value: str) -> str:
        assert value.startswith('#'), "(hex2escape) Invalid hex value. Hex value must start with '#'."
        assert len(value) == 7, "(hex2escape) Invalid hex value. Hex value must be 7 characters long."
        
        hex = value.lstrip('#')

        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)
        return self.rgb2escape(r, g, b)
    
    def hsl2escape(self, h: float, s: float, l: float) -> str:
        assert 0 <= h <= 360, "(hsl2escape) Invalid hue value. Hue must be between 0 and 360."
        assert 0 <= s <= 100, "(hsl2escape) Invalid saturation value. Saturation must be between 0 and 100."
        assert 0 <= l <= 100, "(hsl2escape) Invalid lightness value. Lightness must be between 0 and 100."
        
        h /= 360.0
        s /= 100.0
        l /= 100.0
        
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p

        if s == 0:
            r = g = b = int(l * 255)
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q

            r = int(hue_to_rgb(p, q, h + 1/3) * 255)
            g = int(hue_to_rgb(p, q, h) * 255)
            b = int(hue_to_rgb(p, q, h - 1/3) * 255)

        return self.rgb2escape(r, g, b)

    def hsv2escape(self, h: float, s: float, v: float) -> str:
        assert 0 <= h <= 360, "(hsv2escape) Invalid hue value. Hue must be between 0 and 360."
        assert 0 <= s <= 100, "(hsv2escape) Invalid saturation value. Saturation must be between 0 and 100."
        assert 0 <= v <= 100, "(hsv2escape) Invalid value value. Value must be between 0 and 100."
        
        h /= 360.0
        s /= 100.0
        v /= 100.0

        if s == 0:
            r = g = b = int(v * 255)
        else:
            i = int(h * 6)
            f = (h * 6) - i
            p = v * (1 - s)
            q = v * (1 - f * s)
            t = v * (1 - (1 - f) * s)

            i = i % 6
            rgb_switch = {
                0: (v, t, p),
                1: (q, v, p),
                2: (p, v, t),
                3: (p, q, v),
                4: (t, p, v),
                5: (v, p, q)
            }
            r, g, b = [int(c * 255) for c in rgb_switch[i]]

        return self.rgb2escape(r, g, b)

class Fore(TextStyle):
    __ESCAPE = "\33[38;5;"
    __ESCAPE24BIT = "\33[38;2;"
    RESET, RESET_ALL = "\33[39m", "\33[0m"
    BOLD, BOLD_RST = "\33[1m", "\33[22m"
    DIM, DIM_RST = "\33[2m", "\33[22m"
    ITALIC, ITALIC_RST = "\33[3m", "\33[23m"
    UNDERLINE, UNDERLINE_RST = "\33[4m", "\33[24m"
    BLINK, BLINK_RST = "\33[5m", "\33[25m"
    INVERT, INVERT_RST = "\33[7m", "\33[27m"
    HIDDEN, HIDDEN_RST = "\33[8m", "\33[28m"
    STRIKETHROUGH, STRIKETHROUGH_RST = "\33[9m", "\33[29m"

    def __init__(self):
        super().__init__(self.__ESCAPE, self.__ESCAPE24BIT, self.RESET)
    
    def bold(self, text: str) -> str:
        return self.BOLD + text + self.BOLD_RST

    def dim(self, text: str) -> str:
        return self.DIM + text + self.DIM_RST

    def italic(self, text: str) -> str:
        return self.ITALIC + text + self.ITALIC_RST

    def underline(self, text: str) -> str:
        return self.UNDERLINE + text + self.UNDERLINE_RST

    def blink(self, text: str) -> str:
        return self.BLINK + text + self.BLINK_RST

    def invert(self, text: str) -> str:
        return self.INVERT + text + self.INVERT_RST

    def hidden(self, text: str) -> str:
        return self.HIDDEN + text + self.HIDDEN_RST

    def strikethrough(self, text: str) -> str:
        return self.STRIKETHROUGH + text + self.STRIKETHROUGH_RST

class Back(TextStyle):
    __ESCAPE = "\33[48;5;"
    __ESCAPE24BIT = "\33[48;2;"
    RESET, RESET_ALL = "\33[49m", "\33[0m"
    
    def __init__(self):
        super().__init__(self.__ESCAPE, self.__ESCAPE24BIT, self.RESET)


BG = Back()
FG = Fore()