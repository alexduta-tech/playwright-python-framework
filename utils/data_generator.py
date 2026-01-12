import os
import random
from time import time
import uuid

from utils.config import ROOT_DIR

first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
statuses = ["Active", "Disabled"]
roles = ["Admin", "Editor", "Viewer"]

random_name = f"{random.choice(first_names)} {random.choice(last_names)}"
non_existing_name = str(uuid.uuid4())
random_email = f"user_{int(time())}@example.com"
random_status = random.choice(statuses)
random_role = random.choice(roles)
# Build path using os.path.join to ensure OS-specific separators
profile_photo = os.path.join(ROOT_DIR, "data", "photo", "test_profile_photo.png")