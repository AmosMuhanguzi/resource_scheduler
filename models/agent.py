import time
import uuid

class Agent:
    STATUS_FREE = "free"
    STATUS_BUSY = "busy"
    
    def __init__(self, name, max_workload=3):
        self.id = str(uuid.uuid4())[:4]
        self.name = name
        self.status = self.STATUS_FREE
        self.max_workload = max_workload
        self.current_workload = 0
        self.assigned_customers = []
        self.total_service_time = 0
        self.service_start_time = None
        
    def assign_customer(self, customer):
        if self.current_workload < self.max_workload:
            self.assigned_customers.append(customer)
            self.current_workload += 1
            if self.current_workload == 1:  # Just became busy
                self.status = self.STATUS_BUSY
                self.service_start_time = time.time()
            return True
        return False
    
    def complete_customer(self, customer_id):
        for i, customer in enumerate(self.assigned_customers):
            if customer.id == customer_id:
                customer.complete_service()
                self.total_service_time += customer.get_service_time()
                self.assigned_customers.pop(i)
                self.current_workload -= 1
                if self.current_workload == 0:
                    self.status = self.STATUS_FREE
                    self.service_start_time = None
                return True
        return False
    
    def get_utilization_rate(self, total_time):
        if total_time == 0:
            return 0
        return min(1.0, self.total_service_time / total_time)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "max_workload": self.max_workload,
            "current_workload": self.current_workload,
            "assigned_customers": [c.id for c in self.assigned_customers],
            "utilization": round(self.total_service_time, 2)
        }
