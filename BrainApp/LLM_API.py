from openai import OpenAI
import os
import base64








def llm_response(overlay_path, mri_path, unique_classes):

    #removing the background class from mask classes
    filtered_classes = [int(c) for c in unique_classes if c != 0]


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

        model="gpt-4.1",
        input=[{
        "role": "user",
        "content": [
            {"type": "input_text",
             
              "text": f"""

              Detected tumour-related regions (excluding background): {filtered_classes}

              You are given two images:
              1. A grayscale image intended to represent an MRI scan
              2. A segmentation overlay highlighting tumor regions in color

              IMPORTANT (STRICT RULES):

              - Only the detected regions in {filtered_classes} are actually present in the scan. 
              - Do NOT mention class numbers or internal labels
              - Translate all detected regions into clear, user-friendly terms:
                - red = necrotic core
                - green = edema (swelling)
                - blue = active tumour
              - If no regions are detected, clearly state that no tumour is visible
              - Do NOT override detected regions using visual judgement

              Use both images together:
                - Use the overlay to locate tumor regions
                - Use the MRI to describe how regions visually appear in the image

              VISUAL PRIORITY RULE (CRITICAL):

              You MUST evaluate the MRI image FIRST before using segmentation data.

              If the MRI image is classified as:
                - BLANK, or
                - NON-DIAGNOSTIC

              Then:
                - You MUST ignore the detected regions: {filtered_classes}
                - You MUST NOT describe tumour regions
                - You MUST NOT assume anatomical structure

              Only if the MRI image is VALID:
                - Then use the detected regions to guide the explanation





             IMAGE VALIDITY CLASSIFICATION (HIGHEST PRIORITY - MUST BE FOLLOWED):

                First, determine which ONE of the following applies:

                A. BLANK IMAGE  
                - Completely black or near-uniform  
                - No visible shapes, edges, or intensity variation  

                B. NON-DIAGNOSTIC IMAGE  
                - Some signal present (e.g., small bright spots or noise)  
                - No clear anatomical structure  
                - No identifiable brain shape  

                C. VALID MRI IMAGE  
                - Clear anatomical structure visible  

                ---

                CRITICAL INSTRUCTION:

                You MUST follow this control flow:

                IF A (BLANK IMAGE):
                - Output ONLY this:
                "The provided image appears to be blank and does not contain any meaningful visual information. Therefore, a meaningful interpretation cannot be performed."
                - STOP. Do NOT continue.

                IF B (NON-DIAGNOSTIC IMAGE):
                - Output ONLY this:
                "The image contains some visual signal; however, it does not display clear or identifiable anatomical structures. Therefore, a meaningful interpretation of brain features cannot be performed."
                - STOP. Do NOT continue.

                IF C (VALID MRI IMAGE):
                - Continue with the structured response below.



                
             Structure your response exactly as follows  :



                1. MRI Description

                 Describe ONLY what is clearly visible in the MRI image:

                    - brightness
                    - shapes
                    - textures
                    - any visible abnormalities

                    If the image is unclear or lacks detail, explicitly say that instead of guessing.
                    Do NOT assume typical brain anatomy, structure or symmetry unless it is clearly visible in the MRI.


                2. Identified Tumor Regions (ONLY if MRI is VALID)

                    Clearly state which tumour-related regions are present (based ONLY on detected regions).

                    Explain each region in simple terms:
                        - what it represents
                        - where it appears

                     Do NOT mention class numbers or internal labels. Only use user-friendly terms (necrotic core, edema, active tumour).

                


            

                3.  Guided Visual Explanation (step-by-step)

                    Write a numbered guide (Step 1, Step 2, etc.)

                    Guide the user visually:
                    - Start with the most obvious abnormal region
                    - Then move to smaller or less obvious areas

                    For each step:
                    - Tell the user WHERE to look
                    - Describe WHAT they should see (brightness, shape, texture)
                    - Explain HOW it differs from normal tissue
                    - Link it to the identified region ONLY if clearly visible

                    If something is not clearly visible, say that.
                    Avoid generic statements.

                4. Interpretation (Non-diagnostic)  

                    Explain what these findings may indicate in simple terms.
                    Do NOT make medical claims or diagnoses.


                5. Important Disclaimer:

                    Always include ALL of the following clearly:

                    - This system is for educational purposes only  
                    - The segmentation and explanation are generated by AI and may be inaccurate  
                    - The results should NOT be used for medical diagnosis  
                    - Users must consult a qualified medical professional  

             GENERAL RULES:
               - Keep language simple and clear
               - Do not use technical/internal model terms
               - Do not guess or hallucinate details
               - Base explanations only on visible evidence + detected regions


             Educational resource (Manditory):

                 ALWAYS provide these links to the user and tell them it can be used for further reading on brian tumors

                
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

