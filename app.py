import gradio as gr

from chatbot import ResearchX
from config import APP_TITLE


# ==========================
# Model Loader
# ==========================

pilot = None


def get_pilot():

    global pilot

    if pilot is None:
        pilot = ResearchX()

    return pilot



# ==========================
# Formatting Helpers
# ==========================

def bullet_list(items):

    if not items:
        return "_Not available._"

    return "\n".join(
        f"- {item}"
        for item in items
    )



def numbered_list(items):

    if not items:
        return "_Not available._"

    return "\n".join(
        f"{i+1}. {item}"
        for i, item in enumerate(items)
    )



# ==========================
# Main Function
# ==========================

def ask_researchx(question):

    if not question.strip():

        yield (
            "Please enter a research question.",
            *[""] * 13
        )

        return


    try:

        bot = get_pilot()


        answer = ""


        # ----------------------
        # Streaming Answer
        # ----------------------

        for token in bot.stream_answer(question):

            answer += token


            yield (

                answer,

                "",

                "",

                "",

                "",

                "",

                "",

                "",

                "",

                "",

                "",

                "",

                question,

                ""

            )


        # ----------------------
        # Structured Analysis
        # ----------------------

        result = bot.analyze(question)



        profile = f"""
## 🔬 Research Profile


### Topic
{result.topic}


### Research Area
{", ".join(result.research_area)}


### Category
{result.category}


### Difficulty
{result.difficulty}


### Confidence
{result.confidence:.0%}

"""



        yield (

            answer,

            profile,

            result.summary,

            result.why_it_matters,

            bullet_list(
                result.key_concepts
            ),

            numbered_list(
                result.technical_breakdown
            ),

            numbered_list(
                result.challenges
            ),

            numbered_list(
                result.research_directions
            ),

            numbered_list(
                result.experimental_setup
            ),

            numbered_list(
                result.evaluation_plan
            ),

            numbered_list(
                result.follow_up_questions
            ),

            result.bottom_line,

            question,

            ""

        )



    except Exception as e:


        yield (

            f"""
## ❌ Error

{str(e)}
""",

            *[""] * 11,

            question,

            ""

        )



# ==========================
# Examples
# ==========================

examples = [

    ["What is Retrieval-Augmented Generation?"],

    ["What research gaps exist in RAG hallucination detection?"],

    ["How should I evaluate a RAG system?"],

    ["How can I turn an AI idea into a research plan?"],

    ["What is self-RAG?"],

]



# ==========================
# CSS
# ==========================

css = """

#title {

text-align:center;
font-size:42px;
font-weight:700;

}


#subtitle {

text-align:center;
color:#666;
margin-bottom:25px;

}


.gradio-container {

max-width:1400px !important;

}

"""



# ==========================
# Interface
# ==========================


with gr.Blocks(
    title=APP_TITLE
) as demo:


    gr.Markdown(
f"""

<div id="title">

⟡ {APP_TITLE}

</div>


<div id="subtitle">

Your AI assistant for AI/ML research exploration.

</div>

"""
)



    with gr.Row():


        with gr.Column(scale=1):


            gr.Markdown(
"""
## Supported Research Modes


📘 Concept Explanation

🔎 Research Gap Exploration

🧪 Research Methodology

🗺️ Research Planning

📄 Paper / Topic Analysis


---


## Example Questions


• What is RAG?

• Research gaps in hallucination detection

• How to evaluate a RAG system?

• Create an AI research plan

"""
)



        with gr.Column(scale=3):


            question = gr.Textbox(

                label="Ask ResearchX",

                placeholder=
                "Ask about AI, ML, Generative AI, or research methodology...",

                lines=3

            )



            with gr.Row():

                submit_btn = gr.Button(
                    "✨ Analyze",
                    variant="primary"
                )


                clear_btn = gr.Button(
                    "🗑️ Clear"
                )



            gr.Examples(

                examples=examples,

                inputs=question

            )



            answer = gr.Markdown(
                label="Quick Answer"
            )


            profile = gr.Markdown(
                label="Research Profile"
            )



            with gr.Tab("Executive Summary"):

                summary = gr.Markdown()



            with gr.Tab("Why It Matters"):

                why_it_matters = gr.Markdown()



            with gr.Tab("Key Concepts"):

                key_concepts = gr.Markdown()



            with gr.Tab("Technical Breakdown"):

                technical_breakdown = gr.Markdown()



            with gr.Tab("Challenges / Limitations"):

                challenges = gr.Markdown()



            with gr.Tab("Research Directions"):

                research_directions = gr.Markdown()



            with gr.Tab("Experimental Setup"):

                experimental_setup = gr.Markdown()



            with gr.Tab("Evaluation Plan"):

                evaluation_plan = gr.Markdown()



            with gr.Tab("Follow-up Questions"):

                follow_up_questions = gr.Markdown()



            with gr.Tab("Bottom Line"):

                bottom_line = gr.Markdown()



            hidden_question = gr.Textbox(
                visible=False
            )


            status_box = gr.Textbox(
                visible=False
            )



    # ==========================
    # Event Connections
    # MUST BE INSIDE BLOCKS
    # ==========================


    outputs = [

        answer,

        profile,

        summary,

        why_it_matters,

        key_concepts,

        technical_breakdown,

        challenges,

        research_directions,

        experimental_setup,

        evaluation_plan,

        follow_up_questions,

        bottom_line,

        hidden_question,

        status_box,

    ]



    submit_btn.click(

        fn=ask_researchx,

        inputs=question,

        outputs=outputs

    )



    question.submit(

        fn=ask_researchx,

        inputs=question,

        outputs=outputs

    )



    clear_btn.click(

        fn=lambda:
        (
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ),

        outputs=outputs

    )



# ==========================
# Launch
# ==========================

demo.queue(
    max_size=20
)



if __name__ == "__main__":

    demo.launch(
        share=True,
        css=css
    )