'''This is a custom layout for the RPi InfoScreen wordclock screen.

    Custom layouts can be created for the screen by creating a new file in the
    "layouts" folder.

    Each layout must have the following variables:
        LAYOUT:   The grid layout. Must be a single string.
        MAP:      The mapping required for various times (see notes below)
        COLS:     The number of columns required for the grid layout
        SIZE:     The size of the individual box containing your letter.
                  Tuple in (x, y) format.
        FONTSIZE: Font size for the letter
'''

# Layout is a single string variable which will be looped over by the parser.
LAYOUT = ("ESKISTLFUNF"
          "ZEHNZWANZIG"
          "DREIVIERTEL"
          "TGNACHVORJM"
          "HALBQZWOLFP"
          "ZWEINSIEBEN"
          "KDREIRHFUNF"
          "ELFNEUNVIER"
	  "WACHTZEHNRS"
          "BSECHSFMUHR")

# Map instructions:
# The clock works by rounding the time to the nearest 5 minutes.
# This means that you need to have settngs for each five minute interval "m00"
# "m00", "m05".
# The clock also works on a 12 hour basis rather than 24 hour:
# "h00", "h01" etc.
# There are three optional parameters:
#   "all": Anything that is always shown regardless of the time e.g. "It is..."
#   "am":  Wording/symbol to indicate morning.
#   "pm":  Wording/symbol to indicate afternoon/evening
MAP = {
       "all": [0, 1, 3, 4, 5],
       "m00": [107, 108, 109],
       "m05": [7, 8, 9, 10, 35, 36, 37, 38],
       "m10": [11, 12, 13, 14, 35, 36, 37, 38],
       "m15": [26, 27, 28, 29, 30, 31, 32, 35, 36, 37, 38],
       "m20": [15, 16, 17, 18, 19, 20, 21, 35, 36, 37, 38],
       "m25": [7, 8, 9, 10, 39, 40, 41, 44, 45, 46, 47],
       "m30": [44, 45, 46, 47],
       "m35": [7, 8, 9, 10, 35, 36, 37, 38, 44, 45, 46, 47],
       "m40": [15, 16, 17, 18, 19, 20, 21, 39, 40, 41],
       "m45": [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
       "m50": [11, 12, 13, 14, 39, 40, 41],
       "m55": [7, 8, 9, 10, 39, 40, 41],
       "h01": [57, 58, 59, 60],
       "h02": [55, 56, 57, 58],
       "h03": [67, 68, 69, 70],
       "h04": [84, 85, 86, 87],
       "h05": [73, 74, 75, 76],
       "h06": [100, 101, 102, 103, 104],
       "h07": [60, 61, 62, 63, 64, 65],
       "h08": [89, 90, 91, 92],
       "h09": [80, 81, 82, 83],
       "h10": [93, 94, 95, 96],
       "h11": [77, 78, 79],
       "h12": [54, 55, 56, 57, 58],
       "am": [116, 117],
       "pm": [118, 119]
  }

# Number of columns in grid layout
COLS = 11

# Size of letter in grid (x, y)
SIZE = (73, 48)

# Font size of letter
FONTSIZE = 48

# Is our language one where we need to increment the hour after 30 mins
# e.g. 9:40 is "Twenty to ten"
HOUR_INCREMENT = True

HOUR_INCREMENT_TIME = 30
