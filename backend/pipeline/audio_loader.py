import os
import librosa
import soundfile as sf
from pydub import AudioSegment


def normalize_audio(input_path: str) -> str:
    """
    Convert any audio format to:
    - WAV
    - Mono
    - 16kHz

    Returns path to normalized WAV file.
    """

    base, _ = os.path.splitext(input_path)
    output_path = f"{base}_normalized.wav"

    # Step 1: Load using pydub (format-agnostic)
    audio = AudioSegment.from_file(input_path)

    # Step 2: Convert to mono
    audio = audio.set_channels(1)

    # Step 3: Export temporary WAV
    temp_wav = f"{base}_temp.wav"
    audio.export(temp_wav, format="wav")

    # Step 4: Resample to 16kHz using librosa
    y, sr = librosa.load(temp_wav, sr=16000, mono=True)
    sf.write(output_path, y, 16000)

    # Cleanup temp file
    os.remove(temp_wav)

    return output_path