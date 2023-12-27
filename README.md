# YouTube Video Downloader & Summarizer

This Python script automates the process of downloading audio from YouTube videos, transcribing the audio using OpenAI's Whisper, summarizing the transcription with OpenAI's GPT models, and cleaning up the downloaded files. It is designed to be easy to use and highly customizable with command-line arguments.

## Features

- **Audio Download**: Downloads the best audio quality from a given YouTube video using `yt-dlp`.
- **Audio Transcription**: Transcribes the audio using OpenAI's Whisper model.
- **Summarization**: Summarizes the transcription using OpenAI's GPT-3.5-turbo, GPT-4, or other specified models.
- **Customizable**: Adjust Whisper model size and GPT model via command-line arguments.

## Prerequisites

Before you start, ensure you have met the following requirements:
- Python 3.6 or higher.
- `ffmpeg` installed on your system.
- An OpenAI API key with access to GPT and Whisper models.

## Installation

1. **Clone the repository**:
   `git clone https://github.com/ancientdeit/yt-video-summary.git`
2. **Navigate to the directory**:
   `cd yt-video-summary`
3. **Install required packages**:
   `pip install -r requirements.txt`
4. **Set up your '.env' file**:
   `OPENAI_API_KEY=your_api_key_here`

## Usage

Run the script from the command line, providing the necessary arguments:

  `python yt_video_summary.py [YouTube Video URL] [Whisper Model Size] [GPT Model] [Summary Language]`

The script will process the video, transcribe the audio, generate a summary, save the summary to a text file, and clean up the downloaded files.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
[OpenAI](https://openai.com/)

[yt-dlp](https://github.com/yt-dlp/yt-dlp)

[FFmpeg](https://ffmpeg.org/)
