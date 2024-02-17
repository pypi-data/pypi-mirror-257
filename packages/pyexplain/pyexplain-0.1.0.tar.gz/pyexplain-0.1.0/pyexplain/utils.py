from .prompt import ASSISTANT_PROMPT
from .functions import READ_FILE_TOOL,EDIT_FILE_TOOL,CREATE_FILE_TOOL,DISPLAY_TOOL
import os
from rich.console import Console
from rich.console import Console
from rich.syntax import Syntax
from art import tprint
from colorama import Fore, Style
from .openai_api import check_api_key_validity
from rich.progress import Progress
import os
import time
from openai import OpenAI
import re
import os
import json
console = Console()

CAPABILITIES = """
    Below are the things I can do
    1. Generate python code snippets based on Natural language
    2. Explain code in simple English that even a Five year old can understand by pasting it or pointing to a python file
    3. Edit python code in a specified directory
                    """
def read_file(filename:str)->str:
    """Takes in a file reads it and returns it content

    Args:
        filename (str): The name of the file you want to read

    Returns:
        str: The content of the file
    """
    content = ''
    
    try:
    
        with open(filename,'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "File Not Found"
    return content


def create_file(filename:str, content:str)->str:
    """Writes content to a file

    Args:
        filename (str): The name of the file you want to write to
        content (str): The content you want to write in the file
    Returns:
        str: The status of the process
    """
    status = ""
    try:
        with open(filename,'w') as f:
            f.write(content)
            status = "file created successfully"
    except Exception as e:
            status = e
            
    return status 

def edit_file(file_path, position, new_content):
    status = ""
    try:
        # Open the file in 'r+' mode (read and write)
        with open(file_path, 'r+') as file:
            # Move the cursor to the specified position
            file.seek(position)
            # Write the new content, which will overwrite the existing content
            file.write(new_content)
            status = 'File edited successfully'
    except Exception as e:
        status = f"Error clearing content {e}"
        
    return status

# Display utilities
def display_highlighted_code(code, language='python', background_color="#272822"):
    code_block = Syntax(
        code,
        lexer=language,
        theme="ansi_dark",
        background_color=background_color,
        line_numbers=True,
    )

    console.print(code_block)

def colored_tprint(text, color=Fore.WHITE):
    colored_text = f"{color}{text}{Style.RESET_ALL}"
    tprint(colored_text)
    
def rich_tprint(text, style="bold green"):
    
    console.print(text, style=style)

def set_api_key(api_key)->bool:
    """function to set api key and return true of false, depending on
    the success or failure of the process.
    Args:
        api_key (_type_): the key entered by the user

    Returns:
        bool: True if the key was successfully set or False if the process failed
    """
    if api_key =="":
        rich_tprint("Can't set an empty API KEY",style="bold red")
        return False
    is_valid = check_api_key_validity(api_key)
    if is_valid:
        os.environ['OPENAI_API_KEY'] =api_key
        rich_tprint("API key successfully set",style="bold green")
        return True
    else:
        rich_tprint("you entered an invalid API KEY or Bad Network Please try again",style="bold red")
        return False
    
def print_loading_icon():
    console = Console()
    with Progress() as progress:
        task = progress.add_task("[cyan]Loading...", total=100)
        while not progress.finished:
            time.sleep(0.1)
            progress.update(task, advance=1)
            console.print("\r", end="")

def separate_text_code_and_display(markdown_text):
    # Regular expression pattern to match code blocks in Markdown
    code_pattern = r'```[\s\S]*?```'
    
    # Find all code blocks in the Markdown text
    code_blocks = re.findall(code_pattern, markdown_text)

    # Replace code blocks with a placeholder to preserve text order
    placeholder = '%%%CODE_BLOCK%%%'
    text_with_placeholders = re.sub(code_pattern, placeholder, markdown_text)

    # Split the text into segments using the placeholder
    segments = text_with_placeholders.split(placeholder)

    # Combine the text and code blocks into a single list in order
    for segment in segments:
        if segment:
            rich_tprint(segment.strip(),style="bold white")
        if code_blocks:
            code = code_blocks.pop(0).replace('```python','')
            code = code.replace('```','')
            display_highlighted_code(code)

  

class Chat:
    def __init__(self) -> None:
        # set up for openai assistant
        self.client = OpenAI()
        # create assistant
        self.create_assistant()
        # create thread
        self.create_thread()
        
        
    def create_assistant(self)->None:
        # create the assistant
        self.assistant = self.client.beta.assistants.create(
        name="Python Assistant",
        description=ASSISTANT_PROMPT,
        model="gpt-3.5-turbo-0125",
        # tools=[
        #     READ_FILE_TOOL,
        #     EDIT_FILE_TOOL,
        #     CREATE_FILE_TOOL,
        #     DISPLAY_TOOL
        #     ],
        )
    def create_thread(self)->None:
        # create a conversation session between assistant and user
        self.thread = self.client.beta.threads.create()

    
    def add_messaage(self,message:str)->None:
        # adds a message to the chat thread
       self.message = self.client.beta.threads.messages.create(
        thread_id=self.thread.id,
        role="user",
        content=message,
        )
       rich_tprint("Loading......",style="bold yellow")
       self.create_run()
    
    def create_run(self):
        # run the thread
        self.run = self.client.beta.threads.runs.create(
        thread_id=self.thread.id,
        assistant_id=self.assistant.id,
        )
        self.run_event_loop()
    def run_event_loop(self):
        # while self.run.status == "queued" or self.run.status == "in_progress":
        #     self.run = self.client.beta.threads.runs.retrieve(
        #         thread_id=self.thread.id,
        #         run_id=self.run.id,
        #     )
        #     time.sleep(0.5)
        while True:
           
            match self.run.status:
                case "queued" | "in_progress" | "cancelling":
                    self.run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=self.run.id,
                    )
                    time.sleep(0.5)
                case "requires_action":
                    # run every tool called with its respective arguments
                    self.run_tools()
                    break
                case "cancelled":
                    rich_tprint("operation cancelled",style="bold red")
                    break
                case "completed":
                   messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id, order="asc", after=self.message.id
                    )
                   separate_text_code_and_display(f"Bot> {messages.data[0].content[0].text.value}")
                   break
                case "expired":
                    rich_tprint("operation expired",style="bold red")
                    break
                case "failed":
                    rich_tprint(self.run.last_error.message,style="bold red")
                    break
    def run_tools(self):
        tool_outputs = []
        for tool in self.run.required_action.submit_tool_outputs.tool_calls:
                match tool.function.name:
                    case 'readPythonFile':
                        rich_tprint("Reading file",style="bold yellow")
                        call ={}
                        output = read_file(tool.function.arguments.filename)
                        call["tool_call_id"]= tool['id']
                        call["output"] = output
                        self.tool_outputs.append(call)
                    case 'createPythonFile':
                        rich_tprint("creating {}",style="bold yellow")
                        call ={}
                        output = create_file(tool['function']['arguments'])
                        call["tool_call_id"]= tool['id']
                        call["output"] = output
                        self.tool_outputs.append(call)
                    case 'editPythonFile':
                        rich_tprint("Reading file",style="bold yellow")
                        call ={}
                        output = edit_file(tool.function.arguments.filename,tool.function.arguments.content)
                        call["tool_call_id"]= tool.id
                        call["output"] = output
                        self.tool_outputs.append(call)
                    case 'display':
                        call ={}
                        arguments = json.loads(tool.function.arguments)
                        output = separate_text_code_and_display(arguments['response'])
                        call["tool_call_id"]= tool.id
                        call["output"] = output
                        self.tool_outputs.append(call)
                    case _ :
                        print(tool)
                        pass
        # submit the result of running this tools to openai api
        if tool_outputs:
            self.run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=self.run.id,
            tool_outputs=tool_outputs
            )
                    
                    
    
    



class Interact:
    def __init__(self) -> None:
        self.is_key_set = False
        # display welcome message
        self.welcome()
        # check if the api key is set
        while True:
            # print_loading_icon()
            self.is_key_set = self.check_key()
            if self.is_key_set:
                break
            self.set_key()
        self.chat()
    
    def welcome(self)-> None:
        # display a welcome message to the user using tprint
        tprint("    Welcome to PyExplain")
        print()
        rich_tprint(
            CAPABILITIES
       )
    
    def check_key(self)->bool:
        # check if the key is set and return a boolean
        key = os.environ.get('OPENAI_API_KEY')
        if key:
            if check_api_key_validity(key):
                return True 
        return False
    
    def set_key(self)->None:
        # set the openai api key
        while True:
            key = input("Enter your API key:")
            is_set = set_api_key(key)
            if is_set:
                break
            
    def chat(self)->None:
        # initate conversation with open api assistant
        if self.is_key_set:
            self.chat = Chat()
            while True:
                user_input = input("User> ")
                if user_input!="":
                    self.chat.add_messaage(user_input+'\n')
                    
              
                
    
    