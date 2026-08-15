# ⟡ ResearchX

**AI Research & Paper Intelligence Assistant**

ResearchX is a LangChain-based research assistant designed for undergraduate
students exploring AI, Machine Learning, and Generative AI research.

The project is intentionally built around the exact architectural requirements of
the course assignment:

- PromptTemplate
- RunnableBranch
- RunnableParallel
- Pydantic Structured Output
- Streamlit chat interface
- Clean modular project structure

---

## 1. Project Workflow

```text
User Question
     |
     v
PromptTemplate
     |
     v
RunnableBranch
     |
     +--> Concept Explanation
     +--> Research Gap
     +--> Research Methodology
     +--> Research Planning
     +--> General Research
     |
     v
RunnableParallel
     |
     +--> Main Answer
     +--> Summary
     +--> Key Concepts
     +--> Research Directions
     +--> Follow-up Questions
     |
     v
Pydantic ResearchResponse
     |
     v
Streamlit Chat UI