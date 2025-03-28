<p align="center">
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Python Version">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://ollama.ai">
    <img src="https://img.shields.io/badge/Ollama-Gemma2%3A9B-green" alt="Ollama">
  </a>
</p>


<p align="center"> <b>Net Reflective Reasoning</b> conducts structured reasoning using reflective prompt techniques and web search capability.</p>

<p align="center">Agent-like script.</p>

Can be useful for developers, LLM enthusiasts who need real-time explainable answers based on structured and relevant information.

### Features
- Reflective multi-stage reasoning with confidence scoring and critique
- Real-time web search with smart query reformulation and result parsing
- Structured analysis pipeline: intent → search → critique → synthesis
- Fully asynchronous architecture with caching and fallback strategies

### Demo

![Net Reflective Reasoning demo](https://github.com/kazkozdev/net-reflective-reasoning-llm/blob/main/net-reasoning-demo.gif)

> The demo illustrates the system’s pipeline: it interprets the query "bitcoin exchange rate", reformulates it to "bitcoin price USD", performs web search, parses the retrieved content, and executes a multi-stage reasoning process to generate the final response.

### Requirements

- Python 3.7+
- [Ollama](https://ollama.com) with Gemma2:9B model
- Required Python packages:
  - aiohttp
  - requests
  - beautifulsoup4
  - duckduckgo_search
  - scrapy

### Installation

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

### Reasoning Process Stages:
- Initial Thoughts
- Search Required
- Analysis
- Critique
- Refinement
- Final Answer

## 📝 License

This project is licensed under the MIT License.

