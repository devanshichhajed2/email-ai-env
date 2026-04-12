import random

EASY_EMAILS = [
    {
        "email_text": "I want a refund, my product is damaged.",
        "sender_type": "customer",
        "urgency": "high",
        "emotion": "angry",
        "category": "complaint"
    },
    {
        "email_text": "Can you share pricing details?",
        "sender_type": "customer",
        "urgency": "low",
        "emotion": "neutral",
        "category": "query"
    }
]

MEDIUM_EMAILS = [
    {
        "email_text": "I need help resetting my password.",
        "sender_type": "customer",
        "urgency": "medium",
        "emotion": "neutral"
    }
]

HARD_EMAILS = [
    {
        "email_text": "This is the worst service ever. I want my money back!",
        "sender_type": "customer",
        "urgency": "high",
        "emotion": "angry"
    }
]


def get_task_email(task_type):
    if task_type == "easy":
        return random.choice(EASY_EMAILS)
    elif task_type == "medium":
        return random.choice(MEDIUM_EMAILS)
    else:
        return random.choice(HARD_EMAILS)


# 🔥 FINAL SAFE RETURN FUNCTION (CANNOT FAIL)
def safe(score):
    try:
        score = float(score)
    except:
        score = 0.5

    # STRICTLY BETWEEN (0,1)
    if score <= 0.0:
        score = 0.01
    elif score >= 1.0:
        score = 0.99

    # FIX FLOAT PRECISION
    score = float(f"{score:.2f}")

    # FINAL GUARD (CRITICAL)
    if score <= 0.0:
        score = 0.01
    if score >= 1.0:
        score = 0.99

    return score


def evaluate_task(task_type, email, action):

    # EASY
    if task_type == "easy":
        if action.category == email.get("category"):
            return safe(0.8), "Correct classification"
        else:
            return safe(0.2), "Wrong classification"

    # MEDIUM
    elif task_type == "medium":
        score = 0.3

        if action.reply:
            text = action.reply.lower()

            if "help" in text:
                score += 0.2
            if "thank" in text:
                score += 0.2
            if len(text) > 20:
                score += 0.2

        return safe(score), "Reply evaluated"

    # HARD
    elif task_type == "hard":
        score = 0.3

        if action.reply:
            text = action.reply.lower()

            if "sorry" in text:
                score += 0.2
            if "understand" in text:
                score += 0.2
            if "refund" in text:
                score += 0.2

        return safe(score), "Handled complex email"

    # FALLBACK (IMPORTANT)
    return safe(0.5), "Fallback"