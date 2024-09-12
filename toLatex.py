import base64
import requests

def toLatex(image_path, output_file, api_key):
    # Function to encode the image to base64
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string of the image
    base64_image = encode_image(image_path)

    # Define headers for API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Payload with image in Base64 and request for LaTeX code
    payload = {
        "model": "gpt-4o-2024-08-06",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please generate the LaTeX code for this image. Don't say anything else. Please give it as plain text"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # Send the request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Extracting the LaTeX code from the response
        latex_code = response.json()['choices'][0]['message']['content']

        # Saving the LaTeX code to a text file
        with open(output_file, 'w') as file:
            file.write(latex_code)

        # Print a success message
        print(f"LaTeX code has been saved to '{output_file}'")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Example usage:
api_key = "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"
image_path = '/Users/arav/latexconvert/pythonProject/Screenshot 2024-09-12 at 4.42.01 PM.png'
output_file = 'latex_output.txt'

# Call the function
toLatex(image_path, output_file, api_key)
