from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .models import ChatMessage
from .forms import ChatForm
import openai

openai.api_key = settings.OPENAI_API_KEY

def generate_chatbot_response(user_message, chat_history=None):
    if chat_history is None:
        chat_history = []

    # Append user message to chat history
    chat_history.append({'role': 'user', 'content': user_message})

    # Generate chatbot response using OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    # Extract chatbot's reply from the response
    chatbot_reply = response['choices'][0]['message']['content']

    return chatbot_reply

def chatbot(request):
    # Check if it's a new session
    new_session = not request.session.get('initialized', False)
    if new_session:
        request.session['initialized'] = True

        # If it's a new session, clear chat history
        ChatMessage.objects.all().delete()

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['message']

            # Retrieve chat history from the database
            chat_history = list(ChatMessage.objects.filter(sender='User').values_list('message', flat=True))

            # Format chat history for OpenAI API
            formatted_chat_history = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
            for message in chat_history:
                formatted_chat_history.append({'role': 'user', 'content': message})

            # Generate chatbot response
            chatbot_response = generate_chatbot_response(user_message, formatted_chat_history)

            # Save user message to the database
            ChatMessage.objects.create(sender='User', message=user_message)

            # Save chatbot response to the database
            ChatMessage.objects.create(sender='Bot', message=chatbot_response)

            return redirect('chatbot')
    else:
        form = ChatForm()

    messages = ChatMessage.objects.all()
    return render(request, 'chatbot.html', {'form': form, 'messages': messages})
