from openai import OpenAI
import os
import base64








def llm_response(overlay_path, mri_path, unique_classes):


    #since keys in the venv it wont run outside it
    if not os.getenv("OPENAI_API_KEY"):
        return "Sakib: Sorry but the API key is not found, please find the key attached in cw submission and install it to your environment."
    
    client = OpenAI()

    try:
        #convert mri image to json to give to llm
        with open(mri_path,"rb")as f:

            mri_base64 = base64.b64encode(f.read()).decode("utf-8")


        #convert overlay image to json to give to llm
        with open(overlay_path,"rb")as f:

            image_base64 = base64.b64encode(f.read()).decode("utf-8")

        

        
        
        

        #create the prompt for llm

        response = client.responses.create(

        model="gpt-4.1-mini",
        input=[{
        "role": "user",
        "content": [
            {"type": "input_text",
             
              "text": f"""

              Detected classes from segmentation model: {unique_classes}

              IMPORTANT (STRICT RULES):
                - Class 1 = red (necrotic core)
                - Class 2 = green (edema)
                - Class 3 = blue (active tumor)

                - Only the classes present in {unique_classes} are actually present in the scan.
                - If a class is NOT in {unique_classes}, you MUST say it is NOT present.
                - If a class IS in {unique_classes}, you MUST say it IS present.
                - Do NOT override this using visual judgement.
                - The overlay image may be misleading due to blending — trust the class list first.


                You are given two images:
                1. The first image is the original MRI scan (grayscale).
                2. The second image is a segmentation overlay showing tumor regions.

                Use both images together:
                - Use the overlay (second image) to locate tumor regions
                - Use the MRI (first image) to describe how those regions look visually

                Do NOT rely only on colors. Always describe brightness, texture, shape, and structure in the MRI image.

                Colors (if present):
                - red = necrotic core
                - green = edema (swelling)
                - blue = active tumor

                IMPORTANT:
                - The presence of tumor regions MUST be determined ONLY from the detected classes: {unique_classes}.
                - Do NOT decide tumor presence based on visual inspection of colors.

                If none of the classes 1, 2, or 3 are in {unique_classes}:
                - Say clearly: "No tumor regions are visible in this scan."
                - Do NOT describe tumor types.
                - Do NOT provide guided visual identification for tumors.

            

                If any of the classes 1, 2, or 3 are in {unique_classes}:
                - Tumor regions ARE present.
                - You MUST explicitly state which regions are present based on the classes.

                Explain the scan in simple terms.

                Structure:

                1. What is visible  
                    Describe ONLY what is clearly visible in the MRI image.

                    - Focus on brightness, shapes, and any visible regions
                    - Mention if the image is mostly dark, unclear, or only partially visible
                    - Describe any noticeable differences in brightness or texture

                    Do NOT:
                    - Assume full brain structure is visible
                    - Describe symmetry or normal anatomy unless clearly seen
                    - Use generic descriptions of how a brain "normally" looks

                    If the image lacks clear detail, explicitly say that instead of guessing.

                2. What each colored region means (only if present)  
                Explain each visible color clearly and simply.

                3. Guided visual identification using the MRI image (MOST IMPORTANT)

                    This section MUST be written as a clear numbered step-by-step guide.

                    Use numbered steps (Step 1, Step 2, Step 3, etc.).
                    Do NOT use bullet points in this section.

                    IMPORTANT: Base your explanation strictly on what is visually observable in THIS MRI image.

                    - Do NOT rely on general textbook descriptions unless they clearly match what is visible.
                    - Only describe features that you can actually see in the MRI.
                    - If a feature (e.g., necrotic core, edema, active tumor) is not clearly distinguishable, say that it is not clearly visible.
                    - Do not assume brightness patterns (e.g., "dark center" or "bright region") unless they are clearly present.
                    - Always prioritise direct visual evidence over typical medical expectations.

                    Visual order rule:
                    Always guide the user from the most visually obvious feature to the least obvious:

                    1. Start with the largest or most noticeable abnormal region
                    2. Then move inward to more specific regions
                    3. Then describe smaller internal variations

                    Guide the user as if they are actively looking at the MRI:

                    Step 1: Tell the user where to look first (e.g., center, edges, left or right side), focusing on the most noticeable abnormal region.

                    Step 2: Describe what they should notice in that area using visual features such as brightness, texture, and shape.
                    Use cautious language such as "you may notice" or "this area appears".

                    Step 3: Ask the user to compare this region with normal brain tissue, which appears smoother and more uniform.

                    Step 4: Explain what this visible difference may correspond to (e.g., edema, active tumor, necrotic core), only if it clearly matches the image.

                    Continue with additional numbered steps, moving from larger regions to smaller internal details.

                    For each tumor-related region (if clearly visible), include:
                    - WHERE it is located (center, inside, surrounding, outer area)
                    - HOW it looks in the MRI (brightness, texture, shape)
                    - HOW the user can recognise it visually

                    Always describe visual differences:
                    brighter vs darker
                    smooth vs irregular
                    well-defined vs diffuse (spread-out)

                    Make the explanation feel like instructions the user can follow with their eyes.

                    The goal is to help the user think:
                    "Oh, I can see it now."

                    Avoid generic statements like:
                    "There is a tumor present"

                    Always guide observation step-by-step.

                4. What this means for the patient  
                Explain in simple, non-diagnostic terms. Avoid making definitive clinical claims.

                5. - Always remind the user to consult a doctor for medical advice
                   - Always remind the user that this is an AI interpretation and not a medical diagnosis
                   - Always remind the user that the output can be incorrect

                Rules:
                - Do not assume tumors exist
                - Only describe colors that are clearly visible
                - If unsure, say no tumor is visible
                - Keep it concise and clear for a non-medical audience
                - Use medically accurate information consistent with trusted sources like PubMed and the WHO classification.
                
                - provide these links for further reading:https://www.cancer.gov/types/brain    and  https://www.nhs.uk/conditions/brain-tumours/   and https://www.who.int/news-room/fact-sheets/detail/cancer
                -Format all links as clickable HTML links using <a href="URL" target="_blank">text</a>.
                
                """
                },
            {
                "type": "input_image",

                "image_url": f"data:image/png;base64,{mri_base64}"
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

