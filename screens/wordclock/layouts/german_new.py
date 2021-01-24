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
LAYOUT = ("ESKISTLFUENF"
          "ZEHNZWANZIGB"
          "TVORHGNACHJC"
          "DREIVIERTELP"
          "HALBQZWOELFP"
          "ZWEINSIEBENA"
          "KDREIRHFUENF"
          "ELFNEUNVIERS"
	  "WACHTZEHNRSG"
          "BSECHSFMUHRL")

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
       "m00": [116, 117, 118],
       "m05": [7, 8, 9, 10, 11, 30, 31, 32, 33],
       "m10": [12, 13, 14, 15, 30, 31, 32, 33],
       "m15": [40, 41, 42, 43, 44, 45, 46],
       "m20": [7, 8, 9, 10, 11, 30, 31, 32, 33, 40, 41, 42, 43, 44, 45, 46],
       "m25": [7, 8, 9, 10, 11, 25, 26, 27, 48, 49, 50, 51],
       "m30": [48, 49, 50, 51],
       "m35": [7, 8, 9, 10, 11, 30, 31, 32, 33, 48, 49, 50, 51],
       "m40": [7, 8, 9, 10, 11, 25, 26, 27, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46],
       "m45": [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46],
       "m50": [7, 8, 9, 10, 11, 30, 31, 32, 33, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46],
       "m55": [7, 8, 9, 10, 11, 25, 26, 27],
       "h01": [62, 63, 64, 65],
       "h02": [60, 61, 62, 63],
       "h03": [73, 74, 75, 76],
       "h04": [91, 92, 93, 94],
       "h05": [79, 80, 81, 82, 83],
       "h06": [109, 110, 111, 112, 113],
       "h07": [65, 66, 67, 68, 69, 70],
       "h08": [97, 98, 99, 100],
       "h09": [87, 88, 89, 90],
       "h10": [101, 102, 103, 104],
       "h11": [84, 85, 86],
       "h12": [53, 54, 55, 56, 57, 58],
       "am": [120],
       "pm": [120]
  }

# Number of columns in grid layout
COLS = 12

# Size of letter in grid (x, y)
SIZE = (66, 48)

# Font size of letter
FONTSIZE = 48

# Is our language one where we need to increment the hour after 30 mins
# e.g. 9:40 is "Twenty to ten"
HOUR_INCREMENT = True

HOUR_INCREMENT_TIME = 14
print("ende german")
