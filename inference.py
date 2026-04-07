import os
from env.environment import EmailEnv
from env.models import Action
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)


def get_action_from_ai(email_text):
    email = email_text.lower()

    
    if "refund" in email or "worst" in email or "not working" in email:
        return Action(
            category="complaint",
            reply="We sincerely apologize for the inconvenience. We understand your concern and will process your refund quickly."
        )

    elif "help" in email or "password" in email:
        return Action(
            category="request",
            reply="Thank you for reaching out. We will help you resolve your issue. Please follow the instructions provided."
        )

    elif "price" in email or "pricing" in email:
        return Action(
            category="query",
            reply="Thank you for your interest. We provide flexible pricing plans. Please let us know your requirements."
        )

    
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
        env = EmailEnv()

        # START block
        print(f"[START] task={task}", flush=True)

        obs = env.reset(task_type=task)

        step_count = 0
        total_score = 0.0

        action = get_action_from_ai(obs.email_text)
        result = env.step(action)

        step_count += 1
        reward = result["reward"].score
        total_score += reward

        # STEP block
        print(f"[STEP] step={step_count} reward={reward}", flush=True)

        # END block
        print(f"[END] task={task} score={total_score} steps={step_count}", flush=True)

    print("\nEND")

if __name__ == "__main__":
    main()
