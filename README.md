# OpenAI DeepResearch AGET Cognitive Agent

A sophisticated cognitive research agent that combines OpenAI's Agents orchestration with Deep Research API, enhanced with continuous learning and intelligent routing.

## 🧠 About DeepThink

DeepThink is a meticulous research companion that doesn't just answer questions - it learns, adapts, and improves with every interaction. Built on the proven OpenAI_DeepResearch dual-implementation architecture, it intelligently routes queries to the optimal research method and continuously refines its strategies.

## ✨ Key Features

### Dual Research Engines
- **OpenAI Agents System**: Multi-agent orchestration for technical queries (30-60s)
- **Deep Research API**: Professional-grade comprehensive research (2-5 min)

### Intelligent Routing
- Auto-selects optimal method based on query analysis
- Pattern recognition improves routing accuracy over time
- Fallback mechanisms ensure reliability

### Cognitive Capabilities
- **Memory System**: Remembers successful patterns and source quality
- **Learning Loop**: Improves through usage and feedback
- **Synthesis Engine**: Combines multiple information streams
- **Citation Management**: Professional-grade citations with validation

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/OpenAI-DeepResearch-aget.git
cd OpenAI-DeepResearch-aget

# Install dependencies
pip install -r requirements.txt

# Set up environment
export OPENAI_API_KEY="your-api-key"
```

### Basic Usage
```python
from src.core.router import ResearchRouter

# Initialize the cognitive agent
agent = ResearchRouter()

# Let DeepThink handle your research
result = await agent.research(
    "What are the latest advances in LLM orchestration frameworks?"
)

print(f"Method used: {result.method}")
print(f"Research findings: {result.content}")
print(f"Citations: {result.citations}")
```

## 🏗️ Architecture

### Three-Tier Design
1. **Research Layer**: OpenAI Agents + Deep Research API
2. **Intelligence Layer**: Routing, learning, synthesis
3. **Memory Layer**: Patterns, citations, preferences

### Agent Pipeline
```
Query → Analyzer → Router → Research Engine → Synthesizer → Memory → Result
         ↑                                                      ↓
         └──────────── Learning Feedback Loop ─────────────────┘
```

## 📊 Performance

| Metric | OpenAI Agents | Deep Research API |
|--------|--------------|-------------------|
| Speed | 30-60 sec | 2-5 min |
| Depth | Good | Excellent |
| Citations | Basic | Professional |
| Customization | High | Medium |

## 🎯 Use Cases

### Technical Implementation
```python
# Quick technical questions
result = await agent.research(
    "How to implement error handling in LangChain?",
    method="agents"  # Force specific method
)
```

### Comprehensive Analysis
```python
# Deep research for strategic decisions
result = await agent.research(
    "Analyze the competitive landscape of AI agent frameworks",
    method="deep_research"  # Force comprehensive research
)
```

### Auto-Selection (Recommended)
```python
# Let DeepThink choose the best approach
result = await agent.research(
    "Your research question here"
    # No method specified - uses intelligent routing
)
```

## 📈 Continuous Learning

DeepThink improves through:
- **Pattern Recognition**: Learns optimal query-method mappings
- **Source Evaluation**: Tracks reliability of information sources
- **User Preferences**: Adapts to your research style
- **Performance Metrics**: Optimizes for speed and quality

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your-api-key
DEEP_RESEARCH_MODEL=o3-deep-research-2025-06-26
AGENT_MODEL=gpt-4o
ENABLE_LEARNING=true
CACHE_RESULTS=true
```

### Custom Settings
```python
agent = ResearchRouter(
    learning_enabled=True,
    cache_ttl=3600,
    routing_threshold=0.7,
    max_retries=3
)
```

## 📚 Documentation

- [Architecture Guide](docs/architecture.md)
- [API Reference](docs/api.md)
- [Learning System](docs/learning.md)
- [Integration Guide](docs/integration.md)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built on the foundation of OpenAI_DeepResearch, enhanced with AGET cognitive patterns.

---
*DeepThink - Your cognitive research companion*
*Version 1.0.0 | AGET Framework*