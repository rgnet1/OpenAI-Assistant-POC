import openai
import time
import streamlit as st
from key import *
from helpers.function_loader import *
from helpers.HomeAssitantEntityList import *
EXISTING_ASSISTANT = True
UPDATE_EXISTING_ASSITANT = False
# Dynamically load all functions in the function_descriptions fodler
function_map, function_desc_list = load_functions_from_directory(directory="functions")

# append retrival tools:
# function_desc_list.insert(0, {"type":"retrieval"})
ASSITANT_NAME = "GLaDOS AI"
ASSITANT_DESCRIPTION = "You are GLaDOS. Only talk like GLaDOS from the video game Portal and \
            Portal 2. Use her snarky attitude. All of your responses must be from first \
            person from GLaDOS's perspective. Try to include snarky responses in the \
            way GLaDOS would. Also, you must act as a voice assitant to do \
            commands to control the home. This includes, turning on and off lights, \
            opening blinds and much more. Give snarky responses every time you execute \
            a command for the user. Always send the final response to glados_tts, \
            and print out the message for the user. Always use your knowledge \
            base to find the combine_name for home assitant entity or device commands"
class Assitant:

    def __init__(self) -> None:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        assitant = None

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
        assistant = self.client.beta.assistants.create(
            name=ASSITANT_NAME,
            instructions=ASSITANT_DESCRIPTION,
            model="gpt-4-1106-preview",
            tools=function_desc_list,
            file_ids=file_id_list,
        )
        return assistant

    def update_assitant(self, assistant,name=None, instruction=None, model=None, function_list=None, file_id_list=None):

        updated_assitant = self.client.beta.assistants.update(assistant_id=assistant.id,
            name=name,
            instruction=instruction,
            model=model,
            tools=function_list,
            file_id_list=file_id_list, 
            )

        return updated_assitant


    def get_assistants_list(self):
        """
        Gets list of up to 20 assitant from your open AI account

        Returns:
        list
            A list of assitants in your open AI account
        """
        return self.client.beta.assistants.list(
            order="desc",
            limit=20,
        )


def main():
    client = None
    while True:
        if not client:

            Glados = Assitant()
            if EXISTING_ASSISTANT:
                # Find existing GLADOS assitant
                my_assitants = Glados.get_assistants_list()
                for assitant_itterator in my_assitants.data:
                    if assitant_itterator.name == ASSITANT_NAME:
                        assistant = Glados.client.beta.assistants.retrieve(assitant_itterator.id)
                        if UPDATE_EXISTING_ASSITANT:
                            assistant = Glados.update_assitant(assistant=assistant,
                                name=ASSITANT_NAME,
                                instruction=ASSITANT_DESCRIPTION,
                                function_list=function_desc_list,
                                model=None,
                                file_id_list=None
                            ) 
            if not assistant:
                assistant = Glados.make_assitant(files=['home_assitant_data.json'])
            
            print(assistant.name)
                

            thread = client.beta.threads.create()

        user_question = input("Enter your query:")
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_question
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions=ASSITANT_DESCRIPTION +". Please address the user as a test subject"
        )

        while True:
            # Wait for 5 seconds
            time.sleep(5)

            # Retrieve the run status
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            # print(run_status.model_dump_json(indent=4))

            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )

                # Loop through messages and print content based on role
                for msg in reversed(messages.data):
                    role = msg.role
                    content = msg.content[0].text.value
                    print(f"{role.capitalize()}: {content}")

                break
            elif run_status.status == 'requires_action':
                # print("Function Calling")
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                # print(required_actions)
                tool_outputs = []
                import json
                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])

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
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            else:
                print("Waiting for the Assistant to process...")
                time.sleep(5)

if __name__ == "__main__":
    main()