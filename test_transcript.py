import logging
from youtube_transcript_api import YouTubeTranscriptApi

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    logger.info("Attempting to fetch transcript...")
    transcript = YouTubeTranscriptApi.get_transcript('usOmwLZNVuM', languages=['en'])
    logger.info(f"Successfully retrieved transcript with {len(transcript)} entries")
    for entry in transcript:
        print(f"{entry['text']}")
except Exception as e:
    logger.error(f"Failed to get transcript: {str(e)}", exc_info=True)
