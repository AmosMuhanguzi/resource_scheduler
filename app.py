from flask import Flask, render_template, jsonify, request
from models import Scheduler, Agent
from simulation import Simulation

app = Flask(__name__)

# Initialize scheduler and simulation
scheduler = Scheduler()
simulation = Simulation(scheduler)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/state')
def get_state():
    # Add simulation status to the state
    state = scheduler.get_state()
    state['simulation_status'] = {
        'running': simulation.running,
        'paused': simulation.paused
    }
    return jsonify(state)

@app.route('/api/start', methods=['POST'])
def start_simulation():
    simulation.start()
    return jsonify({"status": "started"})

@app.route('/api/stop', methods=['POST'])
def stop_simulation():
    simulation.stop()
    return jsonify({"status": "stopped"})

@app.route('/api/pause', methods=['POST'])
def pause_simulation():
    simulation.pause()
    return jsonify({"status": "paused"})

@app.route('/api/resume', methods=['POST'])
def resume_simulation():
    simulation.resume()
    return jsonify({"status": "resumed"})

@app.route('/api/reset', methods=['POST'])
def reset_simulation():
    simulation.reset()
    return jsonify({"status": "reset"})

@app.route('/api/algorithm', methods=['POST'])
def set_algorithm():
    algorithm = request.json.get('algorithm')
    scheduler.set_algorithm(algorithm)
    return jsonify({"status": "algorithm updated", "algorithm": algorithm})

@app.route('/api/agents/add', methods=['POST'])
def add_agent():
    name = request.json.get('name', 'New Agent')
    max_workload = int(request.json.get('max_workload', 3))
    agent = Agent(name, max_workload=max_workload)
    scheduler.add_agent(agent)
    return jsonify({"status": "agent added", "agent": agent.to_dict()})

@app.route('/api/agents/remove', methods=['POST'])
def remove_agent():
    agent_id = request.json.get('agent_id')
    success = scheduler.remove_agent(agent_id)
    return jsonify({"status": "success" if success else "failed"})

if __name__ == '__main__':
    app.run(debug=True)
