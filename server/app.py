import os
import uvicorn
from fastapi import FastAPI
from env.environment import EmailEnv
from env.models import Action

app = FastAPI()

env = EmailEnv()


@app.get("/")
def home():
    return {"message": "Email AI Environment Running"}


@app.post("/reset")
def reset(task_type: str = "easy"):
    obs = env.reset(task_type=task_type)
    return obs.dict()


@app.post("/step")
def step(action: dict):
    action_obj = Action(**action)
    result = env.step(action_obj)

    raw_score = result["reward"].score

    try:
        score = float(raw_score)
    except:
        score = 0.5

    if score <= 0.0:
        score = 0.01
    elif score >= 1.0:
        score = 0.99

    score = float(f"{score:.2f}")

    if score <= 0.0:
        score = 0.01
    if score >= 1.0:
        score = 0.99

    return {
        "observation": result["observation"].dict(),
        "reward": {
            "score": score,
            "feedback": str(result["reward"].feedback)
        },
        "done": bool(result["done"]),
        "info": {}
    }
    
@app.get("/state")
def get_state():
    return env.state()


def main():
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()