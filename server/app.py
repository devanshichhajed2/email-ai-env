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

    return {
        "observation": result["observation"].dict(),
        "reward": {
            "score": float(result["reward"].score),
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