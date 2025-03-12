import random
import time
import threading
from models import Customer, Agent, Scheduler

class Simulation:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.running = False
        self.paused = False
        self.simulation_thread = None
        self.customer_generation_thread = None
        self.customer_completion_thread = None
        
    def start(self):
        if self.running:
            return
            
        self.running = True
        self.paused = False
        
        # Initialize agents only if there are none
        if not self.scheduler.agents:
            agent_names = ["Aketch", "Muhanguzi", "Batya"]
            for i, name in enumerate(agent_names[:3]):  # Start with fewer agents
                self.scheduler.add_agent(Agent(name, max_workload=2))
        
        # Start customer generation thread
        self.customer_generation_thread = threading.Thread(target=self._generate_customers)
        self.customer_generation_thread.daemon = True
        self.customer_generation_thread.start()
        
        # Start customer completion thread
        self.customer_completion_thread = threading.Thread(target=self._process_customer_completions)
        self.customer_completion_thread.daemon = True
        self.customer_completion_thread.start()
        
        # Start main simulation thread
        self.simulation_thread = threading.Thread(target=self._run_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
    
    def pause(self):
        """Pause the simulation without stopping threads"""
        self.paused = True
    
    def resume(self):
        """Resume a paused simulation"""
        self.paused = False
    
    def reset(self):
        """Reset the simulation to its initial state"""
        # First stop if running
        was_running = self.running
        if was_running:
            self.stop()
        
        # Reset the scheduler
        self.scheduler.reset()
        
        # Restart if it was running
        if was_running:
            self.start()
    
    def stop(self):
        self.running = False
        if self.simulation_thread:
            self.simulation_thread.join(timeout=1.0)
        if self.customer_generation_thread:
            self.customer_generation_thread.join(timeout=1.0)
        if self.customer_completion_thread:
            self.customer_completion_thread.join(timeout=1.0)
    
    def _generate_customers(self):
        """Generate new customers at random intervals"""
        while self.running:
            # Skip if paused
            if self.paused:
                time.sleep(0.5)
                continue
                
            # Random wait between 1, 5 seconds before generating a new customer
            wait_time = random.uniform(1, 5)
            time.sleep(wait_time)
            
            # Generate a new customer with random service time and priority
            service_time = random.randint(5, 30)  # 5 to  30  seconds
            
            # Assign priority with probabilities: 85% Normal, 10% Corporate, 5% VIP
            priority_roll = random.random()
            if priority_roll < 0.85:
                priority = Customer.PRIORITY_NORMAL
            elif priority_roll < 0.95:
                priority = Customer.PRIORITY_CORPORATE
            else:
                priority = Customer.PRIORITY_VIP
                
            customer = Customer(service_time, priority)
            self.scheduler.add_customer(customer)
    
    def _process_customer_completions(self):
        """Check for completed customers and remove them from agents"""
        while self.running:
            # Skip if paused
            if self.paused:
                time.sleep(0.5)
                continue
                
            time.sleep(1)  # Check every second
            
            for agent in self.scheduler.agents:
                for customer in list(agent.assigned_customers):  # Create a copy to avoid modification issues
                    if customer.start_service_time and time.time() - customer.start_service_time >= customer.service_time:
                        self.scheduler.complete_customer(customer.id)
    
    def _run_simulation(self):
        """Main simulation loop"""
        while self.running:
            # Skip if paused
            if self.paused:
                time.sleep(0.5)
                continue
                
            # Assign customers to available agents
            self.scheduler.assign_customers()
            
            # Sleep for a short interval before the next update
            time.sleep(5)
