# Decision logic ONLY: Evaluates prompt -> returns "LOCAL" or "CLOUD"

# Prompts matching these always go to CLOUD regardless of anything else
CLOUD_KEYWORDS = [
    "analyze", "analyse", "complex", "write code", "explain deeply",
    "summarize", "summarise", "debug", "refactor", "architecture",
    "compare", "difference between", "pros and cons", "essay",
    "research", "step by step", "detailed", "in depth", "algorithm",
    "implement", "design a", "create a system", "build a"
]

# Prompts matching these are always simple — LOCAL no matter the history length
SIMPLE_PATTERNS = [
    "hi", "hello", "hey", "what is your name", "who are you",
    "how are you", "what's up", "good morning", "good evening",
    "thanks", "thank you", "bye", "ok", "okay", "yes", "no",
    "what time", "what day", "what is 2", "what is 1"
]

def _is_clearly_simple(prompt: str) -> bool:
    """Returns True if prompt is obviously trivial."""
    p = prompt.lower().strip()
    # Very short prompts are almost always simple
    if len(p) <= 20:
        return True
    # Matches a known simple pattern prefix
    return any(p.startswith(pat) for pat in SIMPLE_PATTERNS)

def decide_route(prompt: str, history: list[dict]) -> str:
    """
    Smart heuristic routing:
    1. Always evaluate the prompt itself first — never let history override
       an obviously simple or obviously complex prompt.
    2. Only use history length as a tiebreaker for ambiguous mid-range prompts.
    """
    p_lower = prompt.lower().strip()

    # Step 1: If prompt is clearly complex → always CLOUD
    if len(prompt) > 300:
        return "CLOUD"
    if any(kw in p_lower for kw in CLOUD_KEYWORDS):
        return "CLOUD"

    # Step 2: If prompt is clearly simple → always LOCAL
    if _is_clearly_simple(prompt):
        return "LOCAL"

    # Step 3: Ambiguous prompt — use history as tiebreaker
    # (Only escalate to cloud if conversation is very long, >8 turns)
    if len(history) > 8:
        return "CLOUD"

    return "LOCAL"