from openai import OpenAI
import os
import base64






client = OpenAI()



def llm_response(MRI_path):



    #since keys in the venv it wont run outside it
    if not os.getenv("OPENAI_API_KEY"):
        return "Sakib: Sorry but the API key is on my local pc virtual environment so it wont work here"


    try:

        #convert image to base64 to give to llm

        with open(MRI_path,"rb")as f:

            image_base64 = base64.b64encode(f.read()).decode("utf-8")





        response = client.responses.create(

        model="gpt-4.1-mini",
        input=[{
        "role": "user",
        "content": [
            {"type": "input_text",
             
              "text": "Describe this brain MRI image in simple academic terms"},
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

