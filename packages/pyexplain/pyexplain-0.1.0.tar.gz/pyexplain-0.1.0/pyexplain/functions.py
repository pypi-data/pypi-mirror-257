# define all the tools you wold need

READ_FILE_TOOL = {
    "type": "function",
    "function": {
      "name": "readPythonFile",
      "description": "Read the contents of a python file",
      "parameters": {
        "type": "object",
        "properties": {
          "filename": {"type": "string", "description": "The name of the file whose content you want to read",},
        },
        "required": ["filename"]
      }
    } }


EDIT_FILE_TOOL = {
    "type": "function",
    "function": {
      "name": "editPythonFile",
      "description": "Edits the contents of a python file. only use when user asks you to explicitly to edit a file",
      "parameters": {
        "type": "object",
        "properties": {
          "filename": {"type": "string", "description": "The name of the file you want to create",},
          "position": {"type": "integer", "description": "The position you want to put your cursor at",},
          "new_content": {"type": "string", "description": "The new content you want to insert in the file",},
        },
        "required": ["filename","position","new_content"]
      }
    } }


CREATE_FILE_TOOL = {
    "type": "function",
    "function": {
      "name": "createPythonFile",
      "description": "creates a new python file and adds content to it. only use when user asks you explicitly to create a file",
      "parameters": {
        "type": "object",
        "properties": {
          "filename": {"type": "string", "description": "The name of the file you want to create",},
          "content": {"type": "string", "description": "The content you want to insert in the file",},
        },
        "required": ["filename","content"]
      }
    } }

DISPLAY_TOOL = {
    "type": "function",
    "function": {
      "name": "display",
      "description": "Display your response to the user",
      "parameters": {
        "type": "object",
        "properties": {
          "response": {"type": "string", "description": "Something you want to show the user",},
        },
        "required": ["response"]
      }
    } }

