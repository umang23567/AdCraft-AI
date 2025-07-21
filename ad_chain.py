import json
from dotenv import load_dotenv
import streamlit as st

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
# from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


# Pydantic model definition
class SocialMediaAd(BaseModel):
    company_name: str = Field(description="Name of company/brand publishing the ad")
    headline: str = Field(description="Catchy headline of the ad")
    text: str = Field(description="Main text body of the ad")
    call_to_action: str = Field(description="Call to action phrase of the ad")
    hashtags: list[str] = Field(description="List of relevant hashtags for the ad")
    location: str = Field(description="Geographical location of company/brand publishing the ad")
    phone: str= Field(description="Phone number of the company/brand publishing the ad")
    email: str= Field(description="Email of the company/brand publishing the ad")
    website: str= Field(description="Website of the company/brand publishing the ad")

# # Load API Key
# def load_api_key():
#     load_dotenv()       # Load api from .env
#     if not os.environ.get("GOOGLE_API_KEY"):
#         os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# Load examples (few shots)
def load_few_shot_examples(file_path="examples.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        examples = json.load(f)
    return examples


# Initialize LLM and Chain
def setup_llm_chain(temp=0.7):   
    
    examples = load_few_shot_examples()
    parser = JsonOutputParser(pydantic_object=SocialMediaAd)
    
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
            "- Name of company/brand: {company_name} \n"
            "- Product name: {product_name}\n"
            "- Product description: {product_description}\n"
            "- Platform for the ad: {platform}\n"
            "- Target audience: {audience}\n"
            "- Tone of the ad: {tone}\n"
            "- Call to action of the ad: {cta}\n"
            "- Phone number of company for contact: {phone}\n"
            "- Email of company for contact: {email}\n"
            "- Website link of company: {website}\n"
            "- Location: {location}\n"
            "- Campaign Goal: {campaign_goal}\n"
            "- Keywords to Include: {keywords_to_include}\n"
            "- Word Limit of text: {word_limit} words\n"
            "- Include hashtags: {include_hashtags}\n\n"),
            
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
                "Also use relevant emojis wherever needed. "
                "Pay close attention to all provided specifications. Do not change any important information given. "
                "Use proper punctuations. "
                "If any field is empty, do not guess and leave the corresponding output field empty or skip non-essential text related to it. "
                "You can correct the punctuations and spellings of the user input."
                "The hashtags if generated should be exciting and appeal to the viewers. Generate maximum 3 hashtags."
                "Limit the headline to a maximum of 25 characters, including spaces and punctuation."
                "Use the given keywords to include."
                "Ensure the main body text is as close as possible to the given word limit."
                "There are few examples that you can consider before generating the output. "),

        
        few_shot_prompt,
        
        
        ("human", 
        "Generate a catchy ad based on the provided specifications:\n"
        "- Name of company/brand: {company_name}\n"
        "- Product name: {product_name}\n"
        "- Product description: {product_description}\n"
        "- Platform for the ad: {platform}\n"
        "- Target audience: {audience}\n"
        "- Tone of the ad: {tone}\n"
        "- Call to action of the ad: {cta}\n"
        "- Phone number of company for contact: {phone}\n"
        "- Email of company for contact: {email}\n"
        "- Website link of company: {website}\n"
        "- Location: {location}\n"
        "- Campaign Goal: {campaign_goal}\n"
        "- Keywords to Include: {keywords_to_include}\n"
        "- Word Limit of text: {word_limit} words\n"
        "- Include hashtags: {include_hashtags}\n\n"

        "The output should be a JSON object with the following keys:\n"
        # "The output should be 2 JSON object options with the following keys: \n"
        "- `company_name`: A catchy headline for the ad.\n"
        "- `headline`: A catchy headline for the ad.\n"
        "- `text`: The main body text of the ad.\n"
        "- `call_to_action`: The call to action phrase.\n"
        "- `hashtags`: An array of hashtags to be used.\n"
        "- `location`: Location of the company.\n"
        "- `phone`: Phone number of the company.\n"
        "- `email`: Email of the company.\n"
        "- `website`: Website of the company.\n"

        "{format_instructions}"
        ),
    ])

    # print(chat_prompt)
    
    # Return full chain
    return chat_prompt | model | parser

def generate_ad(input_data, temp):

    parser = JsonOutputParser(pydantic_object=SocialMediaAd)
    
    chain = setup_llm_chain(temp)
    
    input_data["format_instructions"] = parser.get_format_instructions()

    # print("Input:")
    # print(input_data)
    
    result = chain.invoke(input_data)
    
    # print("Result:")
    # print(result)
    
    return result


