import os
import getpass
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables (for GOOGLE_API_KEY)
load_dotenv()

# Ensure GOOGLE_API_KEY is set
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API Key: ")

# Initialize the Gemini Flash 2.0 model

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=1.2) 

def generate_social_media_post(topic: str, platform: str, tone: str, cta: str = "", include_emojis: bool = True, include_hashtags: bool = True) -> str:


    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"You are an expert social media manager. Generate a concise and engaging {platform} post."),
        ("user", f"""
        Generate a social media post for {platform} about: "{topic}".
        The tone should be: {tone}.
        {"Include a call to action: " + cta if cta else ""}
        {"Include relevant emojis." if include_emojis else "Do not include emojis."}
        {"Include 3-5 relevant hashtags." if include_hashtags else "Do not include hashtags."}

        Consider {platform} specific conventions:
        - Twitter: Max 280 characters, concise.
        - Instagram: Focus on visuals, strong hashtags, engaging caption.
        - LinkedIn: Professional, insightful, career-focused.
        """)
    ])

    chain = prompt_template | llm | StrOutputParser()

    try:
        response = chain.invoke({
            "topic": topic,
            "platform": platform,
            "tone": tone,
            "cta": cta,
            "include_emojis": include_emojis,
            "include_hashtags": include_hashtags
        })
        return response
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print("--- Social Media Post Generator ---")

    while True:
        user_topic = input("Enter the topic for your post (e.g., 'new AI features', 'summer sale', 'mental health awareness'): ")
        if not user_topic:
            print("Topic cannot be empty. Please enter a topic.")
            continue

        user_platform = input("Choose a platform (Twitter, Instagram, LinkedIn, Facebook): ").strip().title()
        if user_platform not in ["Twitter", "Instagram", "LinkedIn", "Facebook"]:
            print("Invalid platform. Please choose from Twitter, Instagram, LinkedIn, or Facebook.")
            continue

        user_tone = input("Choose a tone (professional, casual, humorous, informative, promotional): ").strip().lower()
        if user_tone not in ["professional", "casual", "humorous", "informative", "promotional"]:
            print("Invalid tone. Please choose from professional, casual, humorous, informative, or promotional.")
            continue

        user_cta = input("Enter a call to action (optional, e.g., 'Visit our website!', 'Learn more'): ").strip()

        user_emojis = input("Include emojis? (yes/no): ").strip().lower() == 'yes'
        user_hashtags = input("Include hashtags? (yes/no): ").strip().lower() == 'yes'

        print(f"\nGenerating {user_platform} post for '{user_topic}' with '{user_tone}' tone...")
        post = generate_social_media_post(
            topic=user_topic,
            platform=user_platform,
            tone=user_tone,
            cta=user_cta,
            include_emojis=user_emojis,
            include_hashtags=user_hashtags
        )
        print("\n--- Generated Post ---")
        print(post)
        print("----------------------\n")

        another = input("Generate another post? (yes/no): ").strip().lower()
        if another != 'yes':
            break

    print("Thank you for using the Social Media Post Generator!")