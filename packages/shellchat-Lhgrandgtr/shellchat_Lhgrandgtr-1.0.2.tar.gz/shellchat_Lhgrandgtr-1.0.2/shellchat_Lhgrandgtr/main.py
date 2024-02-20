from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
import requests
import json
import argparse
from time import sleep

style = Style.from_dict({
    "welcome": "bold underline",
    "question": "fg:#00FF00",
    "generated_text": "fg:#FF0000",
    "error": "fg:#FF0000",
    "prompt": "fg:#FFA500",
    "prompt_text": "fg:#FFFFFF",
})

# def generate_text(question, url):
#     payload = {
#         "text": question
#     }
 
#     headers = {
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(payload))

#     if response.status_code == 200:
#         print_formatted_text(HTML("<ansired>B-chat:</ansired>"), HTML(f"<ansigreen>{response.json()}</ansigreen>"), style=style)
#     else:
#         print_formatted_text(HTML("<ansired>Error:</ansired>"), HTML(f"<ansigreen>{response.text}</ansigreen>"), style=style)

def generate_text(question, url):
    payload = {
        "text": question
    }
 
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print_formatted_text(HTML("<ansired>B-chat:</ansired>"), style=style)
        # Print response character by character
        for char in response.text:
            print_formatted_text(char, end='', style=style)
            sleep(0.05)
    else:
        print_formatted_text(HTML("<ansired>Error:</ansired>"), HTML(f"<ansigreen>{response.text}</ansigreen>"), style=style)


def main():
    print_formatted_text(HTML("<ansiblue>Welcome to Text Generation Interface!</ansiblue>"), style=style)
    print_formatted_text(HTML("<ansiblue>Enter your question or type 'quit' to exit.</ansiblue>"), style=style)

    parser = argparse.ArgumentParser(description='Text Generation Interface')
    parser.add_argument('--url', type=str, default='http://10.101.15.171:8002/text-generation',
                        help='URL for text generation service')

    args = parser.parse_args()

    history = InMemoryHistory()

    while True:
        question = prompt("\nPrompt: ", style=style, history=history)

        if question.lower() == 'quit':
            print("Goodbye!")
            break

        generate_text(question, args.url)

if __name__ == "__main__":
    main()
