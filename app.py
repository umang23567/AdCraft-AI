import streamlit as st
from streamlit_tags import st_tags

from ad_chain import generate_ad
from image_gen import overlay_txt, gen_grad_bg, gen_solid_bg, process_bg

import io

import hashlib
import io
import json

api_key = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = api_key

st.set_page_config(layout="wide")

# Custom CSS to control padding (balanced – not too tight, not too wide)
st.markdown("""
    <style>
    .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    /* Remove default Streamlit padding at top */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Custom title styling */
    .centered-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0rem;
        font-family: 'Segoe UI', sans-serif;
        color:  "#000000";
    }

    /* Custom subtitle styling */
    .centered-subtitle {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 400;
        margin-top: 0;
        margin-bottom: 2rem;
        font-family: 'Segoe UI', sans-serif;
        color: "#000000";
    }
    </style>
""", unsafe_allow_html=True)



st.markdown('<div class="centered-title">AdCraft AI</div>', unsafe_allow_html=True)
st.markdown('<div class="centered-subtitle">Generate engaging social media ads instantly!</div>', unsafe_allow_html=True)


inp_col1, inp_col2 , space1, styling_col, space2, out_col = st.columns([0.8,0.8,0.05,0.4,0.05,1.5])


with inp_col1:
    
    # st.markdown("Required Ad Details")
        
    company_name = st.text_input("\* Company/Brand Name")
    product_name = st.text_input("\* Product Name")
    product_description = st.text_area("\* Product Description")
    platform = st.selectbox("\* Platform", ["Instagram", "Facebook", "Twitter", "LinkedIn"], index=None)
    cta = st.text_input("\* Call to Action")
    
        
    with st.expander("Additional details", expanded=False):
        
        audience = st.text_input("Target Audience", value="Everyone")
        tone = st.text_input("Tone/Style", value="Exciting")
        
        campaign_goal = st.text_input("Campaign Goal", value="Increase awareness")
        keywords = st_tags(
            label="Enter keywords to include",
            text="Press enter to add more",
            value=[],
            suggestions=[],
            maxtags=10,
            key="1",
        )
        
        
        
        
    
with inp_col2:
        
    # st.markdown("Additional Ad Details")
        
    phone = st.text_input("\* Phone number")
    email = st.text_input("\* Email")
    website = st.text_input("\* Website link")
    location = st.text_input("\* Location")
    
    word_limit = st.slider("Word Limit", min_value=50, max_value=75, value=50)
    temperature = st.slider("Creativity ", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    include_hashtags = st.checkbox("Include Hashtags", value=True)
    
    submitted=st.button("Generate Ad")
           
    
input_data = {
    "company_name": company_name,
    "product_name": product_name,
    "product_description": product_description,
    "platform": platform,
    "audience": audience or "Everyone",
    "tone": tone or "Exciting",
    "cta": cta,
    
    "phone": phone or "",
    "email": email or "",
    "website": website or "",
    "location": location or "",
    
    "campaign_goal": campaign_goal or "Increase awareness",
    "keywords_to_include": keywords or "",
    "word_limit": word_limit,
    "include_hashtags": include_hashtags,
}

form_hash = hashlib.md5(json.dumps({**input_data,"temperature": temperature}, sort_keys=True).encode()).hexdigest()

if "form_hash" in st.session_state and st.session_state.form_hash != form_hash:
    keys_to_reset = ["generated_ad", "ad_image", "restyle_trigger", "restyle", "missing_bg_warning"]
    for key in keys_to_reset:
        st.session_state.pop(key, None)

    
    
st.session_state.form_hash = form_hash


with styling_col:
    
    st.text("Styling Options")
    
    text_font = st.selectbox("Text Font", [ "Arial", "Georgia", "Montserrat","Pacifico","Anton"], key="txt_font")
    font_dict = {
        "Arial": "fonts/OpenSans-VariableFont_wdth,wght.ttf",
        "Georgia": "fonts/LibreBaskerville-Regular.ttf",
        "Montserrat": "fonts/Montserrat-Italic-VariableFont_wght.ttf",
        "Pacifico": "fonts/Pacifico-Regular.ttf",
        "Anton": "fonts/Anton-Regular.ttf"
    }
    Font = font_dict[text_font]
    
    text_color = st.color_picker("Font Color", "#000000")  
    
    bg_style = st.selectbox("Background Style", ["Solid", "Gradient", "Image"], key="bg_style")

    if bg_style == "Solid":
        color = st.color_picker("Background Color", "#FFFFFF", key="solid_color")
        bg = gen_solid_bg(color)

    elif bg_style == "Gradient":
        start_color = st.color_picker("Start Color", "#FFFFFF", key="grad_start")
        end_color = st.color_picker("End Color", "#FFFFFF", key="grad_end")
        direction = st.selectbox("Gradient Direction",["Vertical","Horizontal","Diagonal"])
        bg = gen_grad_bg(start_color,end_color,direction)

    elif bg_style == "Image":
        
        start_color = None
        end_color = None
        bg = st.file_uploader("Upload Background Image", type=["png", "jpg", "jpeg"], key="bg_img")
        
        if bg is not None:
            bg = process_bg(bg)

    
required_fields = [company_name or "", product_name or "", product_description or "", platform or "", cta or "",
                   phone or "", email or "", website or "", location or ""]
all_required_filled = all(field.strip() for field in required_fields)

    
        
if not st.session_state.get("generated_ad") and all_required_filled:
    
    if submitted:
        with out_col:
            with st.spinner("Generating..."):
                ad = generate_ad(input_data, temperature)
            st.session_state.generated_ad = ad
            st.session_state.restyle_trigger = True
        # st.rerun()
        
elif not all_required_filled:
    with inp_col2:
        st.info("Please fill all \*required fields.")
        
    
if st.session_state.get("generated_ad"):
    
    ad = st.session_state.generated_ad
    
    if st.session_state.get("restyle", True):  
        if bg_style == "Image" and bg is None:
            with styling_col:
                st.info("Please upload a background image.")
        else:
            img = overlay_txt(
                ad,
                bg,
                text_color,
                Font
            )
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            st.session_state.ad_image = img_bytes
            st.session_state.restyle_trigger = False
    
    
    with out_col:
        
        st.image(st.session_state.ad_image, use_container_width=True)

        st.download_button(
            label="Download Ad",
            data=st.session_state.ad_image,
            file_name="ad_image.png",
            mime="image/png",
            icon=":material/download:",
        )
            
    with styling_col:
        
        if st.button("Re-style", icon=":material/refresh:", key="restyle"):
            if bg_style == "Image" and bg is None:
                st.session_state["missing_bg_warning"] = True
            else:
                st.session_state["restyle_trigger"] = True
                st.session_state.pop("missing_bg_warning", None)
                st.rerun()

            
    with inp_col2:
        if st.button("Clear/Reset", icon=":material/refresh:"):
            st.session_state.clear()
            st.rerun()


        
