from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .api_integration import speech_to_text, get_ai_response, text_to_speech

def index(request):
    """
    Render the main page
    """
    return render(request, 'base/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def process_voice(request):
    """
    Process voice input and return AI response as audio
    """
    try:
        # Get the uploaded audio file
        if 'audio' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio']
        audio_content = audio_file.read()
        
        # Step 1: Convert speech to text
        print("Converting speech to text...")
        transcript = speech_to_text(audio_content)
        print(f"Transcript: {transcript}")
        
        # Step 2: Get AI response
        print("Getting AI response...")
        ai_response = get_ai_response(transcript)
        print(f"AI Response: {ai_response}")
        
        # Step 3: Convert AI response to speech
        print("Converting text to speech...")
        audio_response = text_to_speech(ai_response)
        
        if audio_response:
            # Return the audio file
            response = HttpResponse(audio_response, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="response.mp3"'
            return response
        else:
            return JsonResponse({
                'error': 'Failed to generate audio response',
                'transcript': transcript,
                'ai_response': ai_response
            }, status=500)
            
    except Exception as e:
        print(f"Error in process_voice: {str(e)}")
        return JsonResponse({
            'error': 'An error occurred while processing your voice input',
            'details': str(e)
        }, status=500)