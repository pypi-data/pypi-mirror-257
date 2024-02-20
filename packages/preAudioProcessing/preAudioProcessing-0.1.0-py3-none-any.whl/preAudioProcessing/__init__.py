from pathlib import Path

from pydub import AudioSegment
from pydub.silence import split_on_silence


def convert_m4a_to_wav(input_path, output_path) -> bool:
    audio = AudioSegment.from_file(input_path, format="m4a")
    audio.export(output_path, format="wav")

    return True


def convert_mp3_to_wav(input_path, output_path) -> bool:
    audio = AudioSegment.from_file(input_path, format="mp3")
    audio.export(output_path, format="wav")

    return True


def split_audio_on_silence(input_path, output_folder="output_segments", silence_thresh=-50) -> bool:
    # Load the audio file
    output_folder = Path(output_folder)
    audio = AudioSegment.from_file(input_path)
    name = Path(input_path).name.replace(Path(input_path).suffix, "")

    segments = split_on_silence(audio, min_silence_len=400, silence_thresh=silence_thresh)

    for i, segment in enumerate(segments):
        Path.mkdir(output_folder, exist_ok=True, parents=True)
        segment.export(output_folder / f"{name}_{i + 1}.wav", format="wav")

    return True


def audio_reader_filter(path_to_read, path_to_write="filtered_audio", audio_threshold=9,
                        sample_rate_to_write=16000) -> bool:
    path_to_write = Path(path_to_write)
    Path.mkdir(path_to_write, exist_ok=True)
    path_to_read = Path(path_to_read)
    if not path_to_read:
        NotImplemented("Specify audio segment directory")

    for i, one_audio in enumerate(path_to_read.glob("*.wav")):

        try:
            audio_vector = AudioSegment.from_wav(one_audio).set_frame_rate(sample_rate_to_write)
            print(audio_vector.duration_seconds, " secs ")
        except:
            Exception(f"Audio number {i} with name {one_audio.name} reading error")
            break
        if 1 <= audio_vector.duration_seconds <= audio_threshold:
            audio_vector.export(path_to_write / f"{one_audio.name}", format="flac")
        else:
            continue

    return True


if __name__ == "__main__":
    print("Successful Installation")
