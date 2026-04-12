import os
from openai import OpenAI
from env.environment import EmailEnv
from env.models import Action

# ENV VARIABLES (REQUIRED)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)


# SAFE REWARD FUNCTION
def safe_reward(value):
    try:
        value = float(value)
    except:
        return 0.5

    if value <= 0.0:
        value = 0.01
    elif value >= 1.0:
        value = 0.99

    value = float(f"{value:.2f}")

    if value == 0.00:
        value = 0.01
    if value == 1.00:
        value = 0.99

    return value


# LLM ACTION
def get_action_from_ai(email_text):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Classify and reply to email"},
                {"role": "user", "content": email_text}
            ]
        )

        content = response.choices[0].message.content.lower()

        # simple parsing
        if "refund" in content:
            return Action(category="complaint", reply=content)
        elif "price" in content:
            return Action(category="query", reply=content)
        elif "help" in content:
            return Action(category="request", reply=content)
        else:
            return Action(category="query", reply=content)

    except Exception:
        # fallback
        return Action(category="query", reply="default response")


# MAIN EXECUTION
def run_task(task_type):
    env = EmailEnv()
    obs = env.reset(task_type=task_type)

    step = 1
    rewards = []
    success = True
    error_msg = "null"

    # START
    print(f"[START] task={task_type} env=email model={MODEL_NAME}", flush=True)

    try:
        action = get_action_from_ai(obs.email_text)

        result = env.step(action)

        reward = safe_reward(result["reward"].score)
        done = result["done"]

        rewards.append(reward)

        action_str = action.category if action.category else "query"

        # STEP
        print(
            f"[STEP] step={step} action={action_str} reward={reward:.2f} done={str(done).lower()} error={error_msg}",
            flush=True
        )

    except Exception:
        reward = 0.5
        done = True
        success = False
        error_msg = "runtime_error"

        print(
            f"[STEP] step={step} action=error reward={reward:.2f} done=true error={error_msg}",
            flush=True
        )

    # END
    safe_rewards = [f"{safe_reward(r):.2f}" for r in rewards]

    print(
        f"[END] success={str(success).lower()} steps={step} rewards={','.join(safe_rewards)}",
        flush=True
    )


def main():
    for task in ["easy", "medium", "hard"]:
        run_task(task)


if __name__ == "__main__":
    main()