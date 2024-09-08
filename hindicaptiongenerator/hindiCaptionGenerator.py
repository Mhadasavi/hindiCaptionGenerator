import speech_recognition as sr
from googletrans import Translator
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


# Recognize the audio from a video file
def transcribe_audio_from_video(video_path):
    recognizer = sr.Recognizer()
    audio_file = VideoFileClip(video_path).audio
    audio_file.write_audiofile("temp_audio.wav")

    with sr.AudioFile("temp_audio.wav") as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print("Transcription: ", text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None


# Translate the text to Hindi
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
    video_file = "G:/insta1.mp4"  # Path to the video file
    transcription = transcribe_audio_from_video(video_file)

    # if transcription:
        # hindi_captions = translate_text_to_hindi(transcription)
        # create_captioned_video(video_file, hindi_captions)
