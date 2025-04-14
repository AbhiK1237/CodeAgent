# CodeAgent: Terminal-Based AI Coding Assistant

CodeAgent is a powerful terminal-based AI coding assistant that helps you create, modify, and manage software projects directly from your command line interface. Leveraging the capabilities of Google's Gemini API, CodeAgent can understand natural language requests and translate them into actionable code and file operations.

##DEMO
<video src="/Assets/demo.mov" controls></video>

## Features

- **Terminal-Based Interface**: Operate completely within your terminal environment with no GUI requirements.
- **Full-Stack Project Development**: Generate complete project structures, including both frontend and backend components.
- **File Operations**: Create, read, and manage files with simple natural language commands.
- **Code Generation**: Generate high-quality code based on your specifications.
- **Command Execution**: Run system commands like `pip install`, `npm install`, and more directly through the agent.
- **Project Understanding**: The agent can analyze existing projects to make appropriate modifications.
- **Conversational Context**: Maintain context throughout a session for iterative development.
- **Color-Coded Output**: Easily distinguish between different types of information in the terminal.

## Requirements

- Python 3.6+
- Google Gemini API key (free tier)
- Internet connection for API access

## Installation

1. Clone this repository or download the script:

```bash
git clone https://github.com/yourusername/codeagent.git
cd codeagent
```

2. Create a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install the required packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

If the requirements.txt file doesn't exist, create one with these contents:
```
python-dotenv==1.0.0
google-generativeai==0.3.1
google-genai==1.10.0
```

4. Get a Gemini API key:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a free account if you don't have one
   - Generate an API key

5. Create a `.env` file in the project directory with your Gemini API key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

1. Ensure your virtual environment is activated
2. Run the script:

```bash
python codeagent.py
```

3. Once the CodeAgent interface appears, you can start interacting with it using natural language commands:

```
> create a simple tic-tac-toe game using python
```

4. The agent will process your request in steps:
   - Planning: Breaking down the task
   - Action: Executing tasks like creating files or running commands
   - Observation: Showing results of actions
   - Output: Providing final feedback

5. Special commands:
   - Type `exit` or `quit` to end the session
   - Type `clear` to start a new conversation

## Example Interactions

### Creating a New Project

```
> create a simple Flask API with two endpoints
```

### Adding Features to Existing Code

```
> add user authentication to my web application
```

### Running System Commands

```
> install the required packages for a React project
```

### Reading and Understanding Code

```
> analyze the performance of this sorting algorithm
```

## How It Works

CodeAgent works using a "start, plan, action, observe" workflow:

1. **Start**: Understanding your request
2. **Plan**: Breaking down the task into steps
3. **Action**: Executing one step at a time using available tools
4. **Observe**: Reviewing results and proceeding accordingly

The agent has access to several tools:
- `run_command`: Execute system commands
- `create_file`: Create new files with content
- `read_file`: Read existing files
- `list_files`: List files in a directory
- `get_project_structure`: Display the project structure as a tree

## Troubleshooting

- **API Key Issues**: Ensure your Gemini API key is correct and properly set in the `.env` file.
- **Package Errors**: Make sure all required packages are installed.
- **JSON Response Errors**: The agent may occasionally encounter JSON parsing issues. Try rephrasing your request or clearing the conversation.
- **Virtual Environment**: If you're having import errors, check that your virtual environment is activated.

## Limitations

- **Free API Tier**: This project uses the free Gemini API, so it's best suited for simple projects and smaller code tasks. Complex or large-scale applications may exceed API limits or response capabilities.
- The agent operates within the constraints of the underlying Gemini model.
- Complex project structures may require breaking down into smaller tasks.
- API request limits may apply based on your Gemini API usage tier.
- Long code generation tasks might be truncated due to token limitations of the free API.

## Best Practices

- Focus on creating simple, focused projects rather than complex applications
- Break down large tasks into smaller, more manageable requests
- Use the `clear` command to start fresh when switching between unrelated tasks
- Monitor your API usage to avoid hitting rate limits

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve CodeAgent.

## License

[MIT License](LICENSE)
