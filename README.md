# 🖼️ AdCraft AI

**AdCraft AI** is a Streamlit-powered application that allows users to generate personalized **social media ad postss** with the help of **Google Gemini (via LangChain)** and overlay the generated content onto custom-styled image backgrounds.

---

## ✨ Features

* 🔥 **AI-Powered Ad Generation** using Google Gemini via LangChain
* 🎨 **Customizable Ad Styling** (Fonts, Colors, Gradient/Solid/Image Backgrounds)
* 📝 **Structured JSON Output** using Pydantic models
* 🖌️ **Text Overlay Rendering** for headlines, body, CTA, hashtags, and contact info
* 📥 **Downloadable Image Ad**
* ✅ **Session-Aware Interface** with auto-reset on form changes

---

## 📦 Folder Structure

```
adcraft-ai/
│
├── app.py                # Streamlit UI logic
├── ad_chain.py           # LangChain-based ad generation
├── image_gen.py          # Image rendering and text overlay
├── examples.json         # Few-shot examples to guide LLM
├── .env                  # Google Gemini API key (not shared)
├── fonts/                # Font files
│   ├── Anton-Regular.ttf
│   ├── LibreBaskerville-Regular.ttf
│   ├── Montserrat-Italic-VariableFont_wght.ttf
│   ├── OpenSans-VariableFont_wdth,wght.ttf
│   ├── Pacifico-Regular.ttf
└── requirements.txt      # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/adcraft-ai.git
cd adcraft-ai
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

Create a `.env` file with your Gemini API key:

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🧠 Powered By

* [LangChain](https://www.langchain.com/)
* [Google Gemini](https://ai.google.dev/)
* [Streamlit](https://streamlit.io/)
* [Pillow (PIL)](https://pillow.readthedocs.io/)
* [Pydantic](https://docs.pydantic.dev/)

---

## 📷 Example Output

> (Insert an ad preview screenshot here after running the app)

---

## 🛠️ Current issues

* Clear/Reser does not reset the form fields

---


## 🛠️ Future Roadmap

* Support multiple ad variants generation (A/B testing)
* Export ads as PDF or ready-to-post social media kits
* Allow users to switch LLMs (e.g. Gemini, GPT-4, Claude)
* Add user accounts and campaign saving features
* Integrate AI image generation using LLM prompts to generate custom ad background images
* Add image templates for different social platforms (Instagram, LinkedIn, etc.)

---

## 👨‍💻 Developed By

**Umang**
Passionate about Generative AI, product design and UI/UX.

---



