import openai
import os
from dotenv import load_dotenv

load_dotenv()

"""
openai.api_key = "acdf4d4554ea413f9863311aafd77de0"
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview'  # Adjust this to the correct version if necessary
openai.api_base = "https://challenge1.openai.azure.com/"
deployment_name = "beginner"
"""

# Set OpenAI API credentials and configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_base = os.getenv("OPENAI_API_BASE")


deployment_name = "beginner"

expertise_domain = input("Domain in expertise:")



# interpolate the number of recipes into the prompt an ingredients
prompt = f"You're an expert on {expertise_domain}. Suggest a beginner lesson for {expertise_domain} in the following format: Format:- concepts:- brief explanation of the lesson:- exercise in code with solutions"
# Make the completion request using the deployment name as the engine
completion = openai.ChatCompletion.create(
    engine=deployment_name,  # Use the deployment name here
    messages=[{"role": "user", "content": prompt}],max_tokens=1200 , temperature = 0.9# You can adjust the number of tokens as needed
)

# Print the response
print(completion.choices[0].message.content)