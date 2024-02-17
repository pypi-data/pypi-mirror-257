# PyExplain
This is a python library that runs directly in the user's terminal and can assist them to generate and explain code right in their terminal by simply running the following command after installation
```shell
$ pyexplain-interact
```
## Features
1. Generate python code based on natural language input.


    ![Alt installation command](images/code_generation.png)



2. Explain the code in simple english that even a 5 year old can understand.


    ![Alt installation command](images/code_explanation.png)

## Set up and usage
### Installation
You can install the library by running the command bellow
![Alt installation command](images/install.png)
### Usage
run the command below to start

```bash
$ pyexplain-interact
```
you would be prompted to enter your api key if you haven't
![Alt enter your api key](images/enter_api_key.png)


## Architecture
Below is an overview of the architecture of the library.


![Alt installation command](images/pyexplain_architecture.png)


### Major Modules

1. Prompt.<br>
   This module contains the prompts for adjusting the behaviour of the Assistant.

    ![Alt installation command](images/prompt_code.png)


2. Chat.<br>
   The chat class handles creation of assistant, chat thread and handle sending user prompts to the remote openai model.


    ![Alt installation command](images/chat_code.png)


3. Interact.<br>
   This class handles api key set up and interaction with the user throught the terminal.

   ![Alt installation command](images/interact_code.png)

4. OpenAi Functions.<br>
   These contain function descriptions that are passed to openai's api to allow it interact with the user's computer. giving it the capability to create and edit file on their computer. (This feature would be added in the future).

   ## System Evaluation

   1. Accuracy.<br>
        The system has an above average accuracy (7 out of 10) although its not as accurate as accurate cause it uses gpt-3.5 and not the bigger gpt-4
   2. Cost.<br>
      The system uses gpt-3.5 which is smaller and cheaper than gpt-4.
   3. Contextual understanding.<br>
        The conversation history is managed by openai so i give it and 8 out of 10 for contextual understanding.


   ## Limitations / opportunities
   4. Tools.<br>
        it would be nice to have a way to get the assistant to be able to create , edit files and even help the user set up a project on their computer. but its quite difficult to get the prompt that would make the tools run coherently. (Hopefully i can play with it by the weekend and get it working 😉).
    
    5. Context Length.<br>
        One of the most obvious limitations is context length. as you chat with the assistant for longer period of time it begins to find it difficult to remeber things that were said earlier in the conversation. This can be improved with used of vector storage and prompt engineering frameworks (e.g pinecone and langchain)