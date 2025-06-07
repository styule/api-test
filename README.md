# OpenAI Python CLI

Minimal command-line utility for querying OpenAI chat models.

## Quick start

```bash

git clone https://github.com/styule/api-test.git
cd api-test
python -m venv .venv
.\.venv\Scripts\activate       # PowerShell
pip install -r requirements.txt
setx OPENAI_API_KEY "sk-..."   # once, or create .env
python example.py "Hello!"

## Road-map

- **CI workflow**: automated linting & tests on every push  
- **Unit tests**: add `pytest` mocks for `ask_openai`  
- **Prompt modules**: support embeddings and image generation endpoints  
- **Packaging**: publish to PyPI as `openai-cli` for `pip install openai-cli`