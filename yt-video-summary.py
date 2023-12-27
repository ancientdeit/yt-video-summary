import argparse
import os
import yt_dlp
import whisper
import time
from openai import OpenAI
from dotenv import load_dotenv

# Setup the argument parser
parser = argparse.ArgumentParser(description="Download audio from YouTube, transcribe it using Whisper, summarize the transcription with OpenAI's GPT, and clean up the downloaded files.")
parser.add_argument("video_url", help="The URL of the YouTube video")
parser.add_argument("whisper_model_size", help="The size of the Whisper model to use (e.g., tiny, base, small, medium, large)")
parser.add_argument("gpt_model", help="The GPT model to use for summarization (e.g., gpt-3.5-turbo, gpt-4, gpt-4-1106-preview). For longer videos remember to use models with larger context window.")
args = parser.parse_args()

# Load the .env file
load_dotenv()

# Initialize OpenAI API key
client = OpenAI()
client.api_key = os.getenv('OPENAI_API_KEY')

# Download audio from YouTube using yt-dlp
def download_audio(video_url):
    # Define the output template for the original file
    original_file_template = 'original_downloaded_file.%(ext)s'

    options = {
        'format': 'bestaudio/best',  # Choose the best quality audio format
        'extractaudio': True,  # Only keep the audio
        'audioformat': 'wav',  # Convert to wav
        'outtmpl': original_file_template,  # Use the defined template
        'noplaylist': True,  # Only download single video and not a playlist
        'postprocessors': [{  # Postprocessors for extracting and converting audio
            'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
            'preferredcodec': 'wav',  # Specify the desired codec
            'preferredquality': '192',  # Specify the quality
        }, {
            'key': 'FFmpegMetadata',  # Add metadata to the file (optional)
        }]
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    # Define the names for the final files
    input_file = "original_downloaded_file.wav"
    output_file = "output.wav"

    # Convert the audio to mono, 16kHz, and 16-bit using FFmpeg directly
    ffmpeg_command = f"ffmpeg -i '{input_file}' -ac 1 -ar 16000 -sample_fmt s16 '{output_file}'"
    os.system(ffmpeg_command)

    if os.path.exists(input_file):
        os.remove(input_file)

    return output_file

# Transcribe audio using Whisper
def transcribe_audio(audio_path, model_size):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

# Generate a summary using OpenAI GPT
def generate_summary(transcription, gpt_model):
    # Construct the initial conversation context
    messages = [
        {"role": "system", "content": "You are a helpful assistant tasked with summarizing transcriptions."},
        {"role": "user", "content": f"Please summarize the following transcription: {transcription}"}
    ]

    attempts = 0
    max_attempts = 3
    response = None

    while attempts < max_attempts:
        try:
            # Make the API call to generate the completion
            response = client.chat.completions.create(
                model=gpt_model,
                messages=messages
            )
            # Break the loop if the response is successful
            break
        except Exception as e:
            print(f"Attempt {attempts + 1} failed: {e}")
            attempts += 1
            time.sleep(1)  # Wait a bit before retrying to avoid overwhelming the server

    if response:
        # Extract the assistant's reply from the response
        summary = response.choices[0].message.content
        return summary.strip()
    else:
        # Return a default message or raise an error if all attempts fail
        return "Failed to generate a summary after several attempts."

# Clean up the downloaded audio file
def clean(audio_path):
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"Deleted the file: {audio_path}")
    else:
        print(f"The file {audio_path} does not exist")

# Save the summary to a text file
def save_summary(summary, filename):
    with open(filename, 'w') as file:
        file.write(summary)
    print(f"Summary saved to {filename}")

# Main process
if __name__ == "__main__":
    audio_path = download_audio(args.video_url)
    transcription = transcribe_audio(audio_path, args.whisper_model_size)
    summary = generate_summary(transcription, args.gpt_model)
    
    # Save summary to a text file
    summary_filename = os.path.splitext(audio_path)[0] + "_summary.txt"
    save_summary(summary, summary_filename)

    # Clean up the downloaded audio
    clean(audio_path)
    print("\nSummary:\n", summary)
