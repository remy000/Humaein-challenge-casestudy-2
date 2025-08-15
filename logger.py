# Simple step logger
class StepLogger:
    def __init__(self):
        self.steps = []

    def log(self, message: str):
        print(f"[STEP] {message}")
        self.steps.append(message)

    def get_log(self):
        return self.steps
