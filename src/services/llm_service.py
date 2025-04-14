"""
from ctransformers import AutoModelForCausalLM

# Load the model only once
model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
    model_file="tinyllama-1.1b-chat-v1.0.Q3_K_S.gguf",
    model_type="llama",
    gpu_layers=0
)

def generate_interpretation(prompt: str) -> str:
    try:
        if not prompt:
            return "Please provide a valid question and chart data."
            
        # More constrained generation parameters
        response = model(
            prompt,
            max_new_tokens=150,  # Reduced from 300
            temperature=0.7,      # Add some creativity but not too much
            repetition_penalty=1.2,  # Discourage repetition
            stop=["\n\n"]         # Stop at double newlines
        )
        
        # Post-processing to clean up response
        clean_response = response.strip()
        if clean_response.count(":") > 3:  # Simple check for repetitive output
            return "I couldn't generate a clear interpretation. Please try rephrasing your question."
        return clean_response
        
    except Exception as e:
        print(f"Generation error: {str(e)}")
        return "Error generating interpretation. Please try again."



import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
#load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY="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"
# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Set model name
model = "gpt-4o-mini"

def generate_interpretation(prompt: str) -> str:
    try:
        if not prompt:
            return "Please provide a valid question and chart data."

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert astrologer who gives clear and insightful interpretations based on astrology charts."},
                {"role": "user", "content": prompt}
            ],
            #max_tokens=150,
            #temperature=0.7,
            #stop=["\n\n"]
        )

        response = completion.choices[0].message.content.strip()

        if response.count(":") > 3:
            return "I couldn't generate a clear interpretation. Please try rephrasing your question."
        
        return response

    except Exception as e:
        print(f"Generation error: {str(e)}")
        return "Error generating interpretation. Please try again."

print(generate_interpretation("What does it mean if my sun is in Leo and moon is in Pisces?"))

"""
from openai import OpenAI
OPENAI_API_KEY="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"
model = "gpt-4o-mini"

# Create OpenAI client

client = OpenAI(api_key=OPENAI_API_KEY)

import time

# Example rate limit (e.g., 1 request per second)
RATE_LIMIT_INTERVAL = 1  # seconds
last_request_time = 0

def generate_interpretation(prompt: str) -> str:
    global last_request_time
    current_time = time.time()
    
    # Check if we need to wait to respect rate limit
    if current_time - last_request_time < RATE_LIMIT_INTERVAL:
        time.sleep(RATE_LIMIT_INTERVAL - (current_time - last_request_time))
    
    last_request_time = time.time()
    
    try:
        if not prompt:
            return "Please provide a valid question and chart data."

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert astrologer who gives clear and insightful interpretations based on astrology charts."},
                {"role": "user", "content": prompt}
            ]
            
        )

        response = completion.choices[0].message.content.strip()

        if response.count(":") > 3:
            return "I couldn't generate a clear interpretation. Please try rephrasing your question."
        
        return response

    except Exception as e:
        if "insufficient_quota" in str(e):
            return "You have exceeded your current quota. Please check your plan and billing details."
        print(f"Generation error: {str(e)}")
        return "Error generating interpretation. Please try again."
prompt="hello chat,will i get married soon?"
print(generate_interpretation(prompt))