# ✈️ TripMate AI – AI-Powered Multi-Agent Travel Planner

An AI-powered travel planning application that transforms natural-language travel requests into structured and practical travel plans. Built using **LangGraph, LangChain, Groq, FastAPI, and PostgreSQL**, TripMate AI helps users discover flight options, explore hotels, and generate personalized day-by-day itineraries.

## 🌍 Project Overview

Planning a trip often requires searching across multiple websites to find flights, hotels, sightseeing locations, and budget-friendly activities.

**TripMate AI** simplifies this process through a multi-agent workflow. Each agent handles a specific travel-planning task, while LangGraph coordinates the complete workflow.

Users can submit requests such as:

> Plan a 7-day trip to Japan from Mumbai, including flights, hotels, sightseeing, and an overall budget under ₹2 lakh.

The system processes the request and generates a structured travel plan.

## ✨ Key Features

* ✈️ **Flight Search:** Retrieves flight-related information using AviationStack API.
* 🏨 **Hotel Research:** Finds hotel suggestions and accommodation information using Tavily Search.
* 🤖 **Multi-Agent Workflow:** Coordinates specialized agents using LangGraph.
* 🗺️ **AI Itinerary Generation:** Creates practical day-by-day travel itineraries.
* 💰 **Budget Planning:** Provides estimated travel budgets based on user requirements and available information.
* 🌐 **FastAPI Backend:** Provides REST API endpoints for travel requests.
* 💬 **Web Interface:** Simple frontend built using HTML, CSS, and JavaScript.
* 💾 **Conversation Persistence:** Stores workflow checkpoints using PostgreSQL.
* ⚡ **LLM Integration:** Uses Groq-powered language models to generate travel recommendations.

## 🧠 Multi-Agent Architecture

The project uses a sequential multi-agent workflow implemented with LangGraph.

### Agents

| Agent           | Responsibility                                  | Technology        |
| --------------- | ----------------------------------------------- | ----------------- |
| Flight Agent    | Retrieves flight-related information            | AviationStack API |
| Hotel Agent     | Searches hotels and accommodation options       | Tavily API        |
| Itinerary Agent | Generates day-by-day travel plans               | Groq LLM          |
| Final Agent     | Combines all results into a structured response | Groq LLM          |

### Workflow

```text
              User Travel Request
                      |
                      v
                Flight Agent
                      |
                      v
                 Hotel Agent
                      |
                      v
               Itinerary Agent
                      |
                      v
                 Final Agent
                      |
                      v
              Structured Response
```

**LangGraph** manages the execution flow and **PostgreSQL Checkpointing** supports conversation-state persistence.

## 🛠️ Tech Stack

### Backend

* Python 3.10+
* FastAPI
* LangGraph
* LangChain
* PostgreSQL
* Psycopg

### AI & LLM

* Groq API
* Groq-supported language models

### External APIs

* AviationStack API – Flight information
* Tavily API – Web search and hotel research

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2

## 📁 Project Structure

```text
TripMate-AI/
│
├── app.py                  # FastAPI application entry point
├── backend.py              # LangGraph multi-agent workflow
├── test.py                 # Testing the travel agent
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables
│
├── tools/
│   ├── flight_tool.py      # AviationStack flight integration
│   └── tavily_tool.py      # Tavily search integration
│
├── templates/
│   └── index.html          # Frontend template
│
└── static/
    ├── style.css           # Frontend styling
    └── script.js           # Frontend JavaScript
```

## ⚙️ Prerequisites

Before running the project, install:

* Python 3.10 or newer
* PostgreSQL
* Git
* VS Code (recommended)

You will also need API keys for:

* Groq
* Tavily
* AviationStack

## 🔑 Environment Configuration

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db

GROQ_API_KEY=your_groq_api_key

AVIATIONSTACK_API_KEY=your_aviationstack_api_key

TAVILY_API_KEY=your_tavily_api_key

DEFAULT_ORIGIN_IATA=BOM
```

**Note:** `BOM` represents Mumbai Airport. Change the default origin airport code according to your requirements.

Never upload your `.env` file or API keys to GitHub.

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL

cd TripMate-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure PostgreSQL

Create a PostgreSQL database named:

```sql
CREATE DATABASE travel_db;
```

Configure your `DATABASE_URL` in the `.env` file.

### 6. Configure API keys

Add your Groq, Tavily, and AviationStack API keys to `.env`.

### 7. Run the application

```bash
python app.py
```

Open your browser:

```text
http://127.0.0.1:8000/
```

## 🔌 API Endpoints

| Method | Endpoint      | Description               |
| ------ | ------------- | ------------------------- |
| GET    | `/health`     | Checks application health |
| POST   | `/api/travel` | Generates a travel plan   |

### Example API Request

**Endpoint:**

```text
POST http://127.0.0.1:8000/api/travel
```

**Request Body:**

```json
{
    "message": "Plan a 7-day trip to Japan from Mumbai with flights, hotels, sightseeing and a budget under 2 lakh INR."
}
```

### Example using cURL

```bash
curl -X POST http://127.0.0.1:8000/api/travel \
-H "Content-Type: application/json" \
-d "{\"message\":\"Plan a 7-day trip to Japan under 2 lakh INR\"}"
```

## 🔄 How It Works

1. **User Input:** The user submits a natural-language travel request.
2. **Flight Research:** The Flight Agent retrieves available flight-related information.
3. **Hotel Research:** The Hotel Agent searches for accommodation options.
4. **Itinerary Planning:** The Itinerary Agent uses the collected information to generate a day-by-day travel plan.
5. **Final Response:** The Final Agent combines the results into a structured response.
6. **State Persistence:** PostgreSQL Checkpointing saves workflow state for the conversation thread.

## 📌 Important Notes

* Flight information depends on AviationStack API availability and subscription limitations.
* Live ticket prices may not be available through the flight API. The application should clearly communicate when fares cannot be verified.
* Hotel suggestions are based on Tavily search results and should be verified before booking.
* Budget figures are estimates, not confirmed booking prices.
* API keys must be stored securely in environment variables.

## 🔮 Future Enhancements

* [ ] Integrate real-time flight pricing and booking APIs.
* [ ] Add hotel booking integrations.
* [ ] Implement conversational memory for follow-up travel requests.
* [ ] Add currency conversion for international trips.
* [ ] Add interactive maps and sightseeing recommendations.
* [ ] Introduce dynamic budget optimization.
* [ ] Add user authentication and personalized travel history.
* [ ] Deploy the application to a cloud platform.

## 🤝 Contributing

Contributions are welcome!

1. Fork this repository.
2. Create a new feature branch.
3. Implement your changes.
4. Commit your changes.
5. Submit a Pull Request.

## 👨‍💻 Author

**Sarvesh Mandhare**

BE Computer Science Engineering – Artificial Intelligence & Machine Learning

Interested in Python Development, Artificial Intelligence, Generative AI, and Multi-Agent Systems.

* LinkedIn: https://www.linkedin.com/in/sarvesh-mandhare/
* GitHub: https://github.com/SarveshMandhare

---

⭐ If you find this project useful, consider giving it a star!
