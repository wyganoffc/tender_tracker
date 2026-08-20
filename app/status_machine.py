# статусы
ALLOWED = {
    "draft": ["active", "cancelled"],
    "active": ["won", "lost", "cancelled"],
    "won": [],
    "lost": [],
    "cancelled": []
}


# валидация
def validate_transition(old: str, new: str) -> bool:
    """Валидация"""
    return new in ALLOWED.get(old, [])
