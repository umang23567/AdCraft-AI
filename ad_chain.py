import os
import json
import getpass
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
# from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# from functools import lru_cache


# Pydantic model definition
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
# @lru_cache(maxsize=1)
def load_few_shot_examples(file_path="examples.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        examples = json.load(f)
    return examples

# Get parser
# @lru_cache(maxsize=1)
def get_parser():
    return JsonOutputParser(pydantic_object=SocialMediaAd)


# Initialize LLM and Chain
def setup_llm_chain(temp=0.7):   
    
    examples = load_few_shot_examples()
    parser = get_parser()
    
    llm_settings = { "temperature": temp, "max_output_tokens": 512, "top_k": 40,  "top_p": 0.95 }
    
    model = ChatGoogleGenerativeAI (
      model="gemini-2.0-flash",
      temperature=llm_settings["temperature"],
      max_output_tokens=llm_settings["max_output_tokens"]
    )

    # Template for each example
    example_formatter_template = ChatPromptTemplate.from_messages(
        [
            ("human",
            "Generate a catchy ad based on the provided specifications:\n"
            "- Product for which the ad is created: '{product_name}'\n"
            "- Product description: '{product_description}'\n"
            "- Platform for the ad: '{platform}'\n"
            "- Target audience: '{audience}'\n"
            "- Tone of the ad: '{tone}'\n"
            "- Call to action of the ad: '{cta}'\n"
            "- Contact details: {contact_details}\n"
            "- Location: {location}\n"
            "- Campaign Goal: '{campaign_goal}'\n"
            "- Desired Emotion: '{desired_emotion}'\n"
            "- Keywords to Include: '{keywords_to_include}'\n"
            "- Word Limit: {word_limit} words\n"
            "- Include emojis: {include_emojis}\n"
            "- Include hashtags: {include_hashtags}"),
            
            ("ai", "{ad_output_json}"),
        ]
    )

    # Plug in few shot examples
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_formatter_template,
        examples=examples,
    )

    # Main chat prompt template

    chat_prompt = ChatPromptTemplate.from_messages([
        
        
        ("system", "You are a highly creative and engaging social media ad generator. "
                "Your output MUST be in JSON format. "
                "Always use relevant emojis and hashtags. "
                "Pay close attention to all provided specifications. "
                "Use proper punctuations."
                "There are few examples that you can consider before generating the output"),
        
        few_shot_prompt,
        
        ("human", 
        "Generate a catchy ad based on the provided specifications:\n"
        "- Product for which the ad is created: {product_name}\n"
        "- Product description: {product_description}\n"
        "- Platform for the ad: {platform}\n"
        "- Target audience: {audience}\n"
        "- Tone of the ad: {tone}\n"
        "- Call to action of the ad: {cta}\n"
        "- Contact details: {contact_details}\n"
        "- Location: {location}\n"
        "- Campaign Goal: {campaign_goal}\n"
        "- Desired Emotion: {desired_emotion}\n"
        "- Keywords to Include: {keywords_to_include}\n"
        "- Word Limit: {word_limit} words\n"
        "- Include emojis: {include_emojis}\n"
        "- Include hashtags: {include_hashtags}\n\n"


        # "The output should be a JSON object with the following keys:\n"
        "The output should be 2 JSON object options with the following keys: \n"
        "- `headline`: A catchy headline for the ad.\n"
        "- `text`: The main body text of the ad.\n"
        "- `call_to_action`: The call to action phrase (e.g., \"Shop Now!\", \"Learn More\").\n"
        "- `emojis`: An array of emojis to be used.\n"
        "- `hashtags`: An array of hashtags to be used.\n"
        "- `location`: The geographical location relevant to the ad.\n"
        "- `contact_details`: The contact details of the company publishing the ad.\n"
        "{format_instructions}"
        ),
    ])

    # print(chat_prompt)
    
    # Return full chain
    return chat_prompt | model | parser

def generate_ad(input_data, temp):

    parser = get_parser()
    
    chain = setup_llm_chain(temp)
    
    input_data["format_instructions"] = parser.get_format_instructions()

    # print("Input: \n")
    # print(input_data)
    
    result = chain.invoke(input_data)
    
    print("Result: \n")
    print(result)
    
    return result


