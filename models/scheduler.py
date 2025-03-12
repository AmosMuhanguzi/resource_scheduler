import time
from collections import deque

class Scheduler:
    ALGORITHM_ROUND_ROBIN = "round_robin"
    ALGORITHM_PRIORITY = "priority"
    ALGORITHM_SHORTEST_JOB_NEXT = "shortest_job_next"
    
    def __init__(self):
        self.customer_queue = deque()
        self.agents = []
        self.completed_customers = []
        self.algorithm = self.ALGORITHM_ROUND_ROBIN
        self.start_time = time.time()
        self.last_assigned_agent_index = -1
        
    def add_customer(self, customer):
        self.customer_queue.append(customer)
        
    def add_agent(self, agent):
        self.agents.append(agent)
        
    def set_algorithm(self, algorithm):
        if algorithm in [self.ALGORITHM_ROUND_ROBIN, self.ALGORITHM_PRIORITY, self.ALGORITHM_SHORTEST_JOB_NEXT]:
            self.algorithm = algorithm
            
    def get_available_agents(self):
        return [agent for agent in self.agents if agent.current_workload < agent.max_workload]
            
    def assign_customers(self):
        """Assign customers to available agents based on the selected algorithm"""
        if not self.customer_queue:
            return []
            
        available_agents = self.get_available_agents()
        if not available_agents:
            return []
            
        assigned = []
        
        # Sort the queue based on the algorithm
        queue_list = list(self.customer_queue)
        if self.algorithm == self.ALGORITHM_PRIORITY:
            queue_list.sort(key=lambda c: (-c.priority, c.arrival_time))
        elif self.algorithm == self.ALGORITHM_SHORTEST_JOB_NEXT:
            queue_list.sort(key=lambda c: (c.service_time, c.arrival_time))
        # Round robin uses the queue as is (FIFO)
        
        # Clear the queue and refill it with the sorted list
        self.customer_queue.clear()
        self.customer_queue.extend(queue_list)
        
        # Assign customers to agents
        while self.customer_queue and available_agents:
            # Get the next agent based on round-robin
            if self.algorithm == self.ALGORITHM_ROUND_ROBIN:
                self.last_assigned_agent_index = (self.last_assigned_agent_index + 1) % len(available_agents)
                agent = available_agents[self.last_assigned_agent_index]
            else:
                # For other algorithms, pick the first available agent
                agent = available_agents[0]
                
            customer = self.customer_queue.popleft()
            if agent.assign_customer(customer):
                customer.assign_agent(agent)
                assigned.append((agent, customer))
            
            # Update available agents
            available_agents = self.get_available_agents()
            if not available_agents:
                break
                
        return assigned
    
    def complete_customer(self, customer_id):
        for agent in self.agents:
            for customer in agent.assigned_customers:
                if customer.id == customer_id:
                    agent.complete_customer(customer_id)
                    self.completed_customers.append(customer)
                    return True
        return False
    
    def get_metrics(self):
        total_time = time.time() - self.start_time
        
        # Calculate average wait time
        wait_times = [c.get_wait_time() for c in self.completed_customers]
        avg_wait_time = sum(wait_times) / len(wait_times) if wait_times else 0
        
        # Calculate agent utilization
        agent_utilization = {}
        for agent in self.agents:
            agent_utilization[agent.id] = agent.get_utilization_rate(total_time)
        avg_utilization = sum(agent_utilization.values()) / len(agent_utilization) if agent_utilization else 0
        
        # Calculate task distribution (fairness)
        task_counts = {agent.id: len(agent.assigned_customers) + len([c for c in self.completed_customers if c.assigned_agent and c.assigned_agent.id == agent.id]) for agent in self.agents}
        max_tasks = max(task_counts.values()) if task_counts else 0
        min_tasks = min(task_counts.values()) if task_counts else 0
        fairness = 1.0 if max_tasks == 0 else 1.0 - ((max_tasks - min_tasks) / max_tasks)
        
        return {
            "average_wait_time": round(avg_wait_time, 2),
            "average_utilization": round(avg_utilization, 2),
            "fairness": round(fairness, 2),
            "completed_customers": len(self.completed_customers),
            "waiting_customers": len(self.customer_queue),
            "active_customers": sum(len(agent.assigned_customers) for agent in self.agents)
        }
    
    def get_state(self):
        """Get the current state of the system for the frontend"""
        return {
            "queue": [customer.to_dict() for customer in self.customer_queue],
            "agents": [agent.to_dict() for agent in self.agents],
            "active_customers": [customer.to_dict() for agent in self.agents for customer in agent.assigned_customers],
            "completed_customers": [customer.to_dict() for customer in self.completed_customers],
            "metrics": self.get_metrics(),
            "algorithm": self.algorithm
        }
      
        
        
    def remove_agent(self, agent_id):
        for i, agent in enumerate(self.agents):
            if agent.id == agent_id:
            # Check if agent has any assigned customers
                if agent.assigned_customers:
                # Return the customers to the queue
                    for customer in agent.assigned_customers:
                        customer.assigned_agent = None
                        customer.start_service_time = None
                        self.customer_queue.appendleft(customer)
            
            # Remove the agent
                self.agents.pop(i)
                return True
        return False
        
    def reset(self):
        """Reset the scheduler to its initial state"""
        # Keep the agents but clear their stats
        for agent in self.agents:
            agent.status = agent.STATUS_FREE
            agent.current_workload = 0
            agent.assigned_customers = []
            agent.total_service_time = 0
            agent.service_start_time = None
    
        # Clear all customers
        self.customer_queue.clear()
        self.completed_customers = []
    
        # Reset the start time
        self.start_time = time.time()
        self.last_assigned_agent_index = -1
