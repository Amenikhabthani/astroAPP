# 🌌 Astrology API (Horary-Based)

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a FastAPI-based web API designed to answer **horary astrology** questions using a blend of **traditional astrological methods** and **modern AI/NLP** techniques.

---

## 🧠 Powered By

- **John Frawley**’s *Horary Textbook*
- **William Lilly**’s *Introduction to Astrology*
- **Morin’s techniques** (via *Down-to-Earth Sky* by Penny Seator)
- Public APIs like:  
  [Astrologer API](https://rapidapi.com/gbattaglia/api/astrologer/)
---

## 🗂️ Project Structure

astrology-api/ │ ├── src/ │ ├── main.py # FastAPI main app │ ├── api/ │ │ └── endpoints.py # API endpoints │ ├── services/ │ │ ├── astrology_service.py # Horary logic │ │ ├── llm_service.py # LLM response generator │ │ └── utilis.py # Utilities │ └── db/ │ └── database.py # DB logic │ ├── .env # API keys and secrets ├── requirements.txt # Python dependencies ├── README.md # You’re here! ├── .gitignore # Ignore env & secrets


---

## ⚙️ Setup & Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/Amenikhabthani/astroAPP.git
   cd astroAPP
2. **Create & activate a virtual environment**
      ```bash
   python -m venv venv
   source venv/bin/activate       # Windows: venv\Scripts\activate

3. **Install dependencies**
   ```bash

   pip install -r requirements.txt

4. **Create a .env file**
   ```bash

   ASTRO_API_KEY=your_astro_api_key
   OPENAI_API_KEY=your_llm_api_key
   SUPABASE_KEY=your_supabase_api_key
   SUPABASE_URL=your_supabase_url

## 🚀 Run the API

   ```bash 
   uvicorn src.main:app --reload

---
## 🧪 Example Usage

You can test the API using tools like Postman.

Use a POST request to:
http://127.0.0.1:8000/interpret

Under the Body tab:

-Choose raw

-Set the type to JSON

-Paste the example body:
{
  "question": "Will I get the job?"
}

Click Send to receive the response.