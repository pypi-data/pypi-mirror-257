import os
import re
import requests
from io import BytesIO
import numpy as np
from pydub import AudioSegment
import librosa


def download_audio(url, path_to_store=None, store=False):
    if len(re.findall("\.(mp3|wav)", url)) > 0:
        USER_AGENT = {'User-agent': 'Mozilla/5.0'}
        r = requests.get(url, allow_redirects=True)
        file_name = (url.split("?")[0].split('/')[-1]).split(".")[0]

        sound = AudioSegment.from_file(BytesIO(r.content))

        if store:
            sound.export(os.path.join(path_to_store, "{}.wav".format(file_name)), format="wav")

        return sound


def get_temporary_public_url_from_a_private_url(recording_url):
    try:
        if "restricted" in recording_url:
            return (requests.get(
                "https://app.squadiq.in/voice/core/get-temporary-url?recording_url=" + str(recording_url)
            ).json()['recording_url'])
        else:
            return recording_url
    except:
        return None


def load_audio(path, rate=16000):
    audio = AudioSegment.from_wav(path)
    audio = audio.set_frame_rate(rate)
    audio = audio.split_to_mono()

    return audio


def get_array(audio):
    return np.array(audio.get_array_of_samples()).astype(np.float32)


def get_melspectogram(audio, rate=16000):

    sgram = librosa.stft(np.array(audio.get_array_of_samples()).astype(np.float32))
    sgram_mag, _ = librosa.magphase(sgram)
    mel_scale_sgram = librosa.feature.melspectrogram(S=sgram_mag, sr=rate)
    mel_sgram = librosa.amplitude_to_db(mel_scale_sgram, ref=np.min)

    return mel_sgram


def audio_split(audio, hop_length_ms=None, clip_size_ms=10000):
    clips = []

    if hop_length_ms is None:
        hop_length_ms = clip_size_ms

    for i in range(len(audio) // hop_length_ms + 1):
        temp = audio[i * hop_length_ms: i * hop_length_ms + clip_size_ms]
        clips.append(temp)

    return clips


def time_shift(audio, shift_duration, shift_axis):
    if shift_axis == "left":
        shift_duration = -shift_duration

    return np.roll(
        np.array(audio.get_array_of_samples()).T.astype(np.float32),
        shift_duration
    )