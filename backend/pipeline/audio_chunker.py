import os
import math
import soundfile as sf


def chunk_audio(
    audio_path: str,
    chunk_duration: int = 30
) -> list:
    """
    Split WAV audio into chunks of `chunk_duration` seconds.

    Returns list of chunk file paths.
    """

    data, sample_rate = sf.read(audio_path)
    total_samples = len(data)

    samples_per_chunk = sample_rate * chunk_duration
    total_chunks = math.ceil(total_samples / samples_per_chunk)

    base_name = os.path.splitext(audio_path)[0]
    chunk_paths = []

    for i in range(total_chunks):
        start = i * samples_per_chunk
        end = min(start + samples_per_chunk, total_samples)

        chunk_data = data[start:end]

        chunk_path = f"{base_name}_chunk_{i:03d}.wav"
        sf.write(chunk_path, chunk_data, sample_rate)

        chunk_paths.append(chunk_path)

    return chunk_paths