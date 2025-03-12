import time
import uuid

class Customer:
    PRIORITY_NORMAL = 0
    PRIORITY_CORPORATE = 1
    PRIORITY_VIP = 2
    
    PRIORITY_NAMES = {
        PRIORITY_NORMAL: "Normal",
        PRIORITY_CORPORATE: "Corporate",
        PRIORITY_VIP: "VIP"
    }

    def __init__(self, service_time, priority=0):
        self.id = str(uuid.uuid4())[:3]
        self.service_time = service_time  # in seconds
        self.priority = priority
        self.arrival_time = time.time()
        self.start_service_time = None
        self.completion_time = None
        self.assigned_agent = None

    def assign_agent(self, agent):
        self.assigned_agent = agent
        self.start_service_time = time.time()
        
    def complete_service(self):
        self.completion_time = time.time()
        
    def get_wait_time(self):
        if self.start_service_time:
            return self.start_service_time - self.arrival_time
        return time.time() - self.arrival_time
    
    def get_service_time(self):
        if self.completion_time and self.start_service_time:
            return self.completion_time - self.start_service_time
        return 0
    
    def get_priority_name(self):
        return self.PRIORITY_NAMES.get(self.priority, "Unknown")
    
    def to_dict(self):
        return {
            "id": self.id,
            "service_time": self.service_time,
            "priority": self.priority,
            "priority_name": self.get_priority_name(),
            "arrival_time": self.arrival_time,
            "start_service_time": self.start_service_time,
            "completion_time": self.completion_time,
            "wait_time": round(self.get_wait_time(), 2),
            "assigned_agent": self.assigned_agent.id if self.assigned_agent else None
        }
