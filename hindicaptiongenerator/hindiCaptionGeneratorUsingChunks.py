import speech_recognition as sr
from pydub import AudioSegment
from googletrans import Translator
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from hindicaptiongenerator.createSrtFile import split_transcription, create_srt_file


# Split audio into chunks with overlap
def split_audio_with_overlap(audio_path, chunk_length_ms=10000, overlap_ms=2000):
    audio = AudioSegment.from_wav(audio_path)
    chunks = []
    start = 0
    end = chunk_length_ms

    while end < len(audio):
        chunks.append(audio[start:end])
        start += chunk_length_ms - overlap_ms
        end = start + chunk_length_ms

    # Add last chunk
    if start < len(audio):
        chunks.append(audio[start:])

    return chunks


# Recognize the audio chunks
def transcribe_audio_chunks(audio_chunks):
    recognizer = sr.Recognizer()
    transcription = ""
    for i, chunk in enumerate(audio_chunks):
        chunk.export(f"temp_chunk_{i}.wav", format="wav")
        with sr.AudioFile(f"temp_chunk_{i}.wav") as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language='hi-IN')
                print(f"Chunk {i + 1} transcription: {text}")
                transcription += text + " "
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
    return transcription


# Translate the text to Hindi (if needed)
def translate_text_to_hindi(text):
    translator = Translator()
    translated = translator.translate(text, dest='hi')
    return translated.text


# Generate captioned video in Hindi
def create_captioned_video(video_path, caption_text):
    video = VideoFileClip(video_path)
    # Create a TextClip for captions
    caption_clip = TextClip(caption_text, fontsize=24, color='white', size=video.size)
    caption_clip = caption_clip.set_duration(video.duration).set_position(('center', 'bottom'))

    # Combine the video and caption
    final_video = CompositeVideoClip([video, caption_clip])
    final_video.write_videofile("output_video_with_hindi_captions.mp4", codec="libx264", fps=24)


if __name__ == "__main__":
    video_file = "G:/test.mp4"  # Path to the video file

    # Extract audio from the video
    audio_file = VideoFileClip(video_file).audio
    audio_file.write_audiofile("temp_audio.wav")

    # Split the audio into smaller chunks and transcribe
    audio_chunks = split_audio_with_overlap("temp_audio.wav")
    transcription = transcribe_audio_chunks(audio_chunks)

    # Split transcription into chunks
    chunks = split_transcription(transcription, chunk_size=20)  # Adjust chunk_size as needed

    # Create SRT file
    create_srt_file(chunks, 'output_subtitles.srt', chunk_duration=5)  # Adjust chunk_duration as needed

    # Optionally, translate to Hindi (if original transcription was in English)
    # hindi_captions = translate_text_to_hindi(transcription)
    #
    # # Generate video with Hindi captions
    # create_captioned_video(video_file, hindi_captions)
