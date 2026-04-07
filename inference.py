import os
from env.environment import EmailEnv
from env.models import Action
from openai import OpenAI

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def get_action_from_ai(email_text):
    prompt = f"""
You are an email assistant.

Classify the email and generate a reply.

Email:
{email_text}

Return ONLY in this format:
category: <category>
reply: <reply>
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    text = response.choices[0].message.content

    category = "query"
    reply = text

    if "category:" in text.lower():
        category = text.lower().split("category:")[1].split("\n")[0].strip()

    return Action(category=category, reply=reply)
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
