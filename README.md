# Claude Agents

A collection of AI agents built with the Claude Agent SDK, demonstrating various use cases and implementation patterns.

## Projects

### [PM Agent](pm-agent/)
An AI-powered product manager assistant that helps with:
- Feature prioritization using RICE scoring
- User story generation
- Product metrics analysis
- Roadmap planning
- Team capacity management

## Getting Started

Each agent has its own setup instructions in its respective directory. Generally, you'll need:

1. Python 3.13+
2. [uv](https://github.com/astral-sh/uv) package manager
3. Anthropic API key ([get one here](https://console.anthropic.com))

### Setting up credentials

Create a credentials directory and add your API key:

```bash
mkdir credentials
echo "ANTHROPIC_API_KEY=your-api-key-here" > credentials/.env
```

Alternatively, set it as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Repository Structure

```
claude-agents/
├── pm-agent/          # Product Manager agent
├── credentials/       # API keys and secrets (gitignored)
├── .gitignore
└── README.md
```

## Learn More

- [Anthropic API Documentation](https://docs.anthropic.com)
- [Claude Agent SDK](https://github.com/anthropics/anthropic-sdk-python)

## License

MIT
