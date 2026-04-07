from fastapi import FastAPI
from env.environment import EmailEnv
from env.models import Action

app = FastAPI()

env = EmailEnv()


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
        "reward": result["reward"].dict(),
        "done": result["done"],
        "info": result["info"]
    }


@app.get("/")
def home():
    return {"message": "Email AI Environment is running!"}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()