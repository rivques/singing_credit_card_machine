import time
from gpiozero import DigitalOutputDevice # pyright: reportMissingImports=false

enable_pin = DigitalOutputDevice(18)
coil_A_1_pin = DigitalOutputDevice(4)
coil_A_2_pin = DigitalOutputDevice(17)
coil_B_1_pin = DigitalOutputDevice(23)
coil_B_2_pin = DigitalOutputDevice(24)

enable_pin.value = True

def forward(delay, steps):
    i = 0
    while i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        i += 1

def backwards(delay, steps):
    i = 0
    while i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        i += 1

def setStep(w1, w2, w3, w4):
    coil_A_1_pin.value = w1
    coil_A_2_pin.value = w2
    coil_B_1_pin.value = w3
    coil_B_2_pin.value = w4

def playFreq(freq, length, bpm, go_forward=True):
    steps = round(length*60/bpm*freq)
    if go_forward:
        forward(1/freq, steps)
    else:
        backwards(1/freq, steps)

def getFrequency(note, A4=440):
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    octave = int(note[2]) if len(note) == 3 else int(note[1])
        
    keyNumber = notes.index(note[0:-1]);
    
    if (keyNumber < 3) :
        keyNumber = keyNumber + 12 + ((octave - 1) * 12) + 1; 
    else:
        keyNumber = keyNumber + ((octave - 1) * 12) + 1; 

    return A4 * 2** ((keyNumber- 49) / 12)

def playNote(note, length, bpm, go_forward=True):
    playFreq(getFrequency(note), length, bpm, go_forward)

def rest(length, bpm):
    time.sleep(length*240/bpm)

def playSong(notes, lengths, types, bpm):
    assert len(notes) == len(lengths), 'The number of notes and lengths are not the same!'
    assert len(notes) == len(types), 'The number of notes and types are not the same!'
    for i, note in enumerate(notes):
        if note in ['', 'rs', 'RS', 'rest', 'REST']:
            rest(lengths[i], bpm)
        else:
            if types[i][1] in ['s', 'S']:
                playNote(note, lengths[i], bpm)
            else:
                noteLength = lengths[i]*3/4 if lengths[i] <= 1/4 else lengths[i] - 1/8
                playNote(note, noteLength, bpm)
                rest(lengths[i]-noteLength, bpm)

songs = {
    'In The Hall of the Mountain King': {
        'bpm': 120,
        'notes': ['D4', 'E4', 'F4', 'G4', 'A4', 'F4', 'A4', 'G#4', 'E4', 'G#4', 'G4', 'D#4', 'G4', 'D4', 'E4', 'F4', 'G4', 'A4', 'F4', 'A4', 'D5', 'C5', 'A4', 'F4', 'A4', 'C5'], 
        'lengths': [1/8, 1/8,  1/8,  1/8,  1/8,  1/8,  1/4,   1/8,  1/8,   1/4,  1/8,   1/8,  1/4,  1/8,  1/8,  1/8,  1/8,  1/8,  1/8,  1/8,  1/8,  1/8,  1/8,  1/8,  1/8,  1/2],
        'types': ['.X', '.X', '.X', '.X', '.X', '.X', '.X',  '.X', '.X',  '.X', '.X',  '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.X']
    },
    'Twinkle Twinkle Little Star': {
        'bpm': 60,
        'notes': ['C4', 'C4', 'G4', 'G4'],
        'lengths': [1/4, 1/4,  1/4,  1/4],
        'types': ['.X', '.X', '.X', '.X']
    },
    'Once Upon A Time': {
        'bpm': 131, #                                                                                                                                                                                                                                                                                               0:49                                                        0:53
        'notes': ['C4', 'C5', 'F4',  'C4', 'F4', 'F3', 'C4', 'F4', 'C5', 'D5', 'C5', 'G4', 'F4', 'A#3', 'B3', 'C4', 'RS', 'C5', 'A4', 'G4', 'F4', 'E4', 'F4', 'G4', 'RS', 'E5', 'D5', 'C#5', 'C5', 'D4', 'D4', 'D4', 'C5', 'A4', 'G4', 'F4', 'G4', 'A4', 'E4', 'RS', 'G4', 'RS', 'G4', 'F4', 'E4', 'F4', 'C4', 'RS', 'C5', 'A4', 'G4', 'F4', 'E4', 'F4', 'G4', 'RS', 'E5', 'RS', 'D5', 'C#5', 'C5'],
        'lengths': [1/2, 1/2,    1,   1/2,  1/2,    1,  1/2,  1/2,  1/2,  1/2,  1/2,  1/2,    1,  1/16, 1/16,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  3/8, 1/16,  1/16,    1,  1/4,  1/8,  1/8,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4,  1/4, 1/16,  1/16,  3/8],
        'types': ['.S', '.S', '.S',  '.S', '.S', '.X', '.S', '.S', '.S', '.S', '.S', '.S', '.X',  '.S', '.S', '.X', '.X', '.X', '.X', '.X', '.S', '.S', '.X', '.X', '.X', '.S', '.S',  '.S', '.X', '.X', '.X', '.X', '.X', '.X', '.X', '.S', '.S', '.X', '.X', '.X', '.X', '.X', '.X', '.S', '.S', '.X', '.S', '.X', '.X', '.X', '.X', '.S', '.S', '.S', '.S', '.X', '.S', '.X', '.S',  '.S', '.X']
    },
    'Hopes and Dreams': {
        'bpm': 171,
        'notes': ['F5', 'RS', 'F6', 'RS', 'C6', 'RS', 'A#5', 'RS', 'F6', 'RS', 'F5', 'RS'],
        'lengths': [1/8, 3/8,  1/8,  3/8,  1/8,  7/8,   1/8,  3/8,  1/8,  3/8,  1/8,  7/8],
        'types': ['.S', '.X', '.S', '.X', '.S', '.X',  '.S', '.X', '.S', '.X', '.S', '.X', ]
    },
    'MEGALOVANIA': {
        'bpm': 120,
        'notes': [],
        'lengths': [],
        'types': []
    },
}

def main():
    while True:
        print('\nWhich song would you like to hear? We have:\n')
        for i, key in enumerate(songs.keys()):
            print(f'{i}: {key}')
        song_num = int(input('\nEnter a number: '))
        song = songs[list(songs.keys())[song_num]]
        time.sleep(1.5)
        playSong(song['notes'], song['lengths'], song['types'], song['bpm'])


if __name__ == '__main__':
    main()