import os
import json
import getpass
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Pydantic model definition
# Stucture of generated output
class SocialMediaAd(BaseModel):
    headline: str = Field(description="A catchy headline for the social media ad")
    text: str = Field(description="The main body text of the social media ad")
    call_to_action: str = Field(description="The call to action phrase for the ad")
    emojis: list[str] = Field(description="A list of relevant emojis for the ad")
    hashtags: list[str] = Field(description="A list of relevant hashtags for the ad")
    location: str = Field(description="The geographical location relevant to the ad, e.g., 'Downtown Main Street', 'Online'")
    contact_details: str= Field(description="The contact details of company publishing the ad.")

# Load API Key
def load_api_key():
    load_dotenv()       # Load api from .env
    if not os.environ.get("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# Load examples (few shots)
def load_few_shot_examples(file_path="examples.json"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            examples = json.load(f)
        print(f"DEBUG: Successfully loaded few-shot examples from {file_path}")
        return examples
    except FileNotFoundError:
        print(f"ERROR: Examples file '{file_path}' not found. Please create it.")
        exit()
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse examples from '{file_path}': {e}")
        print("Please ensure your examples JSON file is valid.")
        exit()
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while loading examples: {e}")
        exit()

# Get and process user input
def get_user_ad_specs():
    print("Enter your ad specifications as a JSON string. Include as much detail as possible for a better ad.")
    print("Example: {\"context\": \"new coffee shop\", \"platform\": \"Instagram\", \"audience\": "
          "\"young adults\", \"location\": \"Street-1\", \"contact_details\": \"9999999999\", \"tone\": \"exciting\","
          "\"cta\": \"Visit us!\", \"include_emojis\": true, \"include_hashtags\": true, \"word_limit\": 50,"
          "\"product_name\": \"Daily Grind Coffee\", \"product_description\": \"A cozy new coffee shop serving artisanal blends and pastries.\","
          "\"location\": \"Downtown Main Street\", \"campaign_goal\": \"Increase foot traffic and brand awareness.\","
          "\"desired_emotion\": \"Cozy and inviting.\", \"keywords_to_include\": \"fresh, local, community\"}")
    json_input_string = input("JSON Input: ")

    try:
        input_data = json.loads(json_input_string)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input provided. Please ensure your input is a valid JSON string. Details: {e}")
        exit()

    input_data["keywords_to_include"] = [kw.strip() for kw in input_data.get("keywords_to_include", "").split(',') if kw.strip()]
    # Convert keywords to list
    
    return input_data

# Initialize LLM and Chain
def setup_llm_chain(examples, parser):
    
    llm_settings = { "temperature": 0.7, "max_output_tokens": 512, "top_k": 40,  "top_p": 0.95 }
    model = ChatGoogleGenerativeAI (
      model="gemini-2.0-flash",
      temperature=llm_settings["temperature"],
      max_output_tokens=llm_settings["max_output_tokens"]
    )

    # Template for each example
    example_formatter_template = ChatPromptTemplate.from_messages(
        [
            HumanMessage(content="Generate a catchy ad based on the provided specifications:\n"
                                "- Context: '{context}'\n"
                                "- Platform: '{platform}'\n"
                                "- Audience: '{audience}'\n"
                                "- Contact details: '{contact_details}'\n"
                                "- Tone: '{tone}'\n"
                                "- Call to Action: '{cta}'\n"
                                "- Include Emojis: {include_emojis}\n"
                                "- Include Hashtags: {include_hashtags}\n"
                                "- Word Limit: {word_limit} words.\n"
                                "- Product Name: '{product_name}'\n"
                                "- Product Description: '{product_description}'\n"
                                "- Location: '{location}'\n"
                                "- Campaign Goal: '{campaign_goal}'\n"
                                "- Desired Emotion: '{desired_emotion}'\n"
                                "- Keywords to Include: '{keywords_to_include}'"), 
            AIMessage(content="{ad_output_json}"),
        ]
    )

    # Plug in few shot examples
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_formatter_template,
        examples=examples,
        input_variables=[
            "context", "platform", "audience", "contact_details", "tone", "cta",
            "include_emojis", "include_hashtags", "word_limit",
            "product_name", "product_description", "location",
            "campaign_goal", "desired_emotion", "keywords_to_include" 
        ],
    )

    # Main chat prompt template
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a highly creative and engaging social media ad generator. "
         "Your output MUST be in JSON format."
         "Always use relevant emojis and hashtags. "
         "Pay close attention to all provided specifications, including product details, "
         "campaign goals, and emotional tone. Adhere strictly to character limits for headline and text if provided."),
        few_shot_prompt,
        ("human", """
        Generate a catchy ad based on the provided specifications.
        The output should be a JSON object with the following keys:
        - `headline`: A catchy headline for the ad.
        - `text`: The main body text of the ad.
        - `call_to_action`: The call to action phrase (e.g., "Shop Now!", "Learn More").
        - `emojis`: An array of emojis to be used.
        - `hashtags`: An array of hashtags to be used.
        - `location`: The geographical location relevant to the ad.
        - `contact details`: The contact details of company publishing the ad.
        {format_instructions}
        """)
    ])
    
    # Return full chain
    return chat_prompt | model | parser

# Ad Output formatting
def print_ad(ad_output_json):
    print(ad_output_json)
    print("\n--- Generated Social Media Ad ---")
    formatted_output = f"""
     ✨ Social Media Ad ✨

    Headline: {ad_output_json.get('headline', 'N/A')}
    Text: {ad_output_json.get('text', 'N/A')}
    Call to Action: {ad_output_json.get('call_to_action', 'N/A')}
    Emojis: {' '.join(ad_output_json.get('emojis', []))}
    Hashtags: {' '.join(ad_output_json.get('hashtags', []))}
    Location: {ad_output_json.get('location', 'N/A')}
    """
    print(formatted_output)

# Main execution block
if __name__ == "__main__":
    load_api_key()

    examples = load_few_shot_examples()

    parser = JsonOutputParser(pydantic_object=SocialMediaAd)

    chain = setup_llm_chain(examples, parser)

    input_data = get_user_ad_specs()

    input_data["format_instructions"] = parser.get_format_instructions()

    try:
        ad_output_json = chain.invoke(input_data)
        print_ad(ad_output_json)
        
    except Exception as e: 
        print(f"An error occurred during LLM invocation: {e}")
