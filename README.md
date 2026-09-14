# AutoFuzzLLM
AutoFuzzLLM — Agentic LLM Security Fuzzer

AutoFuzzLLM is an agentic security testing framework for Large Language Models (LLMs). It automatically generates adversarial prompt mutations, sends them to one or more LLM providers, evaluates the responses for potential security risks, maps attack categories to OWASP LLM risks, and presents the results through an interactive Streamlit dashboard.

The project combines AI-generated prompt mutation, adaptive fuzzing, response analysis, risk scoring, multi-LLM evaluation, and security reporting into a single workflow.

Purpose: Academic cybersecurity research and defensive evaluation of LLM robustness. Use only against models and systems you are authorized to test.

✨ Key Features

🤖 AI-Powered Prompt Mutation

Generates variations of a seed prompt using multiple adversarial transformation techniques.

Supported mutation operators include:

Roleplay

Authority / instruction manipulation

Persona-based prompts

Context switching

Prompt leakage

Translation

Base64 encoding

ROT13

Unicode transformations

Typoglycemia

Markdown

XML

JSON

Indirect injection

Chain-of-thought-oriented transformations

The project also contains a template-based mutation engine that can act as a fallback.

🧠 Adaptive Fuzzing

The main fuzzing campaign uses an adaptive beam-search style workflow:

Seed Prompt
    ↓
Generate Mutations
    ↓
Execute Against LLM
    ↓
Evaluate Response
    ↓
Assign Oracle Score
    ↓
Add Mutation to Seed Pool
    ↓
Select Top-K Seeds
    ↓
Generate Next Generation
    ↺

Higher-scoring mutations can be carried forward into subsequent generations, allowing the campaign to focus on more promising attack variants.

🔌 Multi-LLM Support

The project provides an LLM router for:

Provider

Integration

Gemini

Google Gemini API

Groq

Groq API

OpenRouter

OpenAI-compatible OpenRouter API

Llama2

Local Ollama server

The architecture separates the fuzzing logic from individual model providers, making provider selection configurable.

🔍 Response & Risk Analysis

Responses are evaluated using several analysis components:

Rule-based response analysis

Keyword/signature-based risk scoring

Refusal detection

Response classification

OWASP LLM category mapping

Adaptive oracle scoring

Risk severity levels

The risk scorer assigns a numerical score and categorizes results as:

Low

Medium

Critical

Error

🛡️ OWASP LLM Mapping

Attack categories are mapped to relevant OWASP LLM risk categories, including areas such as:

Prompt Injection

Sensitive Information Disclosure

Improper Output Handling

Excessive Agency

System Prompt Leakage

📊 Streamlit Dashboard

The application provides two main interfaces:

Batch Fuzzing Campaign

Configure:

LLM providers

Built-in or custom seed prompts

Number of mutations

Then view:

Mutated prompts

Model responses

Risk scores

Severity

OWASP mapping

Response time

Response length

Classification

Campaign insights

Security recommendations

💬 Live Conversation Fuzzer

Test adversarial prompts interactively in a multi-turn conversation and observe the live threat assessment of model responses.

💾 Campaign Database

Campaign information and results are persisted using SQLite.

The database stores:

Campaign timestamp

Attack category

Seed prompt

Campaign results

Mutated prompts

Model responses

Risk information

📄 Security Reports

Campaign results can be used to generate a PDF security assessment containing:

Executive summary

Models tested

Total tests

Average risk score

Model comparison

Most common attack category

Campaign metrics

Detailed findings

Security recommendations

Final security verdict

🏗️ System Architecture

flowchart TD
    A[Streamlit Dashboard] --> B[Campaign Controller]

    B --> C[Seed Prompt / Dataset]
    C --> D[AI Mutator]
    C --> E[Template Mutator]

    D --> F[Mutation Operators]
    E --> F

    F --> G[LLM Executor]
    G --> H[LLM Router]

    H --> I[Gemini]
    H --> J[Groq]
    H --> K[OpenRouter]
    H --> L[Ollama / Llama2]

    G --> M[Model Response]
    M --> N[Oracle Evaluation]
    M --> O[Risk Scorer]
    M --> P[Response Classifier]
    M --> Q[Rule Engine]

    N --> R[Seed Pool]
    R --> D

    O --> S[OWASP Mapper]
    P --> T[Dashboard Insights]
    Q --> T

    T --> U[SQLite Database]
    T --> V[PDF Security Report]

🔄 Fuzzing Workflow

Select a seed prompt

Choose a prompt from the built-in dataset or enter a custom prompt.

Generate adversarial mutations

The AI mutator and mutation operators create different versions of the seed.

Execute mutations

Each mutated prompt is sent to the selected LLM provider.

Evaluate the response

The Oracle checks for leakage, jailbreak indicators, refusal behavior, reasoning indicators, and other response characteristics.

Calculate risk

The risk scorer analyzes potentially dangerous signatures and assigns a risk score.

Map the attack

The attack category is mapped to an OWASP LLM risk category.

Update the seed pool

Mutations receive scores and can become candidates for future generations.

Beam selection

The highest-scoring seeds are retained for the next generation.

Generate insights

The dashboard summarizes model performance, attack distribution, and security posture.

Store and report

Campaign data can be persisted in SQLite and exported into security reports.

📁 Project Structure

AgenticAI/
│
├── app.py                         # Streamlit application entry point
├── core_state.py                  # Application engine/state initialization
├── fuzz_runner.py                 # Standalone fuzzing runner
├── llm_mutator.py                 # LLM mutation utilities
├── scorer.py                      # Scoring utilities
│
├── analysis/
│   ├── insights.py                # Campaign insight generation
│   ├── owasp_mapper.py            # OWASP LLM category mapping
│   ├── response_classifier.py     # Response classification
│   ├── risk_score.py              # Risk scoring engine
│   └── rule_engine.py             # Rule-based analysis
│
├── config/
│   └── settings.py                # Environment/API configuration
│
├── database/
│   └── database.py                # SQLite campaign storage
│
├── datasets/
│   └── seed_prompts.json          # Built-in seed prompt dataset
│
├── fuzzing/
│   ├── campaign.py                # Main adaptive fuzzing campaign
│   ├── executor.py                # LLM execution layer
│   ├── mutator.py                 # Template mutation engine
│   ├── adaptive_campaign.py       # Adaptive campaign implementation
│   │
│   ├── attacks/
│   │   └── base_attacks.py        # Base attack definitions
│   │
│   ├── mutations/
│   │   ├── ai_mutator.py          # AI-powered mutation generation
│   │   └── operators/             # Adversarial mutation operators
│   │
│   ├── oracle/
│   │   └── oracle.py              # Adaptive response oracle
│   │
│   └── seed_pool/
│       ├── seed.py                # Seed representation
│       └── seed_pool.py           # Seed selection/storage
│
├── llm/
│   ├── llm_router.py              # Provider routing
│   ├── gemini_client.py           # Gemini integration
│   ├── groq_client.py             # Groq integration
│   ├── openrouter_client.py       # OpenRouter integration
│   └── ollama_client.py           # Local Ollama integration
│
├── reports/
│   └── report_generator.py        # PDF report generation
│
├── pages/
│   └── 1_Campaign_History.py      # Campaign history page
│
├── tabs/
│   ├── batch_campaign.py          # Batch fuzzing UI
│   └── live_fuzzer.py             # Live conversation fuzzer UI
│
├── ui/
│   ├── charts.py                  # Dashboard charts
│   ├── insights.py                # Dashboard insights
│   ├── explanations.py            # Result explanations
│   └── dynamic_insights.py        # Dynamic UI insights
│
├── datasets/
├── requirements.txt
└── campaign_report.pdf            # Example/generated campaign report

🛠️ Tech Stack

Python

Streamlit — interactive web dashboard

Google Gemini API — Gemini model integration

Groq API — LLM inference

OpenRouter — OpenAI-compatible multi-model access

Ollama — local LLM execution

SQLite — campaign/result persistence

Pandas — result processing and analytics

ReportLab — PDF report generation

python-dotenv — environment configuration

⚙️ Installation

1. Clone the repository

git clone https://github.com/ravinameena0805-lgtm/AgenticAI.git
cd AgenticAI

2. Create a virtual environment

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

The current code also imports groq and the OpenAI-compatible client used by OpenRouter. If they are not already installed in your environment, install them with:

pip install groq openai

4. Configure API keys

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

Do not commit your .env file or API keys to GitHub.

🦙 Running Llama2 Locally with Ollama

The project can use a local Ollama endpoint:

http://localhost:11434/api/chat

The configured local model is:

llama2

Make sure Ollama is running and the model is available before selecting Llama2 in the dashboard.

🚀 Run the Application

Start Streamlit from the project root:

streamlit run app.py

Streamlit will display a local URL in the terminal. Open that URL in your browser.

🧪 Running Tests

The repository contains test files covering several components, including:

test_adaptive.py
test_ai_mutator.py
test_campaign.py
test_database.py
test_mutator.py
test_openrouter.py
test_operator_manager.py
test_oracle.py
test_seed_pool.py

Run an individual test script with:

python test_oracle.py

or another test file as required.

Some integration tests require the corresponding LLM provider/API or local Ollama service to be configured.

📚 Built-in Dataset

The project includes seed prompts in:

datasets/seed_prompts.json

The current dataset contains categories such as:

Prompt Injection

Hallucination

Jailbreak

You can also provide a custom seed prompt directly from the Streamlit interface.

📈 Risk Scoring

The response risk scorer uses rule-based indicators to produce a numerical score.

Examples of monitored signatures include:

Malware-related terms

Exploit-related terms

Credentials

API keys

Passwords

Secrets

System prompts

Developer messages

Tokens

Additional scoring behavior considers response length and explicit refusal language.

Severity

Score < 35     → Low
35–69          → Medium
Score ≥ 70     → Critical

The scoring engine is intended as a heuristic security signal, not as a definitive vulnerability proof.

🔎 Adaptive Oracle

The adaptive Oracle evaluates model responses using indicators such as:

Sensitive information leakage

Jailbreak indicators

Refusal behavior

Long responses

Reasoning-related phrases

A sufficiently high oracle score marks a mutation as a successful/high-value candidate for adaptive exploration.

🛡️ Security & Responsible Use

AutoFuzzLLM is designed for authorized security testing and academic research.

Only test:

Models you own

Models you have permission to evaluate

Authorized research environments

Local test deployments

Do not use the framework to attack third-party systems without authorization.

The generated prompts are adversarial testing inputs; their presence in a test case does not mean the target model is actually vulnerable. Results should be manually reviewed and validated.

🔮 Future Improvements

Potential extensions include:

More sophisticated semantic vulnerability detection

LLM-as-a-judge evaluation

More adaptive mutation strategies

Multi-turn adaptive attack campaigns

Tool-use and agent security testing

Better false-positive reduction

Automated regression testing

More comprehensive OWASP LLM coverage

Additional LLM providers

Richer campaign comparison dashboards

CI/CD security testing integration
