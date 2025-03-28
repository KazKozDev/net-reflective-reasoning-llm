<div align="center">
  <img src="https://github.com/user-attachments/assets/c8427ff2-970e-49a8-847a-5e7db3d90a76" alt="logo">
  <h2>Net Reflective Reasoning</h2>
  <p>Conducts reasoning using reflective prompt techniques and web search capability.</p>
  <p>Agent-like script.</p>
  <p>Can be useful for developers, LLM enthusiasts who need real-time explainable answers based on structured and relevant information.</p>
</div>

### Features
- Reflective multi-stage reasoning with confidence scoring and critique
- Real-time web search with smart query reformulation and result parsing
- Structured analysis pipeline: intent → search → critique → synthesis
- Fully asynchronous architecture with caching and fallback strategies

### Demo

![Net Reflective Reasoning demo](https://github.com/kazkozdev/net-reflective-reasoning-llm/blob/main/net-reasoning-demo.gif)

> The demo illustrates the system’s pipeline: it interprets the query "bitcoin exchange rate", reformulates it to "bitcoin price USD", performs web search, parses the retrieved content, and executes a multi-stage reasoning process to generate the final response — all achieved by applying refinement techniques to a relatively compact gemma2 9B parameter model, which does not inherently possess such capabilities on its own.

### Requirements

- Python 3.7+
- Ollama with Gemma2:9B
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

### License

Under the MIT License.

---
If you like this project, please give it a star ⭐

For questions, feedback, or support, reach out to:

[Artem KK](https://www.linkedin.com/in/kazkozdev/)
