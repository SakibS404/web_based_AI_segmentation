from openai import OpenAI
import os
import base64






client = OpenAI()



def llm_response(image_path):



    #since keys in the venv it wont run outside it
    if not os.getenv("OPENAI_API_KEY"):
        return "Sakib: Sorry but the API key is on my local pc virtual environment so it wont work here"


    try:

        #convert image to base64 to give to llm

        

        with open(image_path,"rb")as f:

            image_base64 = base64.b64encode(f.read()).decode("utf-8")





        response = client.responses.create(

        model="gpt-4.1-mini",
        input=[{
        "role": "user",
        "content": [
            {"type": "input_text",
             
              "text":("This is a brain MRI with tumor segmentation overlay (red = necrotic core, green = edema, blue = enhancing tumor)."
              "First, describe the MRI findings in clear academic terms. Then explain what the colored tumor regions represent. Finally,"
              "discuss what these findings may indicate clinically. Use a professional tone but ensure the explanation is understandable to a general audience. "
                )},
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

