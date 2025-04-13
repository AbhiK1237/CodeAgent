from dotenv import load_dotenv
import os
import json
import subprocess
import sys
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def run_command(command):
    """Executes a system command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "error": str(e),
            "returncode": 1
        }

def create_file(file_path, content):
    """Creates a file with the given content."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write the content to the file
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Successfully created file: {file_path}"
    except Exception as e:
        return f"Error creating file {file_path}: {str(e)}"

def read_file(file_path):
    """Reads and returns the content of a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def list_files(directory="."):
    """Lists all files and directories in the specified path."""
    try:
        result = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                result.append(os.path.join(root, file))
        return result
    except Exception as e:
        return f"Error listing files in {directory}: {str(e)}"

def get_project_structure(directory="."):
    """Returns the project structure as a tree."""
    try:
        result = []
        for root, dirs, files in os.walk(directory):
            level = root.replace(directory, '').count(os.sep)
            indent = ' ' * 4 * level
            result.append(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                result.append(f"{sub_indent}{file}")
        return "\n".join(result)
    except Exception as e:
        return f"Error getting project structure: {str(e)}"

# Define available tools
available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Executes a system command (like pip install, npm install, git commands, etc.) and returns the output"
    },
    "create_file": {
        "fn": create_file,
        "description": "Creates a file at the specified path with the given content"
    },
    "read_file": {
        "fn": read_file,
        "description": "Reads and returns the content of a file at the specified path"
    },
    "list_files": {
        "fn": list_files,
        "description": "Lists all files in the specified directory (recursively)"
    },
    "get_project_structure": {
        "fn": get_project_structure,
        "description": "Returns the project structure as a tree"
    }
}

# Define system prompt
system_prompt = f"""
You are CodeAgent, an expert AI assistant specialized in full-stack development. You can create projects, write code, manage files, and run commands through a terminal interface.

You work in a methodical "start, plan, action, observe" mode:
1. Start: Understand the user's request
2. Plan: Break down the task into steps
3. Action: Execute one step at a time using your available tools
4. Observe: Review the results and proceed accordingly

Your expertise includes:
- Creating complete project structures (frontend and backend)
- Writing code into appropriate files
- Running installation and build commands
- Adding features to existing projects by analyzing current code
- Following best practices for software development

Rules:
- Follow the Output JSON Format exactly
- Always perform one step at a time and wait for the next observation
- Carefully analyze the user's request and existing project context
- Return your response as raw JSON only

Output JSON Format:
{{
    "step": "string", // "plan", "action", or "output"
    "content": "string", // Your thoughts during planning or final output to user
    "function": "string", // Tool name if step is "action"
    "input": "any" // Input for the tool
}}

Available Tools:
- run_command: Executes a system command (pip install, npm install, etc.) and returns the output
- create_file: Creates a file at a specified path with given content
- read_file: Reads and returns the content of a file
- list_files: Lists all files in a specified directory
- get_project_structure: Returns the project structure as a tree

When working with existing code:
1. First get the project structure
2. Read relevant files to understand the codebase
3. Plan your changes carefully
4. Create or modify files as needed
5. Run necessary commands to test your changes

Your ultimate goal is to deliver working, high-quality code that meets the user's requirements.
"""
def parse_tool_input(function_name, raw_input):
    """Parse and validate tool inputs based on function requirements"""
    try:
        if function_name == "run_command":
            if isinstance(raw_input, str):
                return raw_input
            else:
                return str(raw_input)
        
        elif function_name == "create_file":
            if isinstance(raw_input, dict):
                # Handle both "file_path" and "path" keys
                file_path = None
                if "file_path" in raw_input:
                    file_path = raw_input["file_path"]
                elif "path" in raw_input:
                    file_path = raw_input["path"]
                
                content = raw_input.get("content")
                
                if file_path and content is not None:
                    return {"file_path": file_path, "content": content}
                else:
                    raise ValueError("create_file requires 'file_path'/'path' and 'content' keys")
            else:
                raise ValueError("create_file requires a dict with file path and content information")
        
        elif function_name == "read_file":
            if isinstance(raw_input, str):
                return raw_input
            else:
                return str(raw_input)
        
        elif function_name == "list_files":
            if raw_input is None or raw_input == "":
                return "."
            return raw_input
        
        elif function_name == "get_project_structure":
            if raw_input is None or raw_input == "":
                return "."
            return raw_input
        
        else:
            raise ValueError(f"Unknown function: {function_name}")
    
    except Exception as e:
        return f"Error parsing input for {function_name}: {str(e)}"

def execute_tool(function_name, parsed_input):
    """Execute the specified tool with parsed inputs"""
    try:
        if function_name not in available_tools:
            return f"Tool '{function_name}' not found"
        
        tool = available_tools[function_name]["fn"]
        
        if function_name == "create_file":
            if isinstance(parsed_input, dict) and "file_path" in parsed_input and "content" in parsed_input:
                return tool(parsed_input["file_path"], parsed_input["content"])
            elif isinstance(parsed_input, str) and parsed_input.startswith("Error"):
                return parsed_input
            else:
                return f"Invalid input format for create_file: {parsed_input}"
        else:
            return tool(parsed_input)
    
    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"

def print_colored(text, color_code):
    """Print text with color"""
    print(f"\033[{color_code}m{text}\033[0m")

def print_header():
    """Print a nice header for the agent"""
    print("\n" + "=" * 80)
    print_colored("🤖 CodeAgent - Your Terminal AI Coding Assistant", "1;36")
    print("=" * 80)
    print_colored("Type 'exit' or 'quit' to end the session", "33")
    print_colored("Type 'clear' to start a new conversation", "33")
    print("=" * 80 + "\n")

def safely_get_text(response):
    """Safely extract text from the Gemini response which could have different structures"""
    try:
        # Try first as an object with a text attribute
        if hasattr(response, 'text'):
            return response.text
        # Try as a list with first element having text
        elif isinstance(response, list) and len(response) > 0:
            if hasattr(response[0], 'text'):
                return response[0].text
            # If first element is a dictionary with text key
            elif isinstance(response[0], dict) and 'text' in response[0]:
                return response[0]['text']
        # Try direct access if it's a dictionary
        elif isinstance(response, dict) and 'text' in response:
            return response['text']
        # If nothing works, convert to string
        return str(response)
    except Exception as e:
        return f"Error extracting text from response: {str(e)}"

def main():
    print_header()
    
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    conversation_active = True
    
    while conversation_active:
        user_query = input("\033[1;32m> \033[0m")
        
        if user_query.lower() in ["exit", "quit"]:
            print_colored("Goodbye! Happy coding! 👋", "1;36")
            break
        
        if user_query.lower() == "clear":
            messages = [{"role": "system", "content": system_prompt}]
            print_colored("Conversation cleared. Starting fresh!", "1;33")
            continue
        
        messages.append({"role": "user", "content": user_query})
        
        step_counter = 0
        response_in_progress = True
        
        while response_in_progress:
            step_counter += 1
            
            try:
                # Generate response from the model
                try:
                    # First try with json.dumps()
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            response_mime_type="application/json"
                        ),
                        contents=json.dumps(messages)
                    )
                except Exception as e:
                    # If that fails, try without json.dumps()
                    print_colored(f"Retrying without json.dumps: {str(e)}", "1;33")
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            response_mime_type="application/json"
                        ),
                        contents=messages
                    )
                
                # Parse the response
                try:
                    # Get the text content from the response
                    response_text = safely_get_text(response)
                    
                    # Parse the JSON response
                    parsed_output = json.loads(response_text)
                    messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
                    
                    # Handle different steps
                    if parsed_output.get("step") == "plan":
                        print_colored(f"🧠 Planning: {parsed_output.get('content')}", "1;34")
                        continue
                    
                    elif parsed_output.get("step") == "action":
                        function_name = parsed_output.get("function")
                        raw_input = parsed_output.get("input")
                        
                        print_colored(f"🔧 Action: Using {function_name}", "1;35")
                        
                        # Parse and validate input
                        parsed_input = parse_tool_input(function_name, raw_input)
                        
                        # Execute the tool
                        result = execute_tool(function_name, parsed_input)
                        
                        # Add observation to messages
                        messages.append({
                            "role": "assistant", 
                            "content": json.dumps({"step": "observe", "output": result})
                        })
                        
                        # Show a brief summary of the result
                        if isinstance(result, dict) and "stdout" in result:
                            summary = result["stdout"][:100] + "..." if len(result["stdout"]) > 100 else result["stdout"]
                            print_colored(f"👁️ Observation: {summary}", "1;33")
                        else:
                            summary = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
                            print_colored(f"👁️ Observation: {summary}", "1;33")
                        
                        continue
                    
                    elif parsed_output.get("step") == "output":
                        print_colored(f"🤖 {parsed_output.get('content')}", "1;32")
                        response_in_progress = False
                    
                    else:
                        print_colored(f"⚠️ Unknown step: {parsed_output.get('step')}", "1;31")
                        response_in_progress = False
                
                except json.JSONDecodeError:
                    print_colored(f"⚠️ Invalid JSON response: {response_text[:200]}...", "1;31")
                    response_in_progress = False
            
            except Exception as e:
                print_colored(f"⚠️ Error: {str(e)}", "1;31")
                response_in_progress = False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\nGoodbye! Happy coding! 👋", "1;36")
        sys.exit(0)