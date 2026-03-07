class Task:
    def __init__(self, task_id, location, task_type):
        self.task_id = task_id
        self.location = location
        self.task_type = task_type
        self.assigned_robot = None
        self.completed = False