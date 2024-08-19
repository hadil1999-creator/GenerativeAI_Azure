import openai
import os
from dotenv import load_dotenv

load_dotenv()


# Set OpenAI API credentials and configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_base = os.getenv("OPENAI_API_BASE")


deployment_name = "beginner"

# Create your first prompt
text_prompt = "Product description: A home milkshake maker\nSeed words: fast, healthy, compact.\nProduct names: HomeShaker, Fit Shaker, QuickShake, Shake Maker\n\nProduct description: A pair of shoes that can fit any foot size.\nSeed words: adaptable, fit, omni-fit."


response = openai.ChatCompletion.create(
    engine=deployment_name,  # Use the deployment name here
     messages = [{"role":"system", "content":"You are a helpful assistant."},
               {"role":"user","content":text_prompt},])

print(response.choices[0].message.content)