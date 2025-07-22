# Job Requirement Generator

A job requirement generation system built with OpenAI Agents framework.

## Features

- **Intelligent JD Parsing**: Uses LLM to parse detailed job descriptions into structured format
- **Conversation Flow**: Guides users through questions when detailed JD is not available
- **Modular Design**: Clean separation of concerns with multiple agents
- **Environment-based Configuration**: Secure API key management via .env files

## Project Structure

```
job_requirement_generator/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration settings
├── agent_modules/
│   ├── __init__.py
│   ├── orchestrator.py      # Main orchestrator agent
│   └── jd_parser.py        # JD parsing agent
├── tools/
│   ├── __init__.py
│   ├── llm_tools.py        # LLM utility functions
│   └── formatter.py        # Output formatting
├── utils/
│   ├── __init__.py
│   └── session_manager.py  # Session management
├── docs/
│   └── scenario.md         # Scenario documentation
├── main.py                 # Main entry point
├── pyproject.toml         # Project configuration and dependencies
├── env.example            # Environment variables example
└── README.md             # This file
```

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd job_requirement_generator
```

2. **Install dependencies**:
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

3. **Set up environment variables**:
```bash
cp env.example .env
# Edit .env file with your OpenAI API key
```

## Usage

### Basic Usage

```python
from agent_modules.orchestrator import OrchestratorAgent

# Initialize the orchestrator
orchestrator = OrchestratorAgent()

# Process a detailed job description (Scenario 1)
jd_text = """
Senior Software Engineer

We are looking for a Senior Software Engineer with 5+ years of experience in Python, 
JavaScript, and cloud technologies. The ideal candidate should have experience with 
microservices architecture, Docker, and Kubernetes. Strong problem-solving skills 
and excellent communication abilities are required.
"""

result = orchestrator.process_input(jd_text)
print(json.dumps(result, indent=2))
```

### Running the Example

```bash
# Using uv
uv run main.py

# Or using python directly
python main.py
```

## Configuration

The system uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `MODEL_NAME`: OpenAI model to use (default: gpt-4)
- `MAX_TOKENS`: Maximum tokens for responses (default: 2000)
- `TEMPERATURE`: Response creativity (default: 0.1)

## Architecture

### Agents

1. **Orchestrator Agent**: Main controller that determines scenario and routes to appropriate agents
2. **JD Parser Agent**: Handles detailed job description parsing using LLM

### Tools

1. **LLM Tools**: Core LLM-based functions for scenario detection, JD parsing, and question generation
2. **Formatter**: Ensures output format consistency

### Workflow

1. **Scenario Detection**: LLM determines if input contains detailed JD or needs conversation
2. **JD Parsing**: For detailed JD, extracts structured information using LLM
3. **Question Generation**: For incomplete input, generates structured questions
4. **Output Formatting**: Ensures consistent JSON output format

## Output Format

### Scenario 1 (Detailed JD)
```json
{
  "session_id": "uuid",
  "requirements": {
    "title": "Senior Software Engineer",
    "description": "Senior software engineering role",
    "must_have": {
      "technical_skills": ["Python", "JavaScript", "Docker"],
      "domain_experience": ["microservices", "cloud platforms"],
      "soft_skills": ["problem-solving", "communication"]
    },
    "nice_to_have": ["machine learning", "data engineering"]
  }
}
```

### Scenario 2 (Need Conversation)
```json
{
  "session_id": "uuid",
  "questions_with_options": [
    {
      "question": "What is the primary role type?",
      "options": [...],
      "allow_custom_input": true,
      "required": true
    }
  ]
}
```

## Development

### Adding New Features

1. **New Agent**: Create in `agent_modules/` directory
2. **New Tool**: Create in `tools/` directory
3. **Configuration**: Update `config/settings.py`

### Testing

```bash
# Run the main example
uv run main.py

# Test specific scenarios
uv run python -c "from agent_modules.orchestrator import OrchestratorAgent; o = OrchestratorAgent(); print(o.process_input('test input'))"

# Run tests (if available)
uv run pytest
```

## Security

- API keys are stored in `.env` file (not committed to repository)
- Environment variables are used for all sensitive configuration
- `.gitignore` excludes sensitive files

## Contributing

1. Follow the existing code structure
2. Add author information to new files
3. Use English comments and documentation
4. Test your changes before submitting

## License

[Add your license information here] 