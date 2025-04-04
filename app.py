import os
import wave
import threading
import numpy as np
import pyaudio
import concurrent.futures
import pandas as pd
import speech_recognition as sr
from flask import Flask, render_template, jsonify
from pyannote.audio import Pipeline

# Flask app
app = Flask(__name__)

# Globals
SAMPLE_RATE = 44100
CHANNELS = 1
CHUNK_DURATION = 3
FORMAT = pyaudio.paInt16
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)
recording = False
chunk_index = 1
recorded_audio = []
result_df = pd.DataFrame(columns=["fileId", "speaker", "utterance"])
executor = concurrent.futures.ThreadPoolExecutor()
futures_list = []
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.0",
    use_auth_token="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"
)

def save_wav(filename, data):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.tobytes())

def rttm_to_dataframe(rttm_file_path):
    columns = ["type", "fileId", "channel", "start time", "duration", "orthology", "confidence", "speaker", 'x', 'y']
    with open(rttm_file_path, "r") as rttm_file:
        lines = rttm_file.readlines()
        data = [line.strip().split() for line in lines]
        df = pd.DataFrame(data, columns=columns)
        df = df.drop(['x', 'y', "orthology", "confidence", "type", "channel"], axis=1)
        return df

def extract_text_from_audio(audio_file_path, start_time, end_time):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source, duration=end_time - start_time, offset=start_time)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "(Unintelligible)"
    except sr.RequestError as e:
        return f"API error: {e}"

def process_rttm_and_transcribe(rttm_file_path, audio_file_path):
    global result_df
    df = rttm_to_dataframe(rttm_file_path)
    df = df.astype({'start time': 'float', 'duration': 'float'})
    df['end time'] = df['start time'] + df['duration']
    df['utterance'] = df.apply(lambda row: extract_text_from_audio(audio_file_path, row['start time'], row['end time']), axis=1)
    df = df[['fileId', 'speaker', 'utterance']]
    result_df = df

def process_chunk(file, audio_file_path):
    print(f"Processing {file} for diarization...")
    diarization = pipeline(file)
    with open("audio.rttm", "w") as rttm:
        diarization.write_rttm(rttm)
    print(f"Overwritten audio.rttm with {file}")
    process_rttm_and_transcribe("audio.rttm", audio_file_path)

def record_audio():
    global recording, chunk_index, recorded_audio, futures_list

    recorded_audio = []
    chunk_index = 1

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)

    while recording:
        print(f"Recording chunk {chunk_index}...")
        chunk = stream.read(CHUNK_SIZE)
        recorded_audio.append(chunk)
        all_data = b''.join(recorded_audio)

        filename = f"chunk_{chunk_index}.wav"
        save_wav(filename, np.frombuffer(all_data, dtype=np.int16))
        print(f"Saved: {filename}")

        if chunk_index % 3 == 0:
            future = executor.submit(process_chunk, filename, filename)
            futures_list.append(future)

        chunk_index += 1

    stream.stop_stream()
    stream.close()
    audio.terminate()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-recording')
def start_recording():
    global recording
    recording = True
    threading.Thread(target=record_audio).start()
    return jsonify({"status": "Recording started"})

@app.route('/stop-recording')
def stop_recording():
    global recording, chunk_index, futures_list, recorded_audio
    recording = False

    last_chunk = chunk_index - 1
    filename = f"chunk_{last_chunk}.wav"
    print(f"Stopping recording. Last chunk: {filename}")

    if not os.path.exists(filename):
        print(f"Saving final chunk: {filename}")
        chunk_data = b''.join(recorded_audio[-1:])
        save_wav(filename, np.frombuffer(chunk_data, dtype=np.int16))

    for future in futures_list:
        if not future.done():
            future.cancel()
    futures_list = []

    if last_chunk % 3 != 0:
        print(f"Submitting final chunk {filename} for diarization (not multiple of 3).")
        threading.Thread(target=process_chunk, args=(filename, filename)).start()
    else:
        print(f"Final chunk {filename} was already diarized (multiple of 3).")

    return jsonify({"status": f"Recording stopped. Final chunk {filename} handled."})

@app.route('/get-transcript')
def get_transcript():
    global result_df
    return result_df.to_json(orient="records")

@app.route('/clear', methods=['POST'])
def clear_files():
    global result_df
    result_df = pd.DataFrame(columns=['fileId', 'speaker', 'utterance'])

    for file in os.listdir():
        if file.endswith(".wav") or file.endswith(".rttm"):
            os.remove(file)

    return "All audio and transcript files deleted."

if __name__ == '__main__':
    app.run(debug=True)
