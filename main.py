# Import necessary libraries
import getpass
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model

# Load environment variables (for GOOGLE_API_KEY)
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# Set up the LLM settings
llm_settings = { "temperature": 0.7, "max_output_tokens": 512, "top_k": 40,  "top_p": 0.95 }


# Initialize the chat model
model = init_chat_model (
  "gemini-2.0-flash",  
  model_provider="google_genai", 
  temperature=llm_settings["temperature"],
  max_output_tokens=llm_settings["max_output_tokens"]
)

# Define the system and user prompts
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a highly creative and engaging social media ad generator."),
    ("human", """
    Generate a catchy ad based on the provided context: '{context}' 
    for the platform: '{platform}'. 
    The ad should be engaging and tailored for the target audience: '{audience}'. 
    Keep the tone {tone}.
    Include a call to action: '{cta}'. 
    Include emojis: {include_emojis}. 
    Include hashtags: {include_hashtags}.
    Keep the word limit: {word_limit}.
    """)
])

# message = chat_prompt.format(
#     context="new coffee shop opening in town",
#     platform="Instagram",
#     audience="young adults",
#     tone="exciting",
#     cta="Visit us today!",
#     include_emojis=True,
#     include_hashtags=True,
#     word_limit=50
# )

# Take input from user for each parameter
context = input("Enter the ad context: ")
platform = input("Enter the platform: ")
audience = input("Enter the target audience: ")
tone = input("Enter the tone: ")
cta = input("Enter the call to action: ")
include_emojis = input("Include emojis? (Yes/No): ").strip().lower() == "yes"
include_hashtags = input("Include hashtags? (Yes/No): ").strip().lower() == "yes"
word_limit = int(input("Enter the word limit: "))

# Update messages with user input
message = chat_prompt.format(
  context=context,
  platform=platform,
  audience=audience,
  tone=tone,
  cta=cta,
  include_emojis=include_emojis,
  include_hashtags=include_hashtags,
  word_limit=word_limit
)

# Invoke the model 
print(model.invoke(message).content)




