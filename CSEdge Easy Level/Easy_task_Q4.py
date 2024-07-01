import pyaudio
import wave
import numpy as np

class VoiceRecorder:
    def __init__(self, chunk=1024, format=pyaudio.paInt16, channels=1, rate=44100, record_seconds=5, output_file="output.wav"):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.record_seconds = record_seconds
        self.output_file = output_file
        self.p = pyaudio.PyAudio()

    def record(self):
        print("Recording...")
        stream = self.p.open(format=self.format,
                             channels=self.channels,
                             rate=self.rate,
                             input=True,
                             frames_per_buffer=self.chunk)
        frames = []

        for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        self.p.terminate()

        wf = wave.open(self.output_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def playback(self):
        wf = wave.open(self.output_file, 'rb')
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)
        data = wf.readframes(self.chunk)

        print("Playing back...")

        while data:
            stream.write(data)
            data = wf.readframes(self.chunk)

        stream.stop_stream()
        stream.close()
        self.p.terminate()
        print("Playback finished.")

    def save_as(self, new_file):
        print(f"Saving as {new_file}...")
        with wave.open(self.output_file, 'rb') as wf:
            with wave.open(new_file, 'wb') as wf_new:
                wf_new.setnchannels(wf.getnchannels())
                wf_new.setsampwidth(wf.getsampwidth())
                wf_new.setframerate(wf.getframerate())
                wf_new.writeframes(wf.readframes(wf.getnframes()))
        print("File saved.")

if __name__ == "__main__":
    recorder = VoiceRecorder(record_seconds=10)
    recorder.record()
    recorder.playback()
    recorder.save_as("output_copy.wav")