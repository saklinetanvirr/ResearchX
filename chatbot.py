from langchain_core.prompts import PromptTemplate

from chains import (
    build_branch,
    build_structured_pipeline
)

from config import llm


class ResearchX:


    def __init__(self):

        self.branch = build_branch()

        self.structured = build_structured_pipeline()



    def stream_answer(self, question):

        draft = self.branch.invoke(question)


        prompt = PromptTemplate.from_template(
        """
You are ResearchX, an AI/ML research assistant.

Provide a high quality explanation.

Rules:

- Use markdown headings
- Explain step by step
- Use examples
- Keep technical accuracy


Question:

{question}


Research Notes:

{draft}

"""
        )


        chain = prompt | llm


        full_answer = ""


        for chunk in chain.stream(
            {
                "question": question,
                "draft": draft
            }
        ):

            if chunk.content:

                full_answer += chunk.content

                yield chunk.content



    def analyze(self, question):

        draft = self.branch.invoke(question)


        result = self.structured.invoke(
            {
                "draft": draft
            }
        )


        return result