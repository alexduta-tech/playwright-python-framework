import os
import random
import uuid

from utils.config import ROOT_DIR

first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
statuses = ["Active", "Disabled"]
roles = ["Admin", "Editor", "Viewer"]

def random_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"
def non_existing_name():
    return str(uuid.uuid4())
def random_email():
    return f"user_{uuid.uuid4().hex[:8]}@example.com"
def random_status():
    return random.choice(statuses)
def random_role():
    return random.choice(roles)
# Build path using os.path.join to ensure OS-specific separators
profile_photo = os.path.join(ROOT_DIR, "data", "photo", "test_profile_photo.png")