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


#  SAFE SCORING FUNCTION
def safe(score):
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return float(f"{score:.2f}")


def evaluate_task(task_type, email, action):

    # EASY TASK
    if task_type == "easy":
        if action.category == email.get("category"):
            return safe(0.8), "Correct classification"
        else:
            return safe(0.2), "Wrong classification"

    # MEDIUM TASK (MAX 0.9)
    elif task_type == "medium":
        score = 0.2

        if action.reply:
            if "help" in action.reply.lower():
                score += 0.2
            if "thank" in action.reply.lower():
                score += 0.2
            if len(action.reply) > 20:
                score += 0.2

        # max = 0.8
        return safe(score), "Reply evaluated"

    # HARD TASK (MAX 0.9)
    elif task_type == "hard":
        score = 0.2

        if action.reply:
            if "sorry" in action.reply.lower():
                score += 0.2
            if "understand" in action.reply.lower():
                score += 0.2
            if "refund" in action.reply.lower():
                score += 0.2

        # max = 0.8
        return safe(score), "Handled complex email"

    return safe(0.5), "Invalid task"