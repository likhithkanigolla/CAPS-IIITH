import base64
import os
import sys
import google.generativeai as genai
from google.generativeai.types import content_types

def generate(input_file_path):
    try:
        with open(input_file_path, 'r') as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Configure the API key
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        system_instruction="""You are an expert in model-based systems engineering and simulation.

I will give you an XML `.capssaml` file written in the CAPS framework.

Your task is to parse it and generate a **valid JSON file** that can later be used to create simulation models in PyDEVS.

# ... [rest of your system instruction remains unchanged]
"""
    )

    # Create the prompt content
    prompt = input_text

    # Generate content using streaming
    response = model.generate_content(prompt, stream=True)
    
    for chunk in response:
        print(chunk.text, end="")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file_path>")
    else:
        generate(sys.argv[1])
