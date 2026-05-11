# AI Cultural Meaning Explorer

An AI-powered web app that helps users understand how the same word carries different meanings across cultural and literary contexts.

---

## 1. Context, User, and Problem

**Target Users:** Students, writers, and global communicators who want to understand cross-cultural word meanings.

**Workflow:** A user enters a word (e.g., "moon"), selects a cultural context (e.g., Chinese Classical Poetry), and receives an interactive semantic network showing related concepts and explanations.

**Why it matters:** The same word can mean homesickness in Chinese poetry, danger in Western horror, and harmony in Taoist philosophy. Plain dictionaries do not capture this. Misunderstanding cultural symbolism causes confusion in cross-cultural communication, translation, and literary analysis.

---

## 2. Solution and Design

**What I built:** A Streamlit web app with two modes:
- **Main system:** Enter a word → select a cultural context → view an AI-generated semantic network with concept explanations
- **Baseline comparison:** Enter the same word → receive a plain dictionary-style paragraph with no context separation

**Key design choices:**
- Used GPT-4o-mini via the OpenAI API for all generation
- Structured prompts to force consistent JSON output (context list + semantic graph)
- Kept each graph to a single cultural context to avoid mixing meanings
- Built a sidebar baseline so users can directly compare the two approaches side by side
- No RAG or agents — a single prompt per step is enough for this task

**Project structure:**
cultural-meaning-explorer/
├── app.py              # Main Streamlit app
├── prompts.py          # All prompts
├── requirements.txt    # Dependencies
├── .env.example        # API key template
├── eval/
│   └── test_cases.json # 10 evaluation test cases
└── README.md

---

## 3. Evaluation and Results

**Baseline:** A single paragraph dictionary explanation with no cultural context separation.

**Test set:** 10 cases across 5 words (moon, water, night, wind, fire, shadow) and diverse cultural contexts including Chinese Classical Poetry, Western Horror, Taoism, Greek Mythology, and Jungian Psychology.

**Rubric (each scored 1–3):**

| Criterion | 1 – Poor | 2 – Acceptable | 3 – Good |
|---|---|---|---|
| Accuracy | Wrong or irrelevant themes | Partially correct | Matches expected themes |
| Cultural Relevance | Generic, could apply anywhere | Some cultural specificity | Clearly tied to the named context |
| Clarity | Confusing or vague | Understandable | Clear and well-explained |

**Results summary:**

| Word | Context | Accuracy | Cultural Relevance | Clarity |
|---|---|---|---|---|
| moon | Chinese Classical Poetry | 3 | 3 | 3 |
| moon | Western Horror Literature | 3 | 3 | 3 |
| water | Chinese Philosophy | 3 | 3 | 2 |
| water | Western Romantic Poetry | 2 | 2 | 3 |
| night | Gothic Literature | 3 | 3 | 3 |
| night | Chinese Modern Literature | 2 | 2 | 2 |
| wind | Japanese Haiku | 3 | 3 | 3 |
| fire | Greek Mythology | 3 | 3 | 3 |
| fire | Native American Spirituality | 2 | 2 | 2 |
| shadow | Jungian Psychology | 2 | 3 | 2 |

**What worked:** Well-documented contexts (Chinese poetry, Greek mythology, Gothic literature) produced accurate and culturally specific outputs consistently.

**What failed:** Less-documented contexts (Native American spirituality, some modern literature) produced more generic outputs. The system occasionally mixed metaphors from different traditions.

**Where a human should stay involved:** The system should not be used for academic citation or authoritative literary analysis. A human expert should verify outputs for less-documented cultural traditions.

---

## 4. Artifact Snapshot

**Input:** User types "moon" and clicks Explore →

**Step 1 — Context selection:**
The system generates 5 cultural context buttons:
- 🏮 Chinese Classical Poetry
- 🌑 Western Horror Literature
- ☯️ Taoist Philosophy
- 🌊 Japanese Haiku
- 🎭 Shakespearean Drama

**Step 2 — Semantic network:**
Clicking a context displays a visual graph centered on "moon" with 5–6 connected concept nodes (e.g., Homesickness, Reflection, Distance, Night Sky) and one-sentence explanations for each.

**Baseline comparison (sidebar):**
The same word returns a single generic paragraph with no cultural distinction — demonstrating the limitation the system addresses.

---

## Setup and Usage

### Requirements
- Python 3.8+
- OpenAI API key with available credits

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/cultural-meaning-explorer.git
cd cultural-meaning-explorer
pip install -r requirements.txt
```

### API Key Setup

Copy `.env.example` to `.env` and add your key:

```bash
cp .env.example .env
```

Edit `.env`:
OPENAI_API_KEY=your-key-here

### Run the app

```bash
streamlit run app.py
# or on Windows:
py -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.
