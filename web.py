import io

import streamlit as st
import pretty_midi
from scipy.io import wavfile
import numpy as np
import music21



#----------sheet music----------
s = music21.converter.parse('tinyNotation: 4/4 C4_hi D-4_its E#4_working F8 trip{G4 A4 B4}')

path=''
name='sheet'
s.show(fmt='lily.png',fp=path+name)
st.image('sheet.png')


#----------output to midi----------
seq_of_notes =[]
bpm_dict = {1: 4, 2: 2, 4: 1, 8: 0.5, 16: 0.25}
bpm = 120

def notes_to_midi(model_output, bpm=120):
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program('Acoustic Guitar (nylon)'))

    prev_start = 0
    seq_of_notes.append(model_output)
    spb = 60/bpm

    for note in seq_of_notes:
        duration = bpm_dict[note[1]] * spb
        start = float(prev_start)
        end = float(prev_start + duration)
        if note[0] == 0:
            start += float(duration)
            prev_start = start
        else:
            note = pretty_midi.Note(velocity=100, pitch=note[0], start=start, end=end)
            instrument.notes.append(note)
            prev_start = end

    pm.instruments.append(instrument)
    pm.write('example.mid')
    return pm

midi = notes_to_midi([73, 16])

#-----------convert midi to wav----------#
#midi_file = open('song/mz_311_1.mid', "rb")

#midi_data = pretty_midi.PrettyMIDI(midi_file)
#audio_data = midi_data.fluidsynth()
audio_data = midi.fluidsynth()
audio_data = np.int16(
    audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
)

virtualfile = io.BytesIO()
wavfile.write(virtualfile, 44100, audio_data)

#----------play----------#
st.audio(virtualfile)
