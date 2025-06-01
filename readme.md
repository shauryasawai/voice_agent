# Voice AI Agent Using Django

A web-based conversational AI that enables voice-to-voice interaction using Django, Google Cloud APIs, and OpenAI GPT.

## 🎯 Overview

This project creates a complete voice AI agent that can:
- Accept voice input from users
- Convert speech to text using Google Cloud Speech-to-Text
- Process the text using OpenAI's GPT models
- Convert the AI response back to speech using Google Cloud Text-to-Speech
- Play the audio response to the user

## 🚀 Features

- **Real-time Voice Interaction**: Record and play audio directly in the browser
- **Multi-API Integration**: Seamlessly connects STT, LLM, and TTS services
- **Responsive UI**: Clean, minimal interface for easy testing
- **Error Handling**: Graceful fallbacks for unrecognized inputs
- **Production Ready**: Deployable structure with proper configuration

## 🏗️ Architecture

```
User Voice Input → STT API → LLM Processing → TTS API → Audio Response
```

## 📁 Project Structure

```
voice_agent/
├── base/             
│   ├── templates/base/
│   │   └── index.html               # Main UI template
│   ├── views.py                     # Django views handling requests
│   ├── urls.py                      # URL routing
│   └── api_integration.py           # API integration layer
├── project/
│   ├── settings.py                  # Django configuration
│   └── urls.py                      # Main URL configuration
├── requirements.txt                 # Python dependencies
├── manage.py                        # Django management script
└── README.md                        # Project documentation
```

## 🛠️ Technologies Used

### Backend
- **Django 4.2.7**: Web framework
- **Google Cloud Speech-to-Text API**: Voice recognition
- **Google Cloud Text-to-Speech API**: Speech synthesis
- **OpenAI GPT API**: Natural language processing
- **Python 3.8+**: Programming language

### Frontend
- **HTML5**: Structure and layout
- **JavaScript (ES6+)**: Client-side logic
- **Web Audio API**: Audio recording and playback
- **CSS3**: Styling and responsive design

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account with STT/TTS APIs enabled
- OpenAI API account
- Modern web browser with microphone access

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/shauryasawai/voice_agent/
cd voice_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root:

```env
GOOGLE_CLOUD_API_KEY=your_google_cloud_api_key
OPENAI_API_KEY=your_openai_api_key
```

Or update `api_integration.py` directly with your API keys.

### 4. Run the Development Server

```bash
python manage.py runserver
```

### 5. Access the Application

Open your browser and navigate to `http://localhost:8000`

## 🔧 API Integration Details

### Speech-to-Text (Google Cloud)

**Endpoint**: `https://speech.googleapis.com/v1/speech:recognize`

**Request Format**:
```json
{
  "config": {
    "encoding": "LINEAR16",
    "sampleRateHertz": 16000,
    "languageCode": "en-US"
  },
  "audio": {
    "content": "<BASE64_ENCODED_AUDIO>"
  }
}
```

**Response**:
```json
{
  "results": [
    {
      "alternatives": [
        {
          "transcript": "Hello, how are you?",
          "confidence": 0.987
        }
      ]
    }
  ]
}
```

### OpenAI GPT Integration

**Endpoint**: `https://api.openai.com/v1/chat/completions`

**Request Format**:
```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful AI assistant."
    },
    {
      "role": "user",
      "content": "<USER_INPUT_TEXT>"
    }
  ],
  "max_tokens": 150,
  "temperature": 0.7
}
```

**Response**:
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "I'm doing well, thank you for asking!"
      }
    }
  ]
}
```

### Text-to-Speech (Google Cloud)

**Endpoint**: `https://texttospeech.googleapis.com/v1/text:synthesize`

**Request Format**:
```json
{
  "input": {
    "text": "<AI_RESPONSE_TEXT>"
  },
  "voice": {
    "languageCode": "en-US",
    "ssmlGender": "NEUTRAL"
  },
  "audioConfig": {
    "audioEncoding": "MP3"
  }
}
```

**Response**:
```json
{
  "audioContent": "<BASE64_ENCODED_MP3_AUDIO>"
}
```

## 🔄 Application Workflow

1. **Voice Recording**: User clicks "Start Recording" button
2. **Audio Capture**: Browser captures microphone input using Web Audio API
3. **Data Transmission**: Audio data is sent to Django backend as FormData
4. **Speech Recognition**: Backend sends audio to Google STT API
5. **Text Processing**: Transcribed text is sent to OpenAI GPT
6. **Response Generation**: GPT generates appropriate response
7. **Speech Synthesis**: Response text is sent to Google TTS API
8. **Audio Playback**: Generated audio is sent back to frontend and played

## 🎛️ API Endpoints

### POST `/process-voice/`

Processes voice input and returns audio response.

**Request**:
- Content-Type: `multipart/form-data`
- Body: Audio file (WAV format)

**Response**:
```json
{
  "success": true,
  "audio_content": "<BASE64_ENCODED_MP3>",
  "transcript": "User's spoken text",
  "response_text": "AI's text response"
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Error description"
}
```

## 🎨 Frontend JavaScript API

### AudioRecorder Class

```javascript
class AudioRecorder {
  constructor();
  startRecording();     // Begin audio capture
  stopRecording();      // End capture and process
  playAudio(base64);    // Play received audio response
}
```

### Key Functions

- `initializeRecorder()`: Sets up Web Audio API
- `sendAudioToBackend()`: Transmits recorded audio
- `handleResponse()`: Processes server response
- `updateUI()`: Manages button states and feedback

## 🔒 Security Considerations

- Store API keys in environment variables
- Implement rate limiting for API calls
- Validate and sanitize audio input
- Use HTTPS in production
- Implement proper CORS settings

## 🚀 Deployment

### Environment Variables

```env
DEBUG=False
SECRET_KEY=your_secret_key
GOOGLE_CLOUD_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ALLOWED_HOSTS=your-domain.com
```

### Recommended Platforms

- **Heroku**: Easy deployment with buildpacks
- **Railway**: Modern deployment platform
- **Render**: Free tier available
- **DigitalOcean App Platform**: Scalable hosting

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up static file serving
- [ ] Configure database (if needed)
- [ ] Set up monitoring and logging
- [ ] Implement SSL certificate

## 🧪 Testing

### Manual Testing
1. Grant microphone permissions
2. Click "Start Recording"
3. Speak clearly into microphone
4. Click "Stop Recording"
5. Wait for AI response
6. Verify audio playback

### Browser Compatibility
- Chrome 60+ ✅
- Firefox 55+ ✅
- Safari 11+ ✅
- Edge 79+ ✅

## 🔧 Configuration Options

### Audio Settings
```python
# In api_integration.py
AUDIO_CONFIG = {
    'encoding': 'LINEAR16',
    'sample_rate': 16000,
    'language_code': 'en-US'
}
```

### GPT Model Settings
```python
GPT_CONFIG = {
    'model': 'gpt-3.5-turbo',
    'max_tokens': 150,
    'temperature': 0.7
}
```

### TTS Voice Settings
```python
TTS_CONFIG = {
    'language_code': 'en-US',
    'ssml_gender': 'NEUTRAL',
    'audio_encoding': 'MP3'
}
```

## 🐛 Troubleshooting

### Common Issues

**Microphone not working**:
- Check browser permissions
- Ensure HTTPS in production
- Verify Web Audio API support

**API errors**:
- Verify API keys are correct
- Check API quotas and billing
- Review network connectivity

**Audio quality issues**:
- Adjust sample rate settings
- Check microphone quality
- Review browser audio settings

### Debug Mode

Enable debug logging in `settings.py`:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'voice_agent': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📈 Performance Optimization

- Implement audio compression
- Cache common responses
- Use connection pooling for APIs
- Optimize frontend audio processing
- Implement request queuing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Cloud Platform for STT/TTS APIs
- OpenAI for GPT models
- Django community for the excellent framework
- Web Audio API contributors

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation links

---

**Made with ❤️ using Django and AI APIs**
