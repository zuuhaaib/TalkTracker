from django.shortcuts import render
from django.conf import settings
from .models import Chat
from .forms import TextInputForm
import openai
import re

openai.api_key = settings.OPENAI_API_KEY

# Helper function to clean and process the conversation
def clean_conversation(chat_text):
    # Remove timestamps (e.g., Nov 02, 2024 8:50 pm)
    chat_text = re.sub(r'\b[A-Za-z]{3} \d{2}, \d{4} \d{1,2}:\d{2} (am|pm)\b', '', chat_text)
    
    # Remove heart emoji likes (e.g., ❤username), which indicates a "like" but is not part of the conversation flow
    chat_text = re.sub(r'❤[a-zA-Z0-9_]+', '', chat_text)
    
    # Remove "Liked a message" and other non-message content
    chat_text = re.sub(r'Liked a message', '', chat_text)
    
    # Remove any extra whitespace that may remain after the substitutions
    chat_text = re.sub(r'\s+', ' ', chat_text).strip()

    return chat_text

# View to reverse the conversation
def reverse_lines_view(request):
    reversed_text = None
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            lines = text.split('\n')
            # Parse each line into structured data
            messages = []
            for line in reversed(lines):
                if ': ' in line:  # Example: "User: Message"
                    user, message = line.split(': ', 1)
                    messages.append({'user': user, 'message': message})
            # Format back as a conversation for display
            formatted_output = '\n'.join([f"{msg['user']}: {msg['message']}" for msg in messages])
            reversed_text = formatted_output
    else:
        form = TextInputForm()

    return render(request, 'index.html', {'form': form, 'reversed_text': reversed_text})

# View to analyze the conversation with different prompts
def analyze_chat_view(request):
    analysis_result = {
        "humor": None,
        "relationship": None,
        "tone": None,
        "shared_understanding": None,
        "self_reflection": None
    }

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            chat_text = form.cleaned_data['text']
            
            cleaned_conversation = clean_conversation(chat_text)

            # Reverse the conversation for GPT to analyze
            lines = cleaned_conversation.split('\n')
            reversed_lines = '\n'.join(reversed(lines))

            # Task 1: Humor Analysis
            prompt_humor = (
                f"Analyze the following conversation and identify specific instances of humor. "
                f"Who is funnier and why? Provide examples of sarcasm, wit, or playful teasing."
                f"\n{reversed_lines}"
            )
            try:
                response_humor = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt_humor}],
                    max_tokens=1000,
                    temperature=0.3,
                )
                analysis_result["humor"] = response_humor.choices[0]['message']['content'].strip()
            except Exception as e:
                analysis_result["humor"] = f"Error generating humor analysis: {str(e)}"

            # Task 2: Relationship Analysis
            prompt_relationship = (
                f"Analyze the relationship between the two participants in the following conversation. "
                f"Are they close friends, acquaintances, or something else entirely? "
                f"Provide examples of moments that support your conclusion."
                f"\n{reversed_lines}"
            )
            try:
                response_relationship = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt_relationship}],
                    max_tokens=1000,
                    temperature=0.3,
                )
                analysis_result["relationship"] = response_relationship.choices[0]['message']['content'].strip()
            except Exception as e:
                analysis_result["relationship"] = f"Error generating relationship analysis: {str(e)}"

            # Task 3: Tone Analysis
            prompt_tone = (
                f"Analyze the tone of the following conversation. Is it lighthearted, casual, or serious? "
                f"Identify any shifts in tone and what causes them."
                f"\n{reversed_lines}"
            )
            try:
                response_tone = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt_tone}],
                    max_tokens=1000,
                    temperature=0.3,
                )
                analysis_result["tone"] = response_tone.choices[0]['message']['content'].strip()
            except Exception as e:
                analysis_result["tone"] = f"Error generating tone analysis: {str(e)}"

            # Task 4: Shared Understanding
            prompt_shared_understanding = (
                f"Do you notice any shared in-jokes, mutual validation, or moments of camaraderie in the conversation? "
                f"How do these contribute to the relationship dynamics?"
                f"\n{reversed_lines}"
            )
            try:
                response_shared = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt_shared_understanding}],
                    max_tokens=1000,
                    temperature=0.3,
                )
                analysis_result["shared_understanding"] = response_shared.choices[0]['message']['content'].strip()
            except Exception as e:
                analysis_result["shared_understanding"] = f"Error generating shared understanding analysis: {str(e)}"

            # Task 5: Self-Reflection
            prompt_self_reflection = (
                f"Identify any moments of self-reflection where the participants reflect on personal thoughts, career goals, "
                f"or introspection. What do these moments reveal about the participants?"
                f"\n{reversed_lines}"
            )
            try:
                response_self_reflection = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt_self_reflection}],
                    max_tokens=1000,
                    temperature=0.3,
                )
                analysis_result["self_reflection"] = response_self_reflection.choices[0]['message']['content'].strip()
            except Exception as e:
                analysis_result["self_reflection"] = f"Error generating self-reflection analysis: {str(e)}"

            # Save all the individual results to the database
            Chat.objects.create(
                user_message=chat_text,
                assistant_reply=str(analysis_result),
                prompt_type="full_analysis"
            )
    else:
        form = TextInputForm()

    return render(request, 'analysis.html', {'form': form, 'analysis_result': analysis_result})

'''def analyze_chat_view_test(request):
    # Mock analysis result (this simulates the API response)
    analysis_result = {
        "humor": "This conversation contains playful teasing and sarcasm, with Zuhaib being funnier.",
        "relationship": "The relationship seems friendly, with lighthearted teasing between the two.",
        "tone": "The tone is casual and playful, with moments of sarcasm.",
        "shared_understanding": "There are shared in-jokes, such as comments about glasses and inventions.",
        "self_reflection": "Manuella expresses frustration with not coming up with new ideas."
    }

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            chat_text = form.cleaned_data['text']
            
            # Clean the conversation text before processing it
            cleaned_conversation = clean_conversation(chat_text)

            # Reverse the conversation for GPT to analyze (no API calls, using mock data)
            lines = cleaned_conversation.split('\n')
            reversed_lines = '\n'.join(reversed(lines))

            # Simulate results without making any API calls
            # Use mocked data directly to show how the result will appear in the front end
            # Save the mocked analysis to the database (optional for testing)
            Chat.objects.create(
                user_message=chat_text,
                assistant_reply=str(analysis_result),
                prompt_type="test_analysis"
            )
    else:
        form = TextInputForm()

    # Return the mocked results for front-end testing
    return render(request, 'analysis.html', {'form': form, 'analysis_result': analysis_result})'''