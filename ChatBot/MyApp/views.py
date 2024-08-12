import json
import os
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import openai
import graphviz
import requests
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter
from django.views.decorators.csrf import csrf_exempt

# Set your OpenAI API key here
openai.api_key = "your-key-here"
client = openai.OpenAI(api_key=openai.api_key)

# Initialize session state (simulating Streamlit session state)
session_state = {
    'file_ids': [],
    'assistant_id': "asst_BnyJKJc8SXEgaMSSO5aUNvP0"
}

def home(request):
    context={}
    return render(request, 'MyApp/home.html',context)

def about(request):
    context={}
    return render(request, 'MyApp/about.html',context)

def services(request):
    context={}
    return render(request, 'MyApp/services.html',context)

def contact(request):
    context={}
    return render(request, 'MyApp/contact.html',context)

def faq(request):
    context={}
    return render(request, 'MyApp/faq.html',context)

def youtube_summarizer(request):
    context={}
    return render(request, 'MyApp/youtube_summarizer.html',context)

def pdf_chat(request):
    context={}
    return render(request, 'MyApp/pdf_chat.html',context)

# Function to interact with ChatGPT
def chat_with_gpt(messages):
    try:
        response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [ 
             {"role": "system", "content": messages},
        ]
    )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error interacting with OpenAI API: {e}")
        return "Error generating summary. Please try again."

# Function to get video transcript
def get_video_transcript(youtube_url):
    def get_video_id(url):
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1]
        return None

    video_id = get_video_id(youtube_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en'])
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript.fetch())
        return transcript_text
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        raise ValueError(f"Error fetching transcript: {str(e)}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {str(e)}")


def summarize(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            youtube_url = data.get('youtube_url')
        else:
            youtube_url = request.POST.get('youtube-url')
        
        print(f"Received YouTube URL: {youtube_url}")
        
        if youtube_url:
            try:
                transcript = ""
                try:
                    transcript = get_video_transcript(youtube_url)
                except Exception as e:
                    print(f"Error fetching transcript: {str(e)}")
                
                if not transcript:
                    title, description = get_video_details(youtube_url)
                    transcript = f"Title: {title}\nDescription: {description}"
                prompt = f"Summarize the following YouTube video transcript :\n\n{transcript}"
                print(f"Generated Prompt: {prompt}")
                
                summary = chat_with_gpt(prompt)
                print(f"Generated Summary: {summary}")

                if request.content_type == 'application/json':
                    return JsonResponse({'summary': summary})
                else:
                    return JsonResponse({'summary': summary})
            except ValueError as e:
                return HttpResponseBadRequest(str(e))
            except Exception as e:
                return HttpResponseBadRequest(f"Error fetching transcript: {str(e)}")
        else:
            return HttpResponseBadRequest('No URL provided')
    else:
        return HttpResponseBadRequest('Invalid request method')
    
def get_video_details(youtube_url):
    response = requests.get(youtube_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('meta', property='og:title')['content']
        description = soup.find('meta', property='og:description')['content']
        return title, description
    else:
        raise ValueError("Unable to fetch video details")
    
@csrf_exempt
def ask_question_view(request):
    youtube_url = None
    youtube_question = None

    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                youtube_url = data.get('youtube-url-hidden')
                youtube_question = data.get('youtube-question')
            except json.JSONDecodeError:
                return HttpResponseBadRequest('Invalid JSON')
        else:
            youtube_url = request.POST.get('youtube-url-hidden')
            youtube_question = request.POST.get('youtube-question')

        print(f"Received YouTube URL: {youtube_url} and question {youtube_question}")

        if youtube_url:
            try:
                transcript = get_video_transcript(youtube_url)
                if not transcript:
                    title, description = get_video_details(youtube_url)
                    transcript = f"Title: {title}\nDescription: {description}"
                prompt = f"Answer this user question: {youtube_question} from this YouTube video:\n\n{transcript}"
                print(f"Generated Prompt: {prompt}")

                summary = chat_with_gpt(prompt)
                print(f"Generated answer: {summary}")

                if request.content_type == 'application/json':
                    return JsonResponse({'answer': summary})
                else:
                    return JsonResponse({'answer': summary})
            except ValueError as e:
                return HttpResponseBadRequest(str(e))
            except Exception as e:
                return HttpResponseBadRequest(f"Error fetching transcript: {str(e)}")
        else:
            return HttpResponseBadRequest('No URL provided')
    else:
        return HttpResponseBadRequest('Invalid request method')


def create_assistant(request):
    try:
        assistant = client.beta.assistants.create(
            name="PDF Assistant",
            description="You are a pdf assistant. Use the document to answer questions.",
            instructions="""
                IMPORTANT:
                1. If user asks for the file name, do not provide file id. Use the file name provided in the additional instructions.
                2. Give answers straight forward. do not include additional comments.
                3. Analyze chat history provided in the additional instructions before analyzing the document. If you can give the answer by using the chat history provided, use it or if you can't provide a proper answer then analyze the file.

                If the user query seems to be not relevant to the uploaded file just respond as "couldn't found a relevant content from this (file name)".
            """,
            tools=[{"type":"file_search"}],
            model="gpt-3.5-turbo"
        )
        assistant_id = assistant.id
        print(f"Created assistant with ID: {assistant_id}")
        return render(request, 'myApp/youtube_summarizer.html', {'assistant_id': assistant_id})
    except Exception as e:
        print(f"Error creating assistant: {e}")
        return render(request, 'myApp/youtube_summarizer.html', {'assistant_id': e})
    
@csrf_exempt
def chat_pdf(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('pdf_files')
        user_query = request.POST.get('user_query')

        # Save uploaded files temporarily in the root directory of the project
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            file_paths.append(file_path)

            # Upload each file to OpenAI and store file_ids
            message_file = client.files.create(
                file=open(file_path, 'rb'),  # Open the file in binary mode for uploading
                purpose="assistants"
            )
            session_state['file_ids'].append(message_file.id)

        # Create file attachments from file_ids
        attachments = [{"file_id": file_id, "tools": [{"type": "file_search"}]} for file_id in session_state['file_ids']]

        # Create a thread with user query and attachments
        thread = client.beta.threads.create(
            messages=[{"role": "user", "content": user_query, "attachments": attachments}]
        )

        # Create and poll the run to get results
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=session_state['assistant_id'],
            additional_instructions="dO not append [0] at the end. just the straightforward answer"
        )

        # Retrieve messages from the run
        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        # Clean up temporary files (optional)
        for file_path in file_paths:
            os.remove(file_path)

        if messages:
            message_content = messages[0].content[0].text
            annotations = message_content.annotations
            citations = []
            for index, annotation in enumerate(annotations):
                message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
                if file_citation := getattr(annotation, "file_citation", None):
                    cited_file = client.files.retrieve(file_citation.file_id)
                    citations.append(f"[{index}] {cited_file.filename}")
            
            session_state['file_ids'] = []
            # Return JSON response with processed content
            # return render(request, 'MyApp/pdf_chat.html', {'result': message_content.value})
            return JsonResponse({'result': message_content.value, 'citations': citations})

        else:
            return HttpResponseBadRequest('No messages received from OpenAI.')

    else:
        return HttpResponseBadRequest('Invalid request method')
