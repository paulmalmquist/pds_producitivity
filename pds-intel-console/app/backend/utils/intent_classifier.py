import re


INTENT_KEYWORDS = {
    'analytics': ['chart', 'sql', 'trend', 'visual', 'genie'],
    'tasks': ['jira', 'task', 'standup', 'email', 'ticket'],
    'knowledge': ['explain', 'what', 'policy', 'guide', 'rag']
}


def classify_intent(prompt: str) -> tuple[str, list[str]]:
    prompt_lower = prompt.lower()
    matches: set[str] = set()
    reasons: list[str] = []
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword), prompt_lower):
                matches.add(intent)
                reasons.append(f"matched keyword '{keyword}' for {intent}")
                break

    if not matches:
        return 'knowledge', ['defaulted to knowledge intent']
    if len(matches) > 1:
        return 'mixed', reasons
    return matches.pop(), reasons
