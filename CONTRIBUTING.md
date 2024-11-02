# Contributing to Net Reflective Reasoning LLM

We love your input! We want to make contributing to Net Reflective Reasoning LLM as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Quick Start

1. Fork the repository
2. Create your branch: `git checkout -b feature/YourFeature`
3. Make your changes
4. Test your changes
5. Create a Pull Request

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/KazKozDev/Net_Reflective_Reasoning_LLM.git
cd Net_Reflective_Reasoning_LLM
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and the Gemma2:9B model:
```bash
# Install Ollama from https://ollama.ai
ollama pull gemma2:9b
```

## Making Changes

1. Make sure you're working with the latest version:
```bash
git pull origin main
```

2. Create your feature branch:
```bash
git checkout -b feature/YourFeature
```

3. Make your changes
4. Test your changes
5. Commit your changes:
```bash
git add .
git commit -m "Add feature: description"
```

## Code Style

- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and single-purpose
- Follow PEP 8 guidelines
- Maximum line length: 100 characters

## Testing

Before submitting your changes:
1. Make sure the code runs without errors
2. Test with different prompts and queries
3. Check error handling
4. Verify web search functionality
5. Test conversation management

## Pull Request Process

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Push to your fork
7. Create a Pull Request from your fork to our main branch
8. Describe your changes in detail
9. Link any related issues
10. Wait for review

## Bug Reports

To report a bug, [create a new issue](https://github.com/KazKozDev/Net_Reflective_Reasoning_LLM/issues/new) with the "bug" label. When reporting bugs, please include:

1. A quick summary and/or background
2. Steps to reproduce
   - Be specific!
   - Give sample code if you can
3. What you expected to happen
4. What actually happens
5. Your environment details:
   - OS version
   - Python version
   - Ollama version
   - Gemma2:9B model version
6. Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! To propose a new feature, [create a new issue](https://github.com/KazKozDev/Net_Reflective_Reasoning_LLM/issues/new) with the "enhancement" label and include:

1. Clear description of the feature
2. Use cases
3. Potential implementation approach
4. Why this feature would be useful

## Questions?

Have questions or need help? Here are some ways to get assistance:

- [Create a new discussion](https://github.com/KazKozDev/Net_Reflective_Reasoning_LLM/discussions)
- [Check existing issues](https://github.com/KazKozDev/Net_Reflective_Reasoning_LLM/issues) for similar questions
- [Create a new issue](https://github.com/KazKozDev/Net_Reflective_Reasoning_LLM/issues/new) with the "question" label

## License

By contributing, you agree that your contributions will be licensed under the MIT License. See the [LICENSE](LICENSE) file for details.