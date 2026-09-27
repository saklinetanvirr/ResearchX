---
title: ResearchX
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.0.0
app_file: app.py
pinned: false
---

# ResearchX

Your AI assistant for AI/ML research exploration.

# ⟡ ResearchX

## AI Research Assistant for Generative AI & Machine Learning

ResearchX is an AI-powered research exploration assistant designed to help students and researchers understand AI/ML concepts, explore research gaps, design experiments, and plan research projects.

Built with:

- Gradio
- LangChain
- Groq API
- Pydantic Structured Output
- Large Language Models


---

# Features

## 🧠 AI Research Explanation

Provides structured explanations for:

- Generative AI concepts
- Machine Learning topics
- Deep Learning architectures
- NLP research


## 🔎 Research Gap Exploration

Helps identify:

- Open problems
- Research opportunities
- Possible improvements


## 🧪 Research Methodology

Provides guidance on:

- Experimental design
- Dataset selection
- Evaluation metrics
- Baseline comparison


## 🗺️ Research Planning

Transforms AI ideas into:

- Research questions
- Methodology
- Development roadmap


## ⚡ Streaming Response

ResearchX generates answers progressively like ChatGPT using LLM streaming.


---

# Architecture
# 🏗️ ResearchX System Architecture


```
                                      USER
                                       |
                                       |
                                       v
                         +----------------------------+
                         |      Gradio Interface      |
                         |          app.py             |
                         |                            |
                         |  - Chat Interface          |
                         |  - User Input Handling     |
                         |  - Streaming Response      |
                         |  - Research Report Tabs    |
                         +----------------------------+
                                       |
                                       |
                                       v
                         +----------------------------+
                         |       ResearchX Core       |
                         |        chatbot.py          |
                         |                            |
                         |  - Query Processing        |
                         |  - Workflow Management     |
                         |  - LLM Communication       |
                         +----------------------------+
                                       |
                                       |
                                       v
                         +----------------------------+
                         |    LangChain Pipeline      |
                         |         chains.py          |
                         |                            |
                         |  Prompt + Model Workflow   |
                         +----------------------------+
                                       |
                                       |
                                       v
                 +------------------------------------------------+
                 |              RunnableBranch                    |
                 |          Research Query Router                 |
                 +------------------------------------------------+
                                       |
                                       |
        +------------------------------+------------------------------+
        |                              |                              |
        v                              v                              v


+--------------------+       +-----------------------+       +--------------------+
| Concept Pipeline   |       | Research Pipeline     |       | Default Pipeline   |
|                    |       |                       |       |                    |
| CONCEPT_PROMPT     |       | RESEARCH_GAP_PROMPT  |       | DEFAULT_PROMPT     |
| Explanation        |       | METHODOLOGY_PROMPT   |       | General AI Query   |
| Comparison         |       | PLANNING_PROMPT      |       |                    |
| Definition         |       | Research Strategy   |       |                    |
+--------------------+       +-----------------------+       +--------------------+

        |                              |                              |
        +------------------------------+------------------------------+
                                       |
                                       |
                                       v

                         +----------------------------+
                         |        Groq API            |
                         |                            |
                         |   Large Language Model     |
                         |                            |
                         |   openai/gpt-oss-20b       |
                         +----------------------------+
                                       |
                                       |
                                       v

                         +----------------------------+
                         |     Streaming Engine       |
                         |                            |
                         |  Token-by-token generation |
                         |  ChatGPT-like experience   |
                         +----------------------------+
                                       |
                                       |
                                       v

                         +----------------------------+
                         | Structured Output Layer    |
                         |        schemas.py          |
                         |                            |
                         |      Pydantic Model        |
                         |                            |
                         |  Response Validation       |
                         +----------------------------+
                                       |
                                       |
                                       v


        +----------------------------------------------------------------+
        |                     Research Report Output                     |
        |                                                                |
        |  🔬 Research Profile                                           |
        |                                                                |
        |     - Topic                                                    |
        |     - Research Area                                            |
        |     - Category                                                 |
        |     - Difficulty                                               |
        |     - Confidence                                               |
        |                                                                |
        |----------------------------------------------------------------|
        |                                                                |
        |  📝 Executive Summary                                          |
        |                                                                |
        |  💡 Why It Matters                                             |
        |                                                                |
        |  🔑 Key Concepts                                               |
        |                                                                |
        |  ⚙️ Technical Breakdown                                        |
        |                                                                |
        |  ⚠️ Challenges & Limitations                                   |
        |                                                                |
        |  🚀 Research Directions                                        |
        |                                                                |
        |  🧪 Experimental Setup                                         |
        |                                                                |
        |  📊 Evaluation Plan                                             |
        |                                                                |
        |  ❓ Follow-up Questions                                        |
        |                                                                |
        |  🎯 Bottom Line                                                |
        |                                                                |
        +----------------------------------------------------------------+


                                       |
                                       |
                                       v


                         +----------------------------+
                         |       Deployment           |
                         |                            |
                         |   Hugging Face Spaces      |
                         |                            |
                         |   Gradio Hosting           |
                         +----------------------------+

                                       |
                                       |
                                       v

                              PUBLIC AI ASSISTANT