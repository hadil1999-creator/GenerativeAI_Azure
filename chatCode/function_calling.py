import openai
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv()


# Set OpenAI API credentials and configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_base = os.getenv("OPENAI_API_BASE")


deployment_name = "beginner"


#the function that will call the Microsoft Learn API to get a list of courses
def search_courses(role, product, level):
  url = "https://learn.microsoft.com/api/catalog/"
  params = {
     "role": role,
     "product": product,
     "level": level
  }
  response = requests.get(url, params=params)
  modules = response.json()["modules"]
  results = []
  for module in modules[:5]:
     title = module["title"]
     url = module["url"]
     results.append({"title": title, "url": url})
  return str(results)


#we define the function - we may define many functions  
functions = [
   {
      "name":"search_courses",
      "description":"Retrieves courses from the search index based on the parameters provided",
      "parameters":{
         "type":"object",
         "properties":{
            "role":{
               "type":"string",
               "description":"The role of the learner (i.e. developer, data scientist, student, etc.)"
            },
            "product":{
               "type":"string",
               "description":"The product that the lesson is covering (i.e. Azure, Power BI, etc.)"
            },
            "level":{
               "type":"string",
               "description":"The level of experience the learner has prior to taking the course (i.e. beginner, intermediate, advanced)"
            }
         },
         "required":[
            "role"
         ]
      }
   }
]

response = openai.ChatCompletion.create(
engine=deployment_name,
messages= [ {"role": "user", "content": "Find me a good course for a beginner student to learn Azure."} ],
                                        functions=functions,
                                        function_call="auto")

response_message = response.choices[0].message



# Check if the model wants to call a function
if response_message.function_call.name:
 print("Recommended Function call:")
 print(response_message.function_call.name)

 # Call the function.
 function_name = response_message.function_call.name

 available_functions = {
         "search_courses": search_courses,
 }
 function_to_call = available_functions[function_name]

 function_args = json.loads(response_message.function_call.arguments)
 function_response = function_to_call(**function_args)

 print("Output of function call:")
 print(function_response)
 print(type(function_response))


 # Add the assistant response and function response to the messages
 response_message.append( # adding assistant response to messages
     {
         "role": response_message.role,
         "function_call": {
             "name": function_name,
             "arguments": response_message.function_call.arguments,
         },
         "content": None
     }
 )
 response_message.append( # adding function response to messages
     {
         "role": "function",
         "name": function_name,
         "content":function_response,
     }
 )
 
 function_to_call = available_functions[function_name]

function_args = json.loads(response_message.function_call.arguments)
function_response = function_to_call(**function_args)
"""
student_1_description="Emily Johnson is a sophomore majoring in computer science at Duke University. She has a 3.7 GPA. Emily is an active member of the university's Chess Club and Debate Team. She hopes to pursue a career in software engineering after graduating."

student_2_description = "Michael Lee is a sophomore majoring in computer science at Stanford University. He has a 3.8 GPA. Michael is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after finishing his studies."
prompt1 = f'''
Please extract the following information from the given text and return it as a JSON object:

name
major
school
grades
club

This is the body of text to extract the information from:
{student_1_description}
'''

prompt2 = f'''
Please extract the following information from the given text and return it as a JSON object:

name
major
school
grades
club

This is the body of text to extract the information from:
{student_2_description}
'''

# response from prompt one
openai_response1 = openai.ChatCompletion.create(
engine=deployment_name,
messages = [{'role': 'user', 'content': prompt1}]
)
openai_response1.choices[0].message.content

# response from prompt two
openai_response2 = openai.ChatCompletion.create(
engine=deployment_name,
messages = [{'role': 'user', 'content': prompt2}]
)
openai_response2.choices[0].message.content

# Loading the response as a JSON object
json_response1 = json.loads(openai_response1.choices[0].message.content)
print(json_response1)
json_response2 = json.loads(openai_response2.choices[0].message.content)
print(json_response2)

"""