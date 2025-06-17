import getpass
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
import json 
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field 

# Load environment variables (for GOOGLE_API_KEY)
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# Define the expected JSON output structure using Pydantic
class SocialMediaAd(BaseModel):
    headline: str = Field(description="A catchy headline for the social media ad")
    text: str = Field(description="The main body text of the social media ad")
    call_to_action: str = Field(description="The call to action phrase for the ad")
    emojis: list[str] = Field(description="A list of relevant emojis for the ad")
    hashtags: list[str] = Field(description="A list of relevant hashtags for the ad")


# Set up the LLM settings
llm_settings = { "temperature": 0.7, "max_output_tokens": 512, "top_k": 40,  "top_p": 0.95 }

# Initialize the chat model
model = init_chat_model (
  "gemini-2.0-flash",
  model_provider="google_genai",
  temperature=llm_settings["temperature"],
  max_output_tokens=llm_settings["max_output_tokens"]
)

parser = JsonOutputParser(pydantic_object=SocialMediaAd)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a highly creative and engaging social media ad generator. Your output MUST be in JSON format. Always use relevant emojis and hashtags."),
    ("human", """
    Generate a catchy ad based on the provided specifications.
    The output should be a JSON object with the following keys:
    - `headline`: A catchy headline for the ad.
    - `text`: The main body text of the ad.
    - `call_to_action`: The call to action phrase (e.g., "Shop Now!", "Learn More").
    - `emojis`: An array of emojis to be used.
    - `hashtags`: An array of hashtags to be used.
    {format_instructions}
    """)
])

chain = chat_prompt | model | parser

print("Enter your ad specifications as a JSON string:")
# print("Example: {\"context\": \"new coffee shop\", \"platform\": \"Instagram\", \"audience\": \"young adults\", \"tone\": \"exciting\", \"cta\": \"Visit us!\", \"include_emojis\": true, \"include_hashtags\": true, \"word_limit\": 50}")
# json_input_string = input("JSON Input: ")
json_input_string = input()


input_data = json.loads(json_input_string)

input_data["format_instructions"] = parser.get_format_instructions()


# print("\n--- Generating Ad ---")

ad_output_json = chain.invoke(input_data)


# print("\n--- Generated Ad Output (JSON) ---")
print(json.dumps(ad_output_json, indent=2, ensure_ascii=False)) 
print("-----------------------------------\n")
