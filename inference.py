import os
from openai import OpenAI

from env.environment import EmailEnv
from env.models import Action

# ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# OPENAI CLIENT
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)


def get_action_from_ai(email_text):
    prompt = f"""
Classify the email and generate a reply.
Email:
{email_text}
Return ONLY:
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

        category = "query"
        reply = text

        if text and "category:" in text.lower():
            category = text.lower().split("category:")[1].split("\n")[0].strip()

        return Action(category=category, reply=reply), None

    except Exception as e:
        # fallback if API fails
        return Action(
            category="query",
            reply="Thank you for your message."
        ), str(e)


# MAIN FUNCTION 
def main():
    env = EmailEnv()

    for task in ["easy", "medium", "hard"]:
        rewards = []
        step_count = 0
        success = False

        # START
        print(f"[START] task={task} env=email model={MODEL_NAME}", flush=True)

        try:
            obs = env.reset(task_type=task)

            step_count = 1

            action, error = get_action_from_ai(obs.email_text)

            result = env.step(action)

            reward = result["reward"].score
            done = result["done"]

       
            reward = max(0.01, min(0.99, reward))

            rewards.append(reward)

            # SAFE action string
            action_str = (action.category or "none").replace(" ", "_").lower()

            reward_str = f"{reward:.2f}"
            done_str = str(done).lower()
            error_str = error if error else "null"

            # STEP
            print(
                f"[STEP] step={step_count} action={action_str} reward={reward_str} done={done_str} error={error_str}",
                flush=True
            )

            success = bool(done)

        except Exception as e:
            # fallback step if something crashes
            print(
                f"[STEP] step=1 action=none reward=0.10 done=true error={str(e)}",
                flush=True
            )
            rewards.append(0.10)
            step_count = 1
            success = False

        rewards_str = ",".join([f"{r:.2f}" for r in rewards])

        # END
        print(
            f"[END] success={str(success).lower()} steps={step_count} rewards={rewards_str}",
            flush=True
        )


if __name__ == "__main__":
    main()
