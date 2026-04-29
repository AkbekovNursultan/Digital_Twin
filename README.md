# 🤖 Digital Twin Career Engine
**Nursultan Akbekov — Software Engineering, Ala-Too International University**
> An AI-powered personal career manager that analyzes your digital footprint to predict your optimal career path, map your skills, and manage your professional growth.

---

## 🚀 Live Demo
Run locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🏗️ 5-Layer Architecture

### Layer 0 — Data Engineering (The Inputs)

The system is fed three primary data sources, all uploaded to NotebookLM as structured resources:

| Source | Format | Content |
|--------|--------|---------|
| CV / Resume | PDF | Work experience, skills, project descriptions |
| LinkedIn Profile | PDF export | Skills section, education, endorsements |
| Academic Transcript | PDF | Course grades, GPA, relevant coursework |

All data was cleaned and structured before ingestion. The transcript confirmed a **GPA of 3.59** across 6 semesters and 154 credits. The CV captured real production experience from the **O! Mobile Operator Intern Labs 6.0** internship. Soft skills were inferred from project descriptions and course context rather than listed explicitly.

---

### Layer 1 — Platform (MCP Integration)

**Goal:** Bridge NotebookLM and Antigravity so the agent can query personal knowledge directly.

**Implementation:**
- Installed `notebooklm-mcp-server` (v3.0.5) via `npx`
- Authenticated with Google account via `npx notebooklm-mcp-server auth`
- Registered the MCP server in Antigravity with command `npx -y notebooklm-mcp-server`
- Set Antigravity Auto-Execution policy to **Always Proceed**
- Passed the NotebookLM notebook link in the system prompt

**System Prompt Injected:**
```
You are a Digital Twin career agent for Nursultan Akbekov.
Query the NotebookLM notebook via MCP and extract:
1. Hard/technical skills as a JSON array
2. Soft skills inferred from project and internship context
3. Academic background and GPA
4. Work and project experience with technologies used
```

**Verification:** Antigravity successfully listed all notebooks and extracted a structured skill vector with 22 hard skills and 16 soft skills.

---

### Layer 2 — Model (Reasoning & Prediction)

**Goal:** Mathematically predict the top 3 best-fit jobs and identify skill gaps.

**Algorithm:** TF-IDF Vectorization + Cosine Similarity (`scikit-learn`)

**Dataset:** Custom tech jobs dataset with 1,000+ listings across roles including Java Developer, Software Engineer, Backend Developer, Android Developer, and more. Each listing contains `Title`, `Skills`, `ExperienceLevel`, and `Keywords` columns.

**Process:**
1. Combined all hard + soft skills into a single user skill document
2. Combined `Title + Skills + Keywords` for each job into a job document
3. Applied TF-IDF vectorization with bigrams (`ngram_range=(1,2)`, `max_features=5000`)
4. Computed cosine similarity between the user vector and all job vectors
5. Ranked jobs by score, deduplicated by title, returned top 3

**Output (`prediction_output.json`):**
```json
{
  "top_predicted_jobs": [
    {
      "title": "Java Developer",
      "experience_level": "Experienced",
      "similarity_score": 0.2578,
      "missing_skills": ["Advanced Java"]
    },
    {
      "title": "Software Engineer - Experienced",
      "similarity_score": 0.17,
      "missing_skills": ["AWS", "Docker", "Kubernetes", "Agile"]
    },
    {
      "title": "JavaScript Developer",
      "similarity_score": 0.1391,
      "missing_skills": ["React", "Angular", "Responsive Design"]
    }
  ]
}
```

**Script:** `career_predictor.py`

---

### Layer 3 — Agent (Live Execution via Antigravity)

**Goal:** Take the ML-predicted missing skill and autonomously browse the live internet for current learning resources.

**Implementation:**
- Antigravity was given web-browsing tool access
- The ML output (`missing_skill: Advanced Java`) was injected into the agent system prompt dynamically
- The agent executed a live search query, parsed top results, and extracted structured resources

**System Prompt:**
```
You are a career agent for Nursultan Akbekov, a Java Backend Developer.
His ML model predicted his top career match is: Java Developer (Experienced)
His most important missing skill is: Advanced Java (JVM internals, concurrency,
performance tuning, design patterns)

1. Search the web for top 3 current learning resources for "Advanced Java 2024 2025"
2. For each: extract title, URL, type, and why it helps
3. Find 1 active hackathon or open-source Java project
4. Return as JSON with keys: learning_resources and community
```

**Agent Output (`agent_output.json`):** 3 learning resources (Udemy course, O'Reilly book, Effective Java) + 1 open source project (java-design-patterns on GitHub) + 1 hackathon (MLH Global Hack Week).

---

### Layer 4 — Application (Vibe-Coded UI)

**Stack:** Streamlit + Plotly + Anthropic Claude API

**Run:** `streamlit run app.py`

The dashboard has 4 interactive modules accessible via sidebar navigation:

#### ⚖️ Balance Wheel
- Two Plotly radar charts side by side
- Left chart: 12 hard/technical skills with proficiency scores
- Right chart: 10 soft skills with inferred scores
- Summary metrics: average hard score, average soft score

#### 🗺️ RPG Tech Tree
- Dark-mode node graph built with Plotly Scatter
- **Green nodes** = currently unlocked skills (Java Core, Spring Boot, REST API, etc.)
- **Orange nodes** = locked/missing skills (Docker, AWS, Kubernetes, Advanced Java)
- **Gold node** = dream job target (Java Developer Experienced)
- Directed edges show the learning progression path

#### 💬 Live Coach Chatbot
- Real-time chat powered by **gemini-2.5-flash** via Anthropic API
- Normal mode: warm, encouraging career advisor with full profile context
- **Roast Mode** toggle: aggressive senior tech lead persona that humorously critiques the stack, missing skills, and Vue.js choice
- Full conversation history maintained in `st.session_state`

#### 🎁 Semester Wrapped
- Styled shareable card (dark gradient, custom CSS)
- Displays: Top Skill, Best Course, Internship, Shipped Project, GPA, ML Predicted Career, Total Credits
- Designed to be screenshot and posted on LinkedIn

---

### Layer 5 — Infrastructure (Hardware & Hosting)

| Component | Runs On | Why |
|-----------|---------|-----|
| Streamlit server | **Local CPU** | Python web server runs on your machine at `localhost:8501` |
| ML script (`career_predictor.py`) | **Local CPU** | TF-IDF + cosine similarity computed locally via scikit-learn |
| NotebookLM knowledge base | **Google Cloud** | Hosted and served by Google's infrastructure |
| MCP Server (`notebooklm-mcp-server`) | **Local CPU** | Node.js process runs locally, bridges to Google's API |
| Antigravity Agent | **Cloud (Antigravity servers)** | LLM inference and web browsing executed remotely |
| Claude API (chatbot) | **Anthropic Cloud** | API calls sent to Anthropic's servers, response streamed back |
| Job dataset | **Local disk** | CSV file read directly by pandas on your machine |

**Summary:** Data processing and the ML model run entirely on local hardware. All LLM inference (Antigravity agent, Claude chatbot) runs on cloud servers. The NotebookLM knowledge base is hosted on Google Cloud but queried locally via MCP.

---

## 📁 Project Structure

```
digital-twin-career-engine/
│
├── app.py                    # Layer 4: Streamlit dashboard (all 4 UI modules)
├── career_predictor.py       # Layer 2: ML prediction script
├── jobs_dataset.csv          # Layer 2: Job listings dataset
├── prediction_output.json    # Layer 2: ML output (top 3 jobs + missing skills)
├── agent_output.json         # Layer 3: Antigravity web search results
├── requirements.txt          # Python dependencies
├── .env                      # API keys (NOT committed)
├── .gitignore                # Excludes personal data and secrets
└── README.md                 # This file
```

---

## 📦 Requirements

```
streamlit
plotly
pandas
scikit-learn
anthropic
python-dotenv
```

Install:
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_key_here
```

---

## 👤 Author

**Nursultan Akbekov**
Computer Science Bachelor — Ala-Too International University, Bishkek, Kyrgyzstan
GitHub: [@Akbekov](https://github.com)
Email: nursultan20052003@gmail.com