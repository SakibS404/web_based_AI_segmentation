from openai import OpenAI
import os
import base64





client = OpenAI()


def llm_response(image_path):


    #since keys in the venv it wont run outside it
    if not os.getenv("OPENAI_API_KEY"):
        return "Sakib: Sorry but the API key is on my local pc virtual environment so it wont work here"

    try:
        #convert image to json to give to llm
        with open(image_path,"rb")as f:

            image_base64 = base64.b64encode(f.read()).decode("utf-8")



        response = client.responses.create(

        model="gpt-4.1-mini",
        input=[{
        "role": "user",
        "content": [
            {"type": "input_text",
             
              "text": """This is a output of abrain MRI with a segmentation overlay.

                Colors (if present):
                - red = necrotic core
                - green = edema (swelling)
                - blue = active tumor

                IMPORTANT:
                Carefully check if any red, green, or blue colored regions are actually visible.

                If NO colored regions are present:
                - Say clearly: "No tumor regions are visible in this scan."
                - Do not describe tumor types.

                If colored regions ARE present:
                Explain the scan in simple terms.

                Structure:
                1. What is visible
                2. What each colored region means (only if present)
                3. What this means for the patient

                Rules:
                - Do not assume tumors exist
                - Only describe colors that are clearly visible
                - If unsure, say no tumor is visible
                - Keep it concise and clear for a non-medical audience
                - Use medically accurate information consistent with trusted sources like PubMed and the WHO classification.
                - Always remind the user to consult a doctor for medical advice
                - Always remind the user that this is an AI interpretation and not a medical diagnosis
                - Always remind the user that the output can be incorrect
                - provide these links for further reading:https://www.cancer.gov/types/brain    and  https://www.nhs.uk/conditions/brain-tumours/   and https://www.who.int/news-room/fact-sheets/detail/cancer
                -Format all links as clickable HTML links using <a href="URL" target="_blank">text</a>.
                -Do NOT outpt plain URLs.
                """
                },
            {
                "type": "input_image",

                "image_url": f"data:image/png;base64,{image_base64}"
            },
        ],
    }],

        )

        return response.output_text

    except Exception as e:
     print("ERROR:", e)
     return str(e)

