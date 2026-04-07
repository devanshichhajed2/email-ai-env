import os
from env.environment import EmailEnv
from env.models import Action

# Setup client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_NAME = "gpt-4o-mini"


def get_action_from_ai(email_text):
    email = email_text.lower()

    # Complaint / angry emails
    if "refund" in email or "worst" in email or "not working" in email:
        return Action(
            category="complaint",
            reply="We sincerely apologize for the inconvenience. Please share your order details so we can resolve this issue and process your refund."
        )

    # Help / support queries
    elif "help" in email or "password" in email:
        return Action(
            category="request",
            reply="Thank you for reaching out. We will assist you with resetting your password. Please follow the instructions sent to your email."
        )

    # Pricing / info queries
    elif "price" in email or "pricing" in email:
        return Action(
            category="query",
            reply="Thank you for your interest. We offer multiple pricing plans. Please visit our website or let us know your requirements."
        )

    # Default case
    else:
        return Action(
            category="query",
            reply="Thank you for your message. We will get back to you shortly."
        )

def run_task(task_type):
    env = EmailEnv()
    obs = env.reset(task_type=task_type)

    print(f"\n--- Running {task_type.upper()} TASK ---")
    print("Email:", obs.email_text)

    action = get_action_from_ai(obs.email_text)

    result = env.step(action)

    print("AI Action:", action)
    print("Reward:", result["reward"])


def main():
    for task in ["easy", "medium", "hard"]:
        run_task(task)


if __name__ == "__main__":
    main()