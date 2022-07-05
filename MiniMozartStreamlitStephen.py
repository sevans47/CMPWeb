import streamlit as st
import numpy as np
import requests
from music21 import note, stream, meter, tie
import music21
from midi2audio import FluidSynth

#initialise some things
MM_API_URL="https://tmp-api-3mknid2ioq-ew.a.run.app"

us = music21.environment.UserSettings()
us['musescoreDirectPNGPath'] = '/usr/bin/mscore'
us['musicxmlPath'] = '/usr/bin/mscore'
us['midiPath'] = '/usr/bin/timidity'

bpm_dict = {1: 4, 2: 2, 4: 1, 8: 0.5, 16: 0.25, 32: 0.125, 64: 0.0625,
            '1': 4, '1d': 6, '2': 2, '2d': 3, '4': 1, '4d': 1.5,
            '8': 0.5, '8d': 0.75, '16': 0.25, '16d': 0.375,
            '32': 0.125, '32d': 0.1875, '64': 0.0625, '64d': 0.09375,
            }


if 'first_session' not in st.session_state:
    st.session_state['first_session'] = True
if 'writing_mode' not in st.session_state:
    st.session_state['writing_mode'] = False
if 'optionlist' not in st.session_state:
    st.session_state['optionlist'] = 'not here yet'
if 'optionnotes' not in st.session_state:
    st.session_state['optionnotes'] = 'not here yet'
if 'optionnames' not in st.session_state:
    st.session_state['optionnames'] = ['👈', '👈', '👈']

empty_stream = stream.Stream()
st.title('MiniMozart🎼✍️')

introtext  = st.empty()
introtext2 = st.empty()
introtext3 = st.empty()
introtext4 = st.empty()

excol1, excol2 = st.columns([1.5,2])
with excol2:
    benwr = st.empty()
excol1, excol2 = st.columns([1.3,5.5])
with excol1:
    benfac = st.empty()
with excol2:
    benim = st.empty()
    benaud = st.empty()

excol1, excol2 = st.columns([1.4,2])
with excol2:
    stewr = st.empty()
excol1, excol2 = st.columns([1.3,5.5])
with excol1:
    stefac = st.empty()
with excol2:
    steim = st.empty()
    steaud = st.empty()

excol1, excol2 = st.columns([1.5,2])
with excol2:
    mizwr = st.empty()
excol1, excol2 = st.columns([1.3,5.5])
with excol1:
    mizfac = st.empty()
with excol2:
    mizim = st.empty()
    mizaud = st.empty()


trycol1, trycol2 = st.columns([1.3,2])
with trycol2:
    ttry = st.empty()
im = st.empty()
aud = st.empty()
ttry.write('**Try it yourself!**')
im.image('blank.png', width = 100)
aud.audio(empty_stream.show('midi'))


col1, col2, col3, col4, col5 = st.columns([1,2,1,2,1])
with col2:
    get_input = st.button('Get a starting bar', key='get_input')
with col4:
    start_writing = st.button('Get suggestions', key='start_writing')

st.write("**Instructions:** Press the left button to randomly choose a mozart bar to start you off. Press play to listen. Once you're happy, press the right button to start writing a melody with MiniMozart's help! Choose a note from the 3 suggestions on the sidebar and keep going until you're happy.")



### get input mode

if get_input:
    st.session_state.first_session = False

    api_url = f"{MM_API_URL}/initialize"
    response = requests.get(api_url).json()['first_sequence']
    input_resp = [[note[0],bpm_dict[note[1]]] for note in response]

    # input_resp = [[np.random.randint(50,70), 16],
    #         [np.random.randint(50,70), 16],
    #         [np.random.randint(50,70), 8],
    #         [0, 8]] #random 4 notes
    st.session_state['input'] = input_resp

    #turn response to stream
    input_pitches, input_durs = [note[0] for note in input_resp], [note[1] for note in input_resp]
    input_notes = [note.Note(pitch, quarterLength = dur) if pitch !=0 else note.Rest(quarterLength=dur) for pitch, dur in zip(input_pitches, input_durs)]
    input_stream = stream.Stream()
    input_stream.append(input_notes)
    #save initial input stream to session state
    st.session_state['input_stream'] = input_stream
    st.session_state['input'] = input_resp

    #add ties
    sequence = input_resp
    s = stream.Stream()
    ts = meter.TimeSignature('4/4')
    s.timeSignature = ts
    total_dur = 0
    last_dur = []
    for pair in sequence:
        n = note.Note(pair[0], quarterLength=pair[1]) if pair[0] !=0 else note.Rest(quarterLength=pair[1])
        total_dur += pair[1]
        last_dur.append(total_dur % 4)
        if len(last_dur) > 1:
            if last_dur[-2] > last_dur[-1] and last_dur[-1] != 0:
                n1 = note.Note(pair[0], quarterLength = s.timeSignature.numerator - last_dur[-2]) if pair[0] !=0 else note.Rest(quarterLength=s.timeSignature.numerator - last_dur[-2])
                n1.tie = tie.Tie('start')
                n2 = note.Note(pair[0],quarterLength=last_dur[-1]) if pair[0] !=0 else note.Rest(quarterLength=last_dur[-1])
                n2.tie = tie.Tie('stop')
                s.append(n1)
                s.append(n2)
                continue
        s.append(n)
    #show stream
    s.show(fmt='lily.png', fp='input')
    im.image('input.png')
    #export to midi / wav
    st.session_state.input_stream.write(fmt='midi',fp='amidifile.mid')
    fs=FluidSynth()
    fs.midi_to_audio('amidifile.mid', 'awavfile.wav')
    aud.audio('awavfile.wav')
    #aud.audio('input.wav')

if st.session_state.first_session:
    introtext.write('**Welcome! MiniMozart is a deep learning powered tool to help you write melodies with Mozarts help.**')
    introtext2.write("Find our project repo on [Github](https://github.com/sevans47/MiniMozart)")
    introtext3.subheader('Our Examples')


#Our model predicts and suggests the 3 notes Mozart might write next in a melody to help you write. To start you off, MiniMozart randomly chooses the first 8 notes of a Mozart melody. Here are some examples pieces written by the team using MiniMozart. The blue is the given Mozart piece, the green is what was generated with our deep learning model')

    htmltxt = '<p <span style="font-family:sans-serif; font-size: 14px;">Here&#39s some melodies the team wrote using suggestions from our deep learning model! </span> <p style="font-family:sans-serif; color:#1a4697; font-size: 14px;"><b>In blue is the real 8 Mozart notes we started with.</b> <span style="font-family:sans-serif; color:#4a8522; font-size: 14px;"><b>In green is what we wrote using deep learning.</b></span></p><p <span style="font-family:sans-serif; color:Black; font-size: 14px;">Scroll down and try it yourself at the bottom! </p>'
    introtext4.markdown(htmltxt, unsafe_allow_html=True)

    benwr.write('**Composed by [Ben Thompson](https://github.com/bendthompson)**')
    benfac.image('benfacec.jpg', width = 117)
    benim.image('bensheetcol.png')
    benaud.audio('benaudio.wav')

    stewr.write('**Orchestrated by [Stephen Evans](https://github.com/sevans47)**')
    stefac.image('stefacec.jpg', width = 117)
    steim.image('stesheetcol.png')
    steaud.audio('steaudio.wav')

    mizwr.write('**Arranged by [Mizuki Nakano](https://github.com/Mizuki8783)**')
    mizfac.image('mizfacec.jpg', width = 123)
    mizim.image('mizsheetcol.png')
    mizaud.audio('mizaudio.wav')




### writing mode

if start_writing:
    #turns on writing mode permanently during the session
    st.session_state['writing_mode'] = True

if st.session_state.writing_mode:
    #set up cols and variables
    c1,c2 = st.sidebar.columns([3,1])
    im.image('input.png')
    #make option buttons
    with c2:
        option1 = st.button(st.session_state.optionnames[0], key='option1')
        st.write('')
        option2 = st.button(st.session_state.optionnames[1], key='option2')
        st.write('')
        option3 = st.button(st.session_state.optionnames[2], key='option3')


    #if you press a button it will append the options from previous iteration, to the main stream
    if option1:
        #st.write('option1')
        st.session_state.input.append(st.session_state.optionlist[0])
        st.session_state.input_stream.append(st.session_state.optionnotes[0]) #4+1
    if option2:
        #st.write('option2')
        st.session_state.input.append(st.session_state.optionlist[1])
        st.session_state.input_stream.append(st.session_state.optionnotes[1]) #4+1
    if option3:
        #st.write('option3')
        st.session_state.input.append(st.session_state.optionlist[2])
        st.session_state.input_stream.append(st.session_state.optionnotes[2]) #4+1

    #add make ties version of mainstream
    sequence = st.session_state.input
    s = stream.Stream()
    ts = meter.TimeSignature('4/4')
    s.timeSignature = ts
    total_dur = 0
    last_dur = []
    for pair in sequence:
        n = note.Note(pair[0], quarterLength=pair[1]) if pair[0] !=0 else note.Rest(quarterLength=pair[1])
        total_dur += pair[1]
        last_dur.append(total_dur % 4)
        if len(last_dur) > 1:
            if last_dur[-2] > last_dur[-1] and last_dur[-1] != 0:
                n1 = note.Note(pair[0], quarterLength = s.timeSignature.numerator - last_dur[-2]) if pair[0] !=0 else note.Rest(quarterLength=s.timeSignature.numerator - last_dur[-2])
                n1.tie = tie.Tie('start')
                n2 = note.Note(pair[0],quarterLength=last_dur[-1]) if pair[0] !=0 else note.Rest(quarterLength=last_dur[-1])
                n2.tie = tie.Tie('stop')
                s.append(n1)
                s.append(n2)
                continue
        s.append(n)

    #write image of tie version
    s.show(fmt='lily.png', fp='input')
    #display new main stream
    #st.session_state.input_stream.show(fmt='lily.png', fp='input') #4+1
    im.image('input.png')
    #display audio

    st.session_state.input_stream.write(fmt='midi',fp='amidifile.mid')
    fs=FluidSynth()
    fs.midi_to_audio('amidifile.mid', 'awavfile.wav')
    aud.audio('awavfile.wav')

    #send lagged input to api
    send8 = st.session_state.input[-8:]
    seq={"sequence": str(send8)}
    res = requests.get(f"{MM_API_URL}/predict", params=seq)
    model_resp = res.json()['predictions']


    # #receive output of 3 notes
    # model_resp = [
    #         [np.random.randint(70,90), int(np.random.choice([4,8,16]))],
    #         [np.random.randint(70,90), int(np.random.choice([4,8,16]))],
    #         [np.random.randint(70,90), int(np.random.choice([4,8,16]))]]

    #turn to notes
    model_pitches, model_durs = [note[0] for note in model_resp], [note[1] for note in model_resp]
    model_notes = [note.Note(pitch, quarterLength = dur) if pitch !=0 else note.Rest(quarterLength=dur) for pitch, dur in zip(model_pitches, model_durs)]

    desc1 = st.sidebar.empty()
    desc21,desc22 = st.sidebar.columns([1.7,2])
    desc3 = st.sidebar.empty()
    desc41,desc42 = st.sidebar.columns([1.7,2])
    with desc1:
        st.write(f'Suggested Notes:')
    with desc22:
        st.write(f'{model_notes[0].name}, {model_notes[1].name}, and {model_notes[2].name}')
    with desc3:
        st.write(f'Suggested Durations:')
    with desc42:
        st.write(f'{model_durs[0]}, {model_durs[1]}, and {model_durs[2]}')
    #assign new options to session state for next round

    st.session_state['optionlist'] = model_resp
    st.session_state['optionnotes'] = model_notes
    #st.session_state['optionnames'] = [note.name for note in model_notes]


    #make empty streams
    op1stream = stream.Stream()
    op2stream = stream.Stream()
    op3stream = stream.Stream()

    #append input stream which will grow each iter: 4, 5, 6, ...
    input_stream = st.session_state.input_stream
    op1stream.append(input_stream)
    op2stream.append(input_stream)
    op3stream.append(input_stream)

    #add the 3 options to make option streams to show
    op1, op2, op3 = model_notes
    op1stream.append(op1) #4+1+1
    op2stream.append(op2) #4+1+1
    op3stream.append(op3) #4+1+1

    #save 3 options stream sheets
    #display 3 options stream sheets
    op1stream.show(fmt='lily.png', fp='option1') #4+1++1
    with c1:
        st.image('option1.png')
    op2stream.show(fmt='lily.png', fp='option2') #4+1+1
    with c1:
        st.image('option2.png')
    op3stream.show(fmt='lily.png', fp='option3') #4+1+1
    with c1:
        st.image('option3.png')



#to do
#image sizes
#option names on button
#containers to align buttons
#autofill
#ties
