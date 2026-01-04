import random
from time import time

from utils.config import ROOT_DIR

first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
statuses = ["Active", "Disabled"]
roles = ["Admin", "Editor", "Viewer"]

random_name = f"{random.choice(first_names)} {random.choice(last_names)}"
random_email = f"user_{int(time())}@example.com"
random_status = random.choice(statuses)
random_role = random.choice(roles)
profile_photo = ROOT_DIR + "/data/photo/test_profile_photo.png"