![Description of the image](https://github.com/kazkozdev/net-reflective-reasoning-llm/blob/main/net-reasoning-banner.jpg)

# Net Reflective Reasoning LLM

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Ollama-Gemma2%3A9B-green)](https://ollama.ai)

A sophisticated web-enabled Language Model framework built on Ollama, featuring advanced reasoning capabilities and automated web search integration. The system utilizes the Gemma2:9B model as its core engine while incorporating multiple reasoning stages and web search capabilities for enhanced response accuracy.

## 🎯 Main Capabilities

- **Standalone Operation**
  - Functions as a complete autonomous system
  - Independently retrieves and processes information from the web
  - Self-evaluates knowledge gaps and automatically initiates web searches
  - Performs multi-stage analysis and verification of gathered information

![Net Reflective Reasoning demo](https://github.com/kazkozdev/net-reflective-reasoning-llm/blob/main/net-reasoning-demo.gif)

- **LLM Agent Integration**
  - Can serve as a specialized web search tool for LLM agent systems
  - Perfect for integration into multi-agent architectures
  - Acts as an information retrieval and processing agent
  - Enhances other agents' capabilities with real-time web data

## 🌟 Key Features

- **Enhanced Reasoning Process**
  - Multi-stage thought process evaluation
  - Confidence scoring for each reasoning step
  - Detailed analysis and critique phases
  - Comprehensive answer synthesis

- **Integrated Web Search**
  - Automatic knowledge evaluation
  - Multi-iteration search strategy
  - Smart query generation
  - Source credibility assessment
  - Content parsing and analysis

- **Conversation Management**
  - Dynamic context management
  - Customizable system prompts
  - Conversation history tracking
  - Reasoning chain visualization

## 🚀 Technical Features

- Asynchronous processing using `asyncio` and `aiohttp`
- Caching system for search results and parsed content
- Multiple website parsing strategies (static/dynamic)
- Structured thought process using enum-based stages
- Comprehensive error handling and recovery
- Modular architecture for easy extension

## 💻 Requirements

- Python 3.7+
- [Ollama](https://ollama.com) with Gemma2:9B model
- Required Python packages:
  - aiohttp
  - requests
  - beautifulsoup4
  - duckduckgo_search
  - scrapy

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/kazkozdev/net-reflective-reasoning-llm.git
cd net-reflective-reasoning-llm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is installed and the Gemma2:9B model is available:
```bash
# Install Ollama from https://ollama.ai
ollama pull gemma2:9b
```

## 🚀 Usage

### Standalone Mode
Run the main script:
```bash
python src/main.py
```

### Integration Mode
Import and use as a web search agent in your multi-agent system:
```python
from src.net_reflective_llm import advancedgptlike

# Initialize as web search agent
search_agent = advancedgptlike(model_name="gemma2:9b")

# Use in async context
async def example():
    response, reasoning = await search_agent.model.process_query("your query here")
    return response, reasoning
```

### Available Commands:
- `clear` - Reset conversation history
- `explain` - View detailed reasoning chain for last response
- `system <prompt>` - Update system prompt
- `quit` or `exit` - Exit the program

## 🏗️ Architecture

The system consists of several key components:

1. **EnhancedLLM**: Core class managing LLM interactions and reasoning process
2. **WebSearchManager**: Handles web searches and content parsing
3. **Conversation**: Manages conversation history and context
4. **ReasoningChain**: Tracks and structures the reasoning process

### Reasoning Process Stages:
- Initial Thoughts
- Search Required
- Analysis
- Critique
- Refinement
- Final Answer

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## 💬 Questions & Support

- [Open an issue](https://github.com/kazkozdev/net-reflective-reasoning-llm/issues/new) for bug reports or feature requests
- [Join the discussion](https://github.com/kazkozdev/net-reflective-reasoning-llm/discussions) for questions or ideas

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✨ Acknowledgments

- Built on the [Ollama](https://ollama.ai) framework
- Uses the Gemma2:9B model
- Inspired by advanced reasoning techniques in AI systems