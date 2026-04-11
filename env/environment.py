<<<<<<< HEAD
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

        self.done = True

        return {
            "observation": Observation(**self.current_email),
            "reward": Reward(score=score, feedback=feedback),
            "done": self.done,
            "info": {}
        }

    def state(self):
=======
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

        self.done = True

        return {
            "observation": Observation(**self.current_email),
            "reward": Reward(score=score, feedback=feedback),
            "done": self.done,
            "info": {}
        }

    def state(self):
>>>>>>> 9442762521da75db7afedec0a183407fecae9595
        return self.current_email