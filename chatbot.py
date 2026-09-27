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



    # -----------------------
    # Streaming answer
    # -----------------------

    def stream_answer(self, question):

        draft = self.branch.invoke(
            question
        )


        prompt = PromptTemplate.from_template(
        """
You are ResearchX, an AI/ML research assistant.

Answer the question clearly.

Use:
- headings
- explanations
- bullet points
- technical accuracy


Question:

{question}


Research Draft:

{draft}

"""
        )


        chain = prompt | llm


        for chunk in chain.stream(
            {
                "question":question,
                "draft":draft
            }
        ):

            if chunk.content:

                yield chunk.content



    # -----------------------
    # Structured report
    # -----------------------

    def analyze(self, question):


        draft = self.branch.invoke(
            question
        )


        result = self.structured.invoke(
            {
                "draft":draft
            }
        )


        return result