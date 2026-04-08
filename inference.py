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

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        text = response.choices[0].message.content

        # parsing
        category = "query"
        reply = text

        if "category:" in text.lower():
            category = text.lower().split("category:")[1].split("\n")[0].strip()

        return Action(category=category, reply=reply)

    except Exception as e:
        print("API ERROR:", str(e))  # important for logs

        # ✅ SAFE FALLBACK (VERY IMPORTANT)
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
    print("START")

    try:
        env = EmailEnv()

        for task in ["easy", "medium", "hard"]:
            print(f"\nSTEP: Running {task} task")

            obs = env.reset(task_type=task)
            print("Email:", obs.email_text)

            action = get_action_from_ai(obs.email_text)

            result = env.step(action)

            print("Action:", action)
            print("Reward:", result["reward"].score)

    except Exception as e:
        print("FATAL ERROR:", str(e))

    print("END")


if __name__ == "__main__":
    main()
