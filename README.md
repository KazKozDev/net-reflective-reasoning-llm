
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/Ollama-Gemma2%3A9B-green)](https://ollama.ai)

<p align="center"> <b>Net Reflective Reasoning</b> is a standalone agent-like script that conducts structured reasoning and searches the web for data to provide accurate answers.</p>

<p align="center">Thoughtful reasoning. Live data. </p>

Can be useful for developers, LLM enthusiasts who need real-time explainable answers based on structured reasoning and relevant information.

### Features
- Reflective multi-stage reasoning with confidence scoring and critique
- Real-time web search with smart query reformulation and result parsing
- Structured analysis pipeline: intent → search → critique → synthesis
- Fully asynchronous architecture with caching and fallback strategies

## 🎬 Demo Preview

![Net Reflective Reasoning demo](https://github.com/kazkozdev/net-reflective-reasoning-llm/blob/main/net-reasoning-demo.gif)

This demo demonstrates the system processing a user query 'bitcoin exchange rate', automatically transforming it to 'bitcoin price USD' for web search. The system then performs net scraping to gather relevant data and applies reflective reasoning methods to analyze the information before delivering comprehensive results to the user.

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
