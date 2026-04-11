from env.environment import EmailEnv
from env.models import Action

# Step 1: Create environment
env = EmailEnv()

# Step 2: Start environment
obs = env.reset(task_type="easy")

print("\n--- Observation (Email AI sees) ---")
print(obs)

# Step 3: Give action (pretend AI response)
action = Action(category="complaint")

# Step 4: Take step
result = env.step(action)

print("\n--- Result after action ---")
print(result)