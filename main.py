import openai
import time
import json
from key import *
from helpers.function_loader import *
from helpers.HomeAssitantEntityList import *
from constants import *

# Special functions that i want to use in the main class
# from functions.GLaDOSTTS import GLaDOSTTS

# Dynamically load all functions in the function_descriptions fodler
function_map, function_desc_list = load_functions_from_directory(directory="functions")

# append retrival tools:
function_desc_list.insert(0, {"type":"retrieval"})




class Assitant:

    def __init__(self, name=ASSITANT_NAME, instructions=ASSISTANT_DESCRIPTION, gpt_model=GPT_MODEL) -> None:
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.assistant = None
        self.name = name
        self.instructions = instructions
        self.gpt_model = gpt_model

    def upload_assitant_files(self, file_names_list: []):
        """
        Uploads files to OpenAI for assistant knowledge base.

        Parameters:
        file_names_list : list of str
            List of file path/names to upload.

        Returns:
        list
            A list of OpenAI file ids.
        """
        file_list = []
        for file in file_names_list:
            print(f"uploading file: {filename}")
            file_list.append(self.client.files.create(
                file=open(filename, "rb"),
                purpose="assistants"
            ).id)

        return file_list


    def make_assitant(self, files=None):
        """
        Creates OpenAI assitant

        Parameters:
        files : list of str
            List of files/path/names to uplaod

        Returns:
        assistant
            Open AI assitant object
        """
        # upload files
        file_id_list = None
        if files:
            file_id_list = self.upload_assitant_files(files)

        
        print("Done uploading file... creating assitant")
        self.assistant = self.client.beta.assistants.create(
            name=self.name,
            instructions=self.instructions,
            model=self.gpt_model,
            tools=function_desc_list,
            file_ids=file_id_list,
        )

    def update_assitant(self,name="NOT_GIVEN", instructions="NOT_GIVEN", model="NOT_GIVEN", function_list="NOT_GIVEN", file_id_list="NOT_GIVEN"):

        self.assistant = self.client.beta.assistants.update(assistant_id=self.assistant.id,
            name=name,
            instructions=instructions,
            # model=model,
            tools=function_list,
            # file_ids=file_id_list,
        )
        self._update_assitant_vars()

    def get_assistants_list(self, assitant_count_limit=20):
        """
        Gets list of up to 20 assitant from your open AI account

        Returns:
        list
            A list of assitants in your open AI account
        """
        return self.client.beta.assistants.list(
            order="desc",
            limit=assitant_count_limit,
        )

    def _update_assitant_vars(self):
        """
        Updates the local class' variables
        """
        self.name = self.assistant.name
        self.gpt_model = self.assistant.model
        self.instructions = self.assistant.instructions

    def find_existing_assitant(self):
        my_assitants = self.get_assistants_list()
        for assitant_itterator in my_assitants.data:
            if assitant_itterator.name == ASSITANT_NAME:
                self.assistant = self.client.beta.assistants.retrieve(assitant_itterator.id)
                self._update_assitant_vars()



def main():
    client = None
    # tts = GLaDOSTTS()
    Glados = Assitant()
    if EXISTING_ASSISTANT:
        Glados.find_existing_assitant()
    if not Glados.assistant:
        Glados.make_assitant(files=['home_assitant_data.json'])
    elif UPDATE_EXISTING_ASSITANT:
        Glados.update_assitant(name=ASSITANT_NAME,
            instructions=ASSISTANT_DESCRIPTION,
            function_list=function_desc_list, 
        ) 
            
    print(Glados.name)
    thread = Glados.client.beta.threads.create()     
    while True:
        user_question = input("Enter your query: ")
        message = Glados.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_question
        )

        run = Glados.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=Glados.assistant.id,
            instructions=ASSISTANT_DESCRIPTION +". Please address the user as a test subject"
        )
        speak = False
        while True:
                       
            # Retrieve the run status
            run_status = Glados.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            # print(run_status.model_dump_json(indent=4))

            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = Glados.client.beta.threads.messages.list(
                    thread_id=thread.id
                )

                # Loop through messages and print content based on role
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    if role == "assistant":
                        content_split = content.split("\n")
                        for paragraph in content_split:
                            function_map["gladosTTS"](paragraph, DEFAULT_SPEAKER_VOLUME)
                            print(paragraph)
                            # tts.run_function(message=paragraph, volume=DEFAULT_SPEAKER_VOLUME)
                            # time.sleep(10)
                        # print(f"{role.capitalize()}: {content}")
                    # if speak:
                    #     speak = False
                        break
                    

                break
            elif run_status.status == 'requires_action':
                # print("Function Calling")
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                # print(required_actions)
                tool_outputs = []
                speak = any(action['function']['name'] == "gladosTTS" for action in required_actions["tool_calls"])
                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])
                    print(f"Calling Function:{func_name}")
                    if func_name in function_map:
                        output = function_map[func_name](**arguments)
                        tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": output
                        })
                    else:
                        raise ValueError(f"Unknown function: {func_name}")
                # print(tool_outputs)
                print("Submitting outputs back to the Assistant...")
                Glados.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            else:
                print("Waiting for the Assistant to process...")
            time.sleep(5)

if __name__ == "__main__":
    main()