import getpass
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.messages import HumanMessage,AIMessage
from langchain.chat_models import init_chat_model
import json 
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field 

# Load environment variables 
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# Define JSON output structure 
class SocialMediaAd(BaseModel):
    headline: str = Field(description="A catchy headline for the social media ad")
    text: str = Field(description="The main body text of the social media ad")
    call_to_action: str = Field(description="The call to action phrase for the ad")
    emojis: list[str] = Field(description="A list of relevant emojis for the ad")
    hashtags: list[str] = Field(description="A list of relevant hashtags for the ad")


# Set up LLM settings
llm_settings = { "temperature": 0.7, "max_output_tokens": 512, "top_k": 40,  "top_p": 0.95 }

# Initialize the chat model
model = init_chat_model (
  "gemini-2.0-flash",
  model_provider="google_genai",
  temperature=llm_settings["temperature"],
  max_output_tokens=llm_settings["max_output_tokens"]
)

parser = JsonOutputParser(pydantic_object=SocialMediaAd)

# Load examples (Few shot prompting)
EXAMPLES_FILE = "examples.json" 
try:
    with open(EXAMPLES_FILE, 'r', encoding='utf-8') as f:
        examples = json.load(f)
    print(f"DEBUG: Successfully loaded few-shot examples from {EXAMPLES_FILE}")
except FileNotFoundError:
    print(f"ERROR: Examples file '{EXAMPLES_FILE}' not found. Please create it.")
    exit()
except json.JSONDecodeError as e:
    print(f"ERROR: Could not parse examples from '{EXAMPLES_FILE}': {e}")
    print("Please ensure your examples JSON file is valid.")
    exit()
except Exception as e:
    print(f"ERROR: An unexpected error occurred while loading examples: {e}")
    exit()

example_formatter_template = ChatPromptTemplate.from_messages(
    [
        HumanMessage(content="Generate a catchy ad based on the provided specifications:\n"
                            "- Context: '{context}'\n"
                            "- Platform: '{platform}'\n"
                            "- Audience: '{audience}'\n"
                            "- Tone: '{tone}'\n"
                            "- Call to Action: '{cta}'\n"
                            "- Include Emojis: {include_emojis}\n"
                            "- Include Hashtags: {include_hashtags}\n"
                            "- Word Limit: {word_limit} words."),
        AIMessage(content="{ad_output_json}"),
    ]
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_formatter_template,
    examples=examples,
    input_variables=["context", "platform", "audience", "tone", "cta", "include_emojis", "include_hashtags", "word_limit"],
)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a highly creative and engaging social media ad generator. Your output MUST be in JSON format. Always use relevant emojis and hashtags."),
    few_shot_prompt,
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
print("Example: {\"context\": \"new coffee shop\", \"platform\": \"Instagram\", \"audience\": \"young adults\", \"tone\": \"exciting\", \"cta\": \"Visit us!\", \"include_emojis\": true, \"include_hashtags\": true, \"word_limit\": 50}")
json_input_string = input("JSON Input: ")
json_input_string = input()

input_data = json.loads(json_input_string)

input_data["format_instructions"] = parser.get_format_instructions()

print("\n--- Generating Ad ---")

# Invoke the model
ad_output_json = chain.invoke(input_data)

print("\n--- Generated Ad Output (JSON) ---")
print(json.dumps(ad_output_json, indent=2, ensure_ascii=False)) 
print("-----------------------------------\n")
