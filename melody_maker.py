import sys
import random
import pygame
from constants import *
from midiutil import MIDIFile
from collections import defaultdict

# assuming all largest note length
def find_min_path_length(num_measures):
    return MEASURE_LENGTH / NOTE_LENGTHS[-1] * num_measures

# assuming all smallest note length until final half note
def find_max_path_length(num_measures):
    smallest_in_half = HALF_NOTE / NOTE_LENGTHS[0]
    smallest_in_measure = MEASURE_LENGTH / NOTE_LENGTHS[0]
    return MEASURE_LENGTH / NOTE_LENGTHS[0] * num_measures - smallest_in_half + 1

def random_DFS(graph, source, targets, target_length):

    def random_DFS_visit(path):
        node = path[-1]
        length = len(path)
        found_path = None
        if length < target_length:
            random.shuffle(graph[node])
            print(graph[node])
            i = 0
            while i < len(graph[node]) and found_path == None:
                neighbor = graph[node][i]
                new_path = path + [neighbor]
                
                if neighbor in targets and len(new_path) == target_length:
                    found_path = new_path
                
                if found_path == None:
                    found_path = random_DFS_visit(new_path)

                i += 1
        return found_path

    path = random_DFS_visit([source])
    assert path != None, "NO PATH FOUND"
    return path

def is_bad_length(beats_remaining, measure_beats, notes_remaining, length):
    if length > measure_beats:
        print("A")
        print(beats_remaining, measure_beats, notes_remaining, length)
        return True

    if (notes_remaining * NOTE_LENGTHS[0]) > beats_remaining:
        print("B")
        print(beats_remaining, measure_beats, notes_remaining, length)
        return True

    if (notes_remaining * NOTE_LENGTHS[-1]) < beats_remaining:
        print("C")
        print(beats_remaining, measure_beats, notes_remaining, length)
        return True

    return False

def construct_measures(note_path, num_measures):
    measures = []
    num_notes = len(note_path)
    beats = num_measures * MEASURE_LENGTH - HALF_NOTE # last note will be half note
    measure = []
    measure_beats = MEASURE_LENGTH
    for i in range(num_notes - 1):
        print(num_notes)
        note_length = random.choice(NOTE_LENGTHS)
        while is_bad_length(beats - note_length, measure_beats, num_notes - 2, note_length):
            note_length = random.choice(NOTE_LENGTHS)

        measure.append((note_path[i], note_length))
        beats -= note_length
        measure_beats -= note_length

        if measure_beats == 0:
            measures.append(measure)
            measure = []
            measure_beats = MEASURE_LENGTH

        num_notes -= 1
    measure.append((note_path[-1], HALF_NOTE))
    measures.append(measure)

    return measures

def generate_note_list(tonic, next_notes):
    # M4 should end on dominant
    targets = set()
    low_tonic = tonic - STEPS_PER_OCTAVE
    for i in range(OCTAVE_RANGE):
        targets.add(low_tonic + STEPS_TO_DOMINANT + STEPS_PER_OCTAVE * i)
    
    # randomly construct note path within certain length
    min_length = find_min_path_length(4)
    max_length = find_max_path_length(4)
    target_length = random.randint(min_length, max_length)
    note_path = random_DFS(next_notes, tonic, targets, target_length)

    # fill M1-M4 with pitch-length tuples
    measures = construct_measures(note_path, 4)

    # copy M1 and M2 into M5 and M6, respectively
    measures.append(measures[0])
    measures.append(measures[1])

    # find last note of M6
    last_note = measures[-1][-1][0]

    # M8 should end on tonic
    targets = set()
    low_tonic = tonic - STEPS_PER_OCTAVE
    for i in range(OCTAVE_RANGE + 1):
        targets.add(low_tonic + STEPS_PER_OCTAVE * i)

    # randomly construct note path within certain length
    min_length = find_min_path_length(2)
    max_length = find_max_path_length(2)
    target_length = random.randint(min_length, max_length)
    note_path = random_DFS(next_notes, last_note, targets, target_length)

    # fill M7 and M8
    measures.extend(construct_measures(note_path, 2))

    return measures

def make_MIDI_file(frmt=1, track=0, time=0, tempo=DEFAULT_BPM):
    midi = MIDIFile(frmt)
    midi.addTempo(track, time, tempo)

    return midi

def add_note(midi, pitch, time, duration, volume=DEFAULT_VOLUME, track=0, channel=0):
    midi.addNote(track, channel, pitch, time, duration, volume)

# randomly generates one-handed major melody
def generate_melody(filename, tonic):
    next_notes = {}
    
    # create dictionary mapping pitches to possible next pitches
    pitch = tonic - STEPS_PER_OCTAVE * OCTAVE_RANGE // 2
    for _ in range(OCTAVE_RANGE):
        next_notes[pitch] = [pitch]
        for step in MAJOR_MELODY_STEPS:

            next_pitch = pitch + step
            next_notes[pitch].append(next_pitch)
            next_notes[next_pitch] = [pitch, next_pitch]

            pitch = next_pitch

    # overwrite possible next pitches for leading tones
    pitch = tonic - STEPS_PER_OCTAVE * OCTAVE_RANGE // 2
    for _ in range(OCTAVE_RANGE):
        leading = pitch + STEPS_PER_OCTAVE - 1
        next_notes[leading] = [leading + 1]

        pitch += STEPS_PER_OCTAVE

    note_list = generate_note_list(tonic, next_notes)

    midi = make_MIDI_file()
    time = 0
    for measure in note_list:
        print(measure)
        for pitch, length in measure:
            add_note(midi, pitch, time, length)
            time += length

    with open(filename, "wb") as midi_file:
        midi.writeFile(midi_file)

def play_melody(filename):
    pygame.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(1000)

if __name__ == "__main__":
    filename = sys.argv[1]
    assert (filename[-SUFFIX_LENGTH:] == MIDI_FILE_SUFFIX)

    generate_melody(filename, MIDDLE_C)
    play_melody(filename)