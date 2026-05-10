# 🔍 Product Comparison Engine

> An AI-powered two-agent system that compares any two products — giving you specs, pros/cons, and a smart recommendation.

---

## 2. Overview

The **Product Comparison Engine** is an intelligent web application that allows users to compare any two products side-by-side. Users simply enter two product names (e.g., *iPhone 15 vs Samsung Galaxy S24*), and a multi-agent AI pipeline automatically fetches product data, analyses it, and delivers a clear, unbiased recommendation.

**Problem it solves:** Researching and comparing products is time-consuming. Users visit multiple sites, read lengthy reviews, and still struggle to make a decision. This engine automates the entire process.

**Who it's for:** Students, shoppers, tech enthusiasts, and anyone who wants to make smarter purchase decisions quickly.

---

## 3. Objective

Students will learn how to:
- Build a **multi-agent AI system** using LangChain
- Use **LLM tool calling** and ReAct agents
- Integrate a **Streamlit** frontend with a multi-step AI backend
- Design agent pipelines where **Agent 1 feeds Agent 2**
- Handle real-world web data fetching inside agent tools
- Structure a production-grade Python AI project

**Key concepts covered:**
- LangChain Agents & AgentExecutor
- ReAct (Reason + Act) agent pattern
- LangChain Tools (`@tool` decorator)
- Chat models with Groq llama
- Streamlit UI with dynamic state management

---

## 4. Features

- 🔵 **Agent 1 — Data Collector:** Automatically fetches specs, price, ratings, and key info for any product
- 🟢 **Agent 2 — Decision Maker:** Analyses both products and generates a structured comparison with pros, cons, and recommendation
- ⚡ **Real-time streaming UI** with live status updates per agent
- 📦 **VS input parser:** Accepts both separate fields and `"Product A vs Product B"` format
- 💡 **Quick example buttons** in the sidebar for instant demos
- 📊 **Formatted comparison table** with markdown rendering
- 🔒 **Secure API key** input via sidebar (not stored)

---

## 5. Architecture / Workflow

```
User Input (Product A, Product B)
            │
            ▼
┌──────────────────────────┐
│  Agent 1: Data Collector │  ← Uses fetch_product_data tool
│  - Fetches specs         │    (SerpAPI + LLaMA 3 knowledge)
│  - Price range           │
│  - User ratings          │
│  - Target audience       │
└──────────┬───────────────┘
           │ Structured Profile A + B
           ▼
┌──────────────────────────┐
│  Agent 2: Decision Maker │  ← Reasoning-only (no tool needed)
│  - Comparison table      │
│  - Pros & Cons           │
│  - Final recommendation  │
└──────────┬───────────────┘
           │
           ▼
  Streamlit UI — Full Report
```

**Step-by-step flow:**
1. User enters Product A and Product B in the Streamlit UI
2. Agent 1 runs for Product A → fetches web data → builds structured profile
3. Agent 1 runs for Product B → same process
4. Agent 2 receives both profiles → performs deep comparison analysis
5. Full report with table, pros/cons, and recommendation is displayed

---

## 6. Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Agent Framework | LangChain 0.2.x |
| LLM Provider | Groq (LLaMA 3 70B) |
| Frontend | Streamlit 1.35 |
| Web Data Tool | SerpAPI + LLM knowledge |
| HTTP Client | Requests |
| Environment | python-dotenv |

---

## 7. Project Structure

```
product_comparison_engine/
│
├── main.py                  # Streamlit app entry point
│
├── agents/
│   ├── __init__.py
│   ├── data_collector.py    # Agent 1: fetches product data
│   └── decision_maker.py    # Agent 2: compares & recommends
│
├── tools/
│   ├── __init__.py
│   └── product_fetcher.py   # LangChain tool: web search
│
├── utils/
│   ├── __init__.py
│   └── helpers.py           # Input parsing & text utilities
│
├── .env                     # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 8. Setup Instructions

### Prerequisites
- Python 3.10 or higher
- A Groq API key → [Get one here](https://console.groq.com)
- A SerpAPI key → [Get one here](https://serpapi.com) (Free, 250 searches/month)

### Installation

**Step 1: Clone or download the project**
```bash
git clone <your-repo-url>
cd product_comparison_engine
```

**Step 2: Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Set up environment**

- GROQ_API_KEY=gsk_your_groq_key_here
- SERPAPI_KEY=your_serpapi_key_here

### Running the Project

```bash
streamlit run main.py
```

Then open your browser at: `http://localhost:8501`

---

## 9. How It Works (Code-Level Explanation)

### `tools/product_fetcher.py`
Defines a LangChain `@tool` called `fetch_product_data`. It calls the SerpAPI (Google Search) to retrieve web snippets about the product, and returns them as a formatted string. This is the "eyes" of Agent 1.

### `agents/data_collector.py`
Builds a **ReAct agent** using `create_react_agent`. The agent receives a product name, uses the `fetch_product_data` tool to gather web data, and then uses LLaMA 3 (via Groq) to reason over that data and return a clean structured profile (price, specs, ratings, etc.).

### `agents/decision_maker.py`
A **reasoning-only agent** (no tool needed). It receives the two structured profiles from Agent 1, and uses a carefully crafted system prompt to produce a formatted comparison table, pros/cons lists, and a clear recommendation.

### `utils/helpers.py`
Contains helper functions like `parse_vs_input()` which parses a string like "iPhone vs Samsung" into two separate product names, and `sanitize_product_name()` for clean formatting.

### `main.py`
The Streamlit UI. Handles user input, calls both agents sequentially, shows live status for each agent step, and renders the final markdown report.

---

## 10. Example Usage

**Input:**
```
Product A: iPhone 15 Pro
Product B: Samsung Galaxy S24
```

**Agent 1 Output (per product):**
```
Product Name: iPhone 15 Pro
Category: Smartphone
Price Range: ₹1,34,900 – ₹1,59,900
Key Specifications:
  - A17 Pro chip (3nm)
  - 48MP main camera, 12MP ultrawide, 12MP telephoto
  - 6.1-inch Super Retina XDR display
  - USB-C with USB 3 speeds
  - Titanium frame
User Ratings: 4.6/5 — Highly praised for camera and performance
Availability: Online & Offline
Target Audience: Premium users, creative professionals
```

**Agent 2 Output:**
```
## 📊 Comparison Summary
| Feature      | iPhone 15 Pro | Samsung Galaxy S24 |
|--------------|--------------|-------------------|
| Price        | ₹1,34,900+   | ₹79,999+          |
| Rating       | 4.6/5        | 4.5/5             |
| Performance  | A17 Pro      | Snapdragon 8 Gen 3|
...

## 🏆 Recommendation
Best Choice: Samsung Galaxy S24
Why: Offers flagship performance at a significantly lower price point...
Best for: Budget-conscious users who want premium Android experience
```

---

## 11. Customization / Extensions

Students can extend this project in several ways:

- **Add real APIs:** Integrate the Flipkart Affiliate API or Amazon Product Advertising API for live pricing
- **Add more agents:** Create an "Agent 3 — Review Sentiment Analyzer" that reads user reviews from the web
- **Price tracking:** Add a history graph showing price trends over time using Plotly
- **Category auto-detection:** Automatically detect whether products are phones, laptops, headphones, etc. and adjust comparison criteria
- **Export feature:** Let users download the comparison as a PDF report
- **Voice input:** Add speech-to-text so users can speak product names

---

## 12. Future Improvements

- 🔄 **Streaming responses** — Show the comparison report token by token as it's generated
- 🌐 **Real e-commerce API integration** — Live price and availability from Amazon/Flipkart
- 📈 **Comparison history** — Save past comparisons in a local database
- 🌍 **Multi-language support** — Generate reports in Tamil, Hindi, etc.
- 📱 **Mobile-responsive UI** — Better layout for phone screens
- 🤝 **Group comparison** — Compare 3 or more products at once
- 🔔 **Price alert agent** — Notify user when a product drops in price

---

## 13. Contributors

- Kruthiga T B
- Lavanya S

---

*Built with ❤️ using LangChain, Groq (LLaMA 3 70B), and Streamlit*
