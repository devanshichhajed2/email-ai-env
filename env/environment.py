from env.models import Observation, Action, Reward
from env.tasks import get_task_email, evaluate_task


class EmailEnv:
    def __init__(self):
        self.current_email = None
        self.task_type = None
        self.done = False

    def reset(self, task_type="easy"):
        self.task_type = task_type
        self.current_email = get_task_email(task_type)
        self.done = False

        return Observation(**self.current_email)

    def step(self, action: Action):
        score, feedback = evaluate_task(
            self.task_type,
            self.current_email,
            action
        )

        # BULLETPROOF SAFETY FIX
        try:
            # ensure score is float
            if score is None:
                score = 0.5

            score = float(score)

            # force into valid range
            if score <= 0.0:
                score = 0.01
            elif score >= 1.0:
                score = 0.99

            # remove floating precision issues
            score = float(f"{score:.2f}")

            # final safety check
            if score <= 0.0:
                score = 0.01
            elif score >= 1.0:
                score = 0.99

        except Exception:
            # fallback in any unexpected case
            score = 0.5
            feedback = "Safe fallback applied"

        self.done = True

        return {
            "observation": Observation(**self.current_email),
            "reward": Reward(score=score, feedback=feedback),
            "done": self.done,
            "info": {}
        }

    def state(self):
        return self.current_email
