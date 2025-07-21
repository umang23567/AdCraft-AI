Here’s a complete and clean `README.md` for your **AdCraft AI** project:

---

```markdown
# 🖼️ AdCraft AI

**AdCraft AI** is a Streamlit-powered application that allows users to generate visually stunning, personalized **social media advertisements** with the help of **Google Gemini (via LangChain)** and overlay the generated content onto custom-styled image backgrounds.

## ✨ Features

- 🔥 **AI-Powered Ad Generation** using Google Gemini (via LangChain)
- 🎨 **Customizable Ad Styling** (Fonts, Colors, Gradient/Solid/Image Backgrounds)
- 📝 **JSON-structured Ad Output** using Pydantic for precision and reliability
- 🖌️ **Text Overlay Rendering** with headline, body text, CTA, hashtags, and contact info
- 📥 **Downloadable Ad Image**
- ✅ **Session-State Aware** to prevent unnecessary recomputations

---

## 📦 Folder Structure

```

adcraft-ai/
│
├── app.py                # Streamlit UI app
├── ad\_chain.py           # LangChain + Pydantic based ad generation
├── image\_gen.py          # Image/text styling and overlay rendering
├── examples.json         # Few-shot examples for better LLM generation
├── .env                  # Store GOOGLE\_API\_KEY here
├── fonts/                # Custom font files used in the app
│   ├── Arial.ttf
│   ├── Anton-Regular.ttf
│   └── ...
└── requirements.txt      # Python dependencies

````

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/adcraft-ai.git
cd adcraft-ai
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your API Key

Create a `.env` file in the root directory and add your Google Gemini API key:

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🧠 Powered By

* [LangChain](https://www.langchain.com/)
* [Google Gemini API](https://ai.google.dev/)
* [Pydantic](https://docs.pydantic.dev/)
* [Streamlit](https://streamlit.io/)
* [Pillow (PIL)](https://python-pillow.org/)

---

## 📌 Notes

* Headlines are limited to **25 characters**.
* Ad body text tries to stay **as close as possible** to the selected word limit.
* Hashtags are limited to a **maximum of 3**, unless user disables them.
* Empty fields are not guessed—output respects only what's provided.

---

## 📷 Example Output

<img src="example_ad.png" alt="Generated Ad Example" width="500"/>

---

## 🛠️ Future Improvements

* 🔧 Add multi-ad generation with variations
* 🧾 Export ads as PDF flyers or social-ready post kits
* 🧠 User account login for saving campaigns
* 🌐 API wrapper for external use

---

## 🧑‍💻 Developed By

**Umang**
Passionate about Generative AI, UI/UX, and real-world product building.

---

## 📄 License

This project is licensed under the MIT License.

```

---

Let me know if you want to:
- Add screenshots or deploy it on Streamlit Cloud
- Support more export formats like PDF
- Enable LLM selection between Gemini/ChatGPT, etc.
```
