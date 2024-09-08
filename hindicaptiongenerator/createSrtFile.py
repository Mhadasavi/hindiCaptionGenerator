import math


def split_transcription(transcription, chunk_size=200):
    """
    Split transcription text into chunks of specified size.
    """
    words = transcription.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks


def format_srt_entry(index, start_time, end_time, text):
    """
    Format a single SRT entry.
    """
    return f"{index}\n{start_time} --> {end_time}\n{text}\n"


def time_to_srt_format(seconds):
    """
    Convert time in seconds to SRT format (HH:MM:SS,MS).
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}"


def create_srt_file(chunks, output_file, chunk_duration=5):
    """
    Create an SRT file from text chunks.
    """
    with open(output_file, 'w', encoding="utf-8") as f:
        start_time = 0
        for i, chunk in enumerate(chunks):
            end_time = start_time + chunk_duration
            f.write(format_srt_entry(
                i + 1,
                time_to_srt_format(start_time),
                time_to_srt_format(end_time),
                chunk
            ))
            start_time = end_time


# if __name__ == "__main__":
#     # Example transcription text
#     transcription = "This is an example transcription. It needs to be split into chunks and formatted into SRT file. Each chunk should be properly timed."
#
#     # Split transcription into chunks
#     chunks = split_transcription(transcription, chunk_size=20)  # Adjust chunk_size as needed
#
#     # Create SRT file
#     create_srt_file(chunks, 'output_subtitles.srt', chunk_duration=5)  # Adjust chunk_duration as needed
