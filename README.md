---
#Astrology API
---

#The project structure
---
horary_astrology_api/
│── src/
│   │── main.py                  # FastAPI main application file
│   │── api/
│   │   │── endpoints.py          # API endpoints
│   │── services/
│   │   │── astrology_service.py  # Core astrology logic (horary analysis)
│   │   │── llm_service.py        # Turkish LLM integration
│   │   │── utilis.py        
│   │── db/
│   │   │── database.py           # Database connection ()

│── requirements.txt              # Python dependencies
│── README.md                     # Documentation
│── .env                           # API keys and secrets