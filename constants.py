### MUSIC CONSTANTS ###
# MIDI pitch for middle C
MIDDLE_C = 60

# 12 pitches in an octave
STEPS_PER_OCTAVE = 12

# 7 steps from tonic to dominant (in major scale)
STEPS_TO_DOMINANT = 7

# maximum range is 1 octave below, 1 octave above
OCTAVE_RANGE = 2

# WWHWWWH steps for pitches in melody
MAJOR_MELODY_STEPS = [2, 2, 1, 2, 2, 2, 1]

EIGHTH_NOTE = 1 / 2
QUARTER_NOTE = 1
DOTTED_QUARTER_NOTE = 1 + 1 / 2
HALF_NOTE = 2

# measured in quarter notes
NOTE_LENGTHS = [EIGHTH_NOTE, QUARTER_NOTE, DOTTED_QUARTER_NOTE, HALF_NOTE]

# measured in quarter notes
MEASURE_LENGTH = 4

# number of measures in melody
NUM_MEASURES = 8

### MIDI CONSTANTS ###
DEFAULT_VOLUME = 100

DEFAULT_BPM = 60

MIDI_FILE_SUFFIX = ".mid"
SUFFIX_LENGTH = len(MIDI_FILE_SUFFIX)