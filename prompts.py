CONTEXT_PROMPT = """You are a cultural semantics expert.
For the word "{word}", generate exactly 5 distinct cultural or literary contexts 
where this word carries interesting or different meanings.

Return ONLY a JSON array, no markdown, no explanation:
[
  {{"id": "ctx1", "label": "Chinese Classical Poetry", "emoji": "🏮"}},
  {{"id": "ctx2", "label": "Western Horror Literature", "emoji": "🌑"}}
]
Cover diverse cultures and time periods."""

GRAPH_PROMPT = """You are a cultural semantics expert.
For the word "{word}" in the context of "{context}", generate a semantic network.

Return ONLY a JSON object, no markdown, no explanation:
{{
  "center": {{"id": "c0", "label": "{word}", "desc": "One sentence describing the core meaning of this word in this context."}},
  "nodes": [
    {{"id": "n1", "label": "Concept (2-3 words)", "desc": "How this concept relates to {word} in this context, 1-2 sentences."}}
  ],
  "edges": [
    {{"from": "c0", "to": "n1", "label": "symbolizes"}}
  ]
}}
Generate 5-6 nodes. All text in English."""

BASELINE_PROMPT = """You are a dictionary assistant.
Explain the word "{word}" in one short paragraph.
Keep it general with no cultural context separation. Reply in English."""