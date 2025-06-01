import requests
import base64
import json
import os
from django.conf import settings
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class APIKeyManager:
    """
    Secure API key management class that retrieves keys from:
    1. Environment variables (including .env file)
    2. Django settings (as fallback)
    """
    @staticmethod
    def get_google_stt_key():
        return os.getenv('GOOGLE_STT_API_KEY', getattr(settings, 'GOOGLE_STT_API_KEY', None))
    
    @staticmethod
    def get_google_tts_key():
        return os.getenv('GOOGLE_TTS_API_KEY', getattr(settings, 'GOOGLE_TTS_API_KEY', None))
    
    @staticmethod
    def get_openai_key():
        return os.getenv('OPENAI_API_KEY', getattr(settings, 'OPENAI_API_KEY', None))


def speech_to_text(audio_content, audio_encoding="WEBM_OPUS", sample_rate=48000, language_code="en-US"):
    """
    Convert audio to text using Google Speech-to-Text API
    
    Args:
        audio_content (bytes): Raw audio data
        audio_encoding (str): Audio encoding format
        sample_rate (int): Sample rate of the audio
        language_code (str): Language code for recognition
    
    Returns:
        str: Transcribed text or error message
    """
    try:
        api_key = APIKeyManager.get_google_stt_key()
        if not api_key:
            logger.error("Google STT API key not configured")
            return "Speech recognition service is not properly configured."
            
        url = f"https://speech.googleapis.com/v1/speech:recognize?key={api_key}"
        
        # Convert audio to base64
        audio_base64 = base64.b64encode(audio_content).decode('utf-8')
        
        payload = {
            "config": {
                "encoding": audio_encoding,
                "sampleRateHertz": sample_rate,
                "languageCode": language_code,
                "enableAutomaticPunctuation": True,
                "enableWordTimeOffsets": False,
                "enableWordConfidence": True,
                "model": "latest_long",
                "useEnhanced": True,
                "profanityFilter": False,
                "speechContexts": [],
                "maxAlternatives": 1,
                "audioChannelCount": 1,
                "enableSeparateRecognitionPerChannel": False
            },
            "audio": {
                "content": audio_base64
            }
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Your-App-Name/1.0'
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"STT API Error - Status: {response.status_code}, Response: {response.text}")
            error_detail = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            return f"Speech recognition failed: {error_detail.get('error', {}).get('message', 'Unknown error')}"
            
        result = response.json()
        
        if 'results' in result and len(result['results']) > 0:
            best_alternative = result['results'][0]['alternatives'][0]
            transcript = best_alternative['transcript']
            confidence = best_alternative.get('confidence', 0.0)
            
            logger.info(f"STT Success - Confidence: {confidence:.2f}")
            
            if confidence > 0.5:
                return transcript
            else:
                return f"Low confidence transcription: {transcript}"
        else:
            logger.warning(f"No speech detected. Full response: {result}")
            return "Sorry, I couldn't detect any speech in the audio. Please speak more clearly."
            
    except requests.exceptions.Timeout:
        logger.error("Speech-to-Text request timed out")
        return "Sorry, the speech recognition service timed out. Please try again."
    except requests.exceptions.RequestException as e:
        logger.error(f"Speech-to-Text Request Error: {e}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"Response content: {e.response.text}")
        return "Sorry, there was a network error processing your speech."
    except Exception as e:
        logger.error(f"Speech-to-Text Unexpected Error: {str(e)}")
        return "Sorry, there was an unexpected error processing your speech."

def get_ai_response(text, model="gpt-4o-mini", max_tokens=150):
    """
    Get AI response using OpenAI GPT API
    
    Args:
        text (str): User input text
        model (str): OpenAI model to use
        max_tokens (int): Maximum tokens in response
    
    Returns:
        str: AI response or error message
    """
    try:
        api_key = APIKeyManager.get_openai_key()
        if not api_key:
            logger.error("OpenAI API key not configured")
            return "AI service is not properly configured."
            
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Your-App-Name/1.0'
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful voice assistant. Keep responses concise and conversational, suitable for voice interaction."
                },
                {
                    "role": "user", 
                    "content": text
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "presence_penalty": 0.1,
            "frequency_penalty": 0.1
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"OpenAI API Error - Status: {response.status_code}, Response: {response.text}")
            error_detail = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            return f"AI service error: {error_detail.get('error', {}).get('message', 'Unknown error')}"
            
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            ai_response = result['choices'][0]['message']['content'].strip()
            logger.info(f"OpenAI Success - Response length: {len(ai_response)}")
            return ai_response
        else:
            logger.warning(f"No choices in OpenAI response: {result}")
            return "I'm sorry, I couldn't generate a response right now."
            
    except requests.exceptions.Timeout:
        logger.error("OpenAI API request timed out")
        return "I'm taking too long to think. Please try again."
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenAI API Request Error: {e}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"Response content: {e.response.text}")
        return "I'm having trouble connecting to my AI service right now. Please try again."
    except Exception as e:
        logger.error(f"OpenAI API Unexpected Error: {str(e)}")
        return "I'm having an unexpected issue right now. Please try again."

def text_to_speech(text, language_code="en-US", voice_name=None, speaking_rate=1.0, pitch=0.0):
    """
    Convert text to speech using Google Text-to-Speech API
    
    Args:
        text (str): Text to convert to speech
        language_code (str): Language code for the voice
        voice_name (str): Specific voice name (optional)
        speaking_rate (float): Speaking rate (0.25 to 4.0)
        pitch (float): Voice pitch (-20.0 to 20.0)
    
    Returns:
        bytes: Audio data in MP3 format or None if error
    """
    try:
        api_key = APIKeyManager.get_google_tts_key()
        if not api_key:
            logger.error("Google TTS API key not configured")
            return None
            
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"
        
        voice_config = {
            "languageCode": language_code,
        }
        
        if voice_name:
            voice_config["name"] = voice_name
        else:
            voice_config["ssmlGender"] = "NEUTRAL"
        
        audio_config = {
            "audioEncoding": "MP3",
            "speakingRate": max(0.25, min(4.0, speaking_rate)),
            "pitch": max(-20.0, min(20.0, pitch)),
            "volumeGainDb": 0.0,
            "sampleRateHertz": 24000,
        }
        
        text_input = {}
        if text.strip().startswith('<speak>') and text.strip().endswith('</speak>'):
            text_input["ssml"] = text
        else:
            text_input["text"] = text
        
        payload = {
            "input": text_input,
            "voice": voice_config,
            "audioConfig": audio_config
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Your-App-Name/1.0'
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"TTS API Error - Status: {response.status_code}, Response: {response.text}")
            return None
            
        result = response.json()
        
        if 'audioContent' in result:
            audio_data = base64.b64decode(result['audioContent'])
            logger.info(f"TTS Success - Audio size: {len(audio_data)} bytes")
            return audio_data
        else:
            logger.warning(f"No audioContent in TTS response: {result}")
            return None
            
    except requests.exceptions.Timeout:
        logger.error("Text-to-Speech request timed out")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Text-to-Speech Request Error: {e}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"Response content: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Text-to-Speech Unexpected Error: {str(e)}")
        return None

def list_available_voices(language_code=None):
    """
    List available voices from Google Text-to-Speech API
    
    Args:
        language_code (str): Filter voices by language code (optional)
    
    Returns:
        list: List of available voices or empty list if error
    """
    try:
        api_key = APIKeyManager.get_google_tts_key()
        if not api_key:
            logger.error("Google TTS API key not configured")
            return []
            
        url = f"https://texttospeech.googleapis.com/v1/voices?key={api_key}"
        
        if language_code:
            url += f"&languageCode={language_code}"
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Your-App-Name/1.0'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Voices API Error - Status: {response.status_code}, Response: {response.text}")
            return []
            
        result = response.json()
        return result.get('voices', [])
        
    except Exception as e:
        logger.error(f"List Voices Error: {str(e)}")
        return []

def validate_api_keys():
    """
    Validate that all required API keys are present
    
    Returns:
        tuple: (bool, list) - (all_valid, missing_keys)
    """
    missing_keys = []
    
    if not APIKeyManager.get_google_stt_key():
        missing_keys.append('GOOGLE_STT_API_KEY')
    if not APIKeyManager.get_google_tts_key():
        missing_keys.append('GOOGLE_TTS_API_KEY')
    if not APIKeyManager.get_openai_key():
        missing_keys.append('OPENAI_API_KEY')
    
    return len(missing_keys) == 0, missing_keys

def process_voice_interaction(audio_content, audio_encoding="WEBM_OPUS", sample_rate=48000):
    """
    Complete pipeline: Speech-to-Text -> AI Response -> Text-to-Speech
    
    Args:
        audio_content (bytes): Raw audio data
        audio_encoding (str): Audio encoding format
        sample_rate (int): Sample rate of the audio
    
    Returns:
        tuple: (transcript, ai_response, audio_response_bytes)
    """
    valid_keys, missing = validate_api_keys()
    if not valid_keys:
        error_msg = f"Missing API keys: {', '.join(missing)}"
        logger.error(error_msg)
        return error_msg, error_msg, None
    
    transcript = speech_to_text(audio_content, audio_encoding, sample_rate)
    if transcript.startswith("Sorry") or transcript.startswith("Speech recognition failed"):
        return transcript, transcript, None
    
    ai_response = get_ai_response(transcript)
    if ai_response.startswith("AI service error") or ai_response.startswith("I'm having"):
        return transcript, ai_response, None
    
    audio_response = text_to_speech(ai_response)
    
    return transcript, ai_response, audio_response