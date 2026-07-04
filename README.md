# Nokes AI

A production-ready AI assistant system with conversational capabilities, memory management, and multi-purpose intelligence.

## Features

- **Conversational AI**: Natural language understanding and generation
- **Memory System**: Vector embeddings for context retention
- **Multi-Mode**: API server, CLI, and programmatic usage
- **Extensible**: Easy plugin architecture for custom capabilities
- **Production Ready**: Logging, error handling, Docker support
- **Fast**: Built on FastAPI for high performance

## Quick Start

### Prerequisites
- Python 3.10+
- pip/poetry
- OpenAI or Anthropic API key

### Installation

```bash
git clone https://github.com/naasifveroni-creator/nokes-ai.git
cd nokes-ai
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:

```env
LLM_PROVIDER=openai  # or anthropic
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
NOKES_HOST=0.0.0.0
NOKES_PORT=8000
LOG_LEVEL=INFO
```

### Run the Server

```bash
python -m nokes.api.server
```

API available at `http://localhost:8000`

### CLI Usage

```bash
python -m nokes.cli.main chat
python -m nokes.cli.main chat --prompt "What is artificial intelligence?"
python -m nokes.cli.main analyze --text "Your text here"
```

## Project Structure

```
nokes/
  core/              AI engine and LLM interfaces
  memory/            Vector store and retrieval
  api/               FastAPI routes and handlers
  cli/               Command-line interface
  models/            Data models and schemas
  utils/             Helper functions and utilities
  tests/             Unit and integration tests
docker/            Container configurations
```

## API Endpoints

- `POST /chat` - Send a message and get a response
- `POST /analyze` - Analyze text content
- `POST /reset` - Reset conversation state
- `GET /health` - Health check

## Development

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black nokes/ tests/

# Lint
flake8 nokes/
```

## Docker

```bash
docker build -f docker/Dockerfile -t nokes:latest .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8000:8000 nokes:latest
```

Or use docker-compose:

```bash
docker-compose up
```

## Usage Examples

### Python API

```python
import asyncio
from nokes.core.engine import NokesEngine

async def main():
    engine = NokesEngine(llm_provider="openai")
    response = await engine.chat("Hello Nokes!")
    print(response.content)

asyncio.run(main())
```

### REST API

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is machine learning?"}'
```

## Contributing

Pull requests welcome! Please ensure tests pass and code is formatted.

## License

MIT
