import streamlit as st
from ad_chain import generate_ad, load_api_key
import json

load_api_key()

# # Remove padding using custom CSS
# st.markdown("""
#     <style>
#         .block-container {
#             padding-top: 1rem;
#             padding-bottom: 1rem;
#             padding-left: 0rem;
#             padding-right: 0rem;
#         }
#     </style>
# """, unsafe_allow_html=True)

st.title("AdCraft AI")
st.text("Generate engaging social media ads for your company instantly",)

inp_col, out_col = st.columns([1,1])

with inp_col:

    with st.form("ad form"):
        
        product_name = st.text_input("Product Name")
        product_description = st.text_area("Product Description")
        platform = st.selectbox("Platform", ["Instagram", "Facebook", "Twitter", "LinkedIn"], index=None)
        audience = st.text_input("Target Audience")
        tone = st.text_input("Tone", value="exciting")
        cta = st.text_input("Call to Action")
        contact_details = st.text_input("Contact Details (Phone/Email)")
        location = st.text_input("Location")
        campaign_goal = st.text_input("Campaign Goal", value="Increase brand awareness")
        desired_emotion = st.text_input("Desired Emotion", value="Exciting, Friendly")
        keywords = st.text_input("Keywords (comma-separated)")
        include_emojis = st.checkbox("Include Emojis", value=True)
        include_hashtags = st.checkbox("Include Hashtags", value=True)
        word_limit = st.slider("Word Limit", min_value=20, max_value=200, value=50)
        
        temperature = st.slider("Creativity ", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

        submitted = st.form_submit_button("Generate Ad")
        
if submitted:
    
    try:
        keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
        input_data = {
            "context": "Social Media Ad",
            "platform": platform,
            "audience": audience,
            "contact_details": contact_details,
            "tone": tone,
            "cta": cta,
            "include_emojis": include_emojis,
            "include_hashtags": include_hashtags,
            "word_limit": word_limit,
            "product_name": product_name,
            "product_description": product_description,
            "location": location,
            "campaign_goal": campaign_goal,
            "desired_emotion": desired_emotion,
            "keywords_to_include": keywords_list,
        }
        
        
        with out_col:
            
            with st.spinner("Generating..."):
                ad = generate_ad(input_data,temperature)

            st.success("Here's your ad!")
            st.markdown(f"### 📌 {ad.get('headline', '')}")
            st.write(ad.get("text", ""))
            st.markdown(f"**🛎️ Call to Action:** {ad.get('call_to_action', '')}")
            st.markdown(f"**📍 Location:** {ad.get('location', '')}")
            st.markdown(f"**📞 Contact:** {ad.get('contact_details', '')}")
            st.markdown(f"**🌈 Emojis:** {' '.join(ad.get('emojis', []))}")
            st.markdown(f"**🏷️ Hashtags:** {' '.join(ad.get('hashtags', []))}")
            
    except Exception as e:
        st.error(f"Something went wrong: {e}")
