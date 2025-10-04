# Cross-AGET Integration Patterns

## DeepThink ↔ llm-judge Integration

### Pattern 1: Quality Evaluation Pipeline
```python
# src/integrations/llm_judge.py
from llm_judge import LLMJudge, Category

class ResearchQualityEvaluator:
    """Use llm-judge to evaluate DeepThink's research quality"""

    def __init__(self):
        self.judge = LLMJudge()
        self.setup_categories()

    def setup_categories(self):
        """Define research quality categories"""
        self.categories = {
            "comprehensive": Category(
                name="Comprehensive Research",
                necessary_properties=[
                    "Covers multiple perspectives",
                    "Includes recent sources",
                    "Addresses core question"
                ],
                sufficient_properties=[
                    "Contains 20+ citations",
                    "Analyzes competing viewpoints",
                    "Provides actionable insights"
                ]
            ),
            "well_cited": Category(
                name="Well-Cited Research",
                necessary_properties=[
                    "Citations from authoritative sources",
                    "Proper attribution"
                ],
                typical_properties=[
                    "Mix of academic and industry sources",
                    "Recent publications (last 2 years)"
                ]
            )
        }

    async def evaluate_research(self, research_result):
        """Evaluate research quality using llm-judge"""
        evaluation = await self.judge.evaluate(
            content=research_result.content,
            categories=self.categories,
            providers=['openai', 'anthropic'],
            consensus='majority'
        )

        # Record evaluation in DeepThink's evolution
        self.record_quality_assessment(evaluation)

        return {
            "quality_score": evaluation.confidence,
            "categories_matched": evaluation.matched_categories,
            "improvement_suggestions": evaluation.feedback
        }
```

### Pattern 2: Research Validation Loop
```python
# DeepThink performs research → llm-judge validates → DeepThink learns

async def validated_research(query):
    # Step 1: DeepThink researches
    result = await deepthink.research(query)

    # Step 2: llm-judge evaluates
    quality = await llm_judge.evaluate_research(result)

    # Step 3: DeepThink learns from evaluation
    if quality["quality_score"] < 0.7:
        # Adjust routing thresholds
        deepthink.learn_from_quality_feedback(quality)
        # Potentially retry with different method
        result = await deepthink.research(query, method="deep_research")

    return result, quality
```

## DeepThink ↔ GM-RKB Integration

### Pattern 3: Knowledge Base Population
```python
# src/integrations/gm_rkb.py

class KnowledgeBasePopulator:
    """Auto-generate GM-RKB entries from research"""

    async def research_to_wiki(self, research_result):
        """Convert research into wiki-ready content"""
        wiki_entry = {
            "title": self.extract_concept_title(research_result),
            "content": self.format_for_mediawiki(research_result),
            "categories": self.identify_categories(research_result),
            "references": self.format_citations_as_references(research_result)
        }

        # Use GM-RKB's publishing system
        await gm_rkb.publish_entry(wiki_entry)

        return wiki_entry
```

## DeepThink ↔ agentic-planner-cli Integration

### Pattern 4: Research-Driven Planning
```python
# src/integrations/planner.py

class ResearchPlanner:
    """Use research to inform planning"""

    async def plan_from_research(self, goal):
        # Step 1: Research the goal domain
        research = await deepthink.research(
            f"Best practices and methods for: {goal}"
        )

        # Step 2: Extract actionable steps
        steps = self.extract_action_items(research)

        # Step 3: Feed to planner
        plan = await agentic_planner.decompose_goal(
            goal=goal,
            context=research.content,
            constraints=steps
        )

        return plan
```

## Meta-Orchestration Pattern (Modality 5)

### Pattern 5: AGET Conductor
```python
# src/orchestration/conductor.py

class AGETConductor:
    """Orchestrate multiple AGETs for complex tasks"""

    def __init__(self):
        self.agents = {
            "research": DeepThink(),
            "evaluation": LLMJudgeAGET(),
            "knowledge": GMRKBAGET(),
            "planning": AgenticPlannerAGET()
        }

    async def complex_research_pipeline(self, query):
        """Full pipeline using multiple AGETs"""

        # 1. DeepThink researches
        research = await self.agents["research"].research(query)

        # 2. llm-judge evaluates quality
        quality = await self.agents["evaluation"].evaluate(research)

        # 3. If quality good, populate knowledge base
        if quality.score > 0.8:
            wiki_entry = await self.agents["knowledge"].create_entry(research)

        # 4. Generate action plan from research
        plan = await self.agents["planning"].plan_from_research(research)

        return {
            "research": research,
            "quality": quality,
            "knowledge_entry": wiki_entry,
            "action_plan": plan
        }
```

## Communication Protocols

### Inter-AGET Message Format
```json
{
    "from_agent": "DeepThink",
    "to_agent": "llm-judge",
    "message_type": "evaluation_request",
    "payload": {
        "content": "research_content_here",
        "metadata": {
            "query": "original_query",
            "method_used": "deep_research",
            "confidence": 0.85
        }
    },
    "timestamp": "2025-09-25T14:30:00Z",
    "correlation_id": "req-123456"
}
```

### Discovery Protocol
```python
# .aget/registry.json
{
    "agent_name": "DeepThink",
    "version": "1.0.0",
    "capabilities": ["research", "routing", "citation"],
    "integrations": {
        "provides": ["research_service", "citation_validation"],
        "consumes": ["quality_evaluation", "knowledge_storage"]
    },
    "endpoints": {
        "research": "http://localhost:8001/research",
        "status": "http://localhost:8001/status"
    }
}
```

## Benefits of Cross-AGET Integration

1. **Quality Assurance**: llm-judge validates research quality
2. **Knowledge Persistence**: GM-RKB stores valuable research
3. **Actionable Insights**: agentic-planner turns research into plans
4. **Feedback Loops**: Each AGET improves others
5. **Emergent Intelligence**: Combined capabilities > sum of parts

## Implementation Priority

1. **Phase 1**: DeepThink standalone (current)
2. **Phase 2**: llm-judge integration for quality
3. **Phase 3**: GM-RKB for knowledge persistence
4. **Phase 4**: Full orchestration with all AGETs

---
*Cross-AGET Integration Patterns v1.0*
*Part of the AGET Ecosystem*