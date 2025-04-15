## -----------------------------------------------------------------------------
## Code Author          : Omar Alaa Eldeen
## Created On           : Monday - 24th March 2026
## File Name            : project.py
## Code Title           : Simulation of Web-Based Ticket Booking System 
## -----------------------------------------------------------------------------
import simpy
import random
import statistics
import matplotlib.pyplot as plt
from tabulate import tabulate  # For tables

# Scenario Constants
PEAK_USERS = 500  
PROCESSING_TIME = 0.2  
SIMULATION_TIME = 10  
ARRIVAL_RATE = PEAK_USERS / SIMULATION_TIME  
MAX_QUEUE_SIZE = 100  # Max queue before dropping requests

# Data collection
response_times = {}
utilization_rates = {}
dropped_requests = {}

# Request Handling Process
def handle_request(env, server, request_id, server_count):
    arrival_time = env.now  

    with server.request() as req:
        yield req  
        
        # Check if the request has waited too long (dropped if waited >1s)
        if env.now - arrival_time > 1:
            dropped_requests[server_count] += 1
            return  

        yield env.timeout(PROCESSING_TIME)  

    response_time = env.now - arrival_time  
    response_times[server_count].append(response_time)

# User Request Generator
def user_request_generator(env, server, server_count):
    request_id = 0
    while True:
        yield env.timeout(random.expovariate(ARRIVAL_RATE))  
        
        # If queue exceeds limit, drop the request
        if len(server.queue) >= MAX_QUEUE_SIZE:
            dropped_requests[server_count] += 1
            continue  

        env.process(handle_request(env, server, request_id, server_count))
        request_id += 1

# Run Simulation
def run_simulation(num_servers):
    response_times[num_servers] = []
    dropped_requests[num_servers] = 0  

    env = simpy.Environment()
    server = simpy.Resource(env, capacity=num_servers)  
    env.process(user_request_generator(env, server, num_servers))
    
    env.run(until=SIMULATION_TIME)  

    avg_response_time = statistics.mean(response_times[num_servers]) if response_times[num_servers] else float('inf')
    server_utilization = (sum(response_times[num_servers]) / (num_servers * SIMULATION_TIME)) * 100

    utilization_rates[num_servers] = server_utilization

    return avg_response_time, server_utilization, dropped_requests[num_servers]

# User Input for Server Count
num_servers = int(input("Enter the number of servers to simulate: "))

# Run Simulation for User-Entered Value
avg_time, utilization, dropped = run_simulation(num_servers)

# Print results in a table
results_table = [[num_servers, f"{avg_time:.3f} sec", f"{utilization:.2f}%", dropped]]
print("\n📊 Simulation Results:")
print(tabulate(results_table, headers=["# Servers", "Avg Response Time", "Server Utilization", "Dropped Requests"], tablefmt="pretty"))

# Explanation 
print("\n🔎 Key Observations:")
if avg_time > 0.5:
    print(f"🔹 With {num_servers} servers, response time is {avg_time:.3f} sec, which is above 500ms. More servers may be needed. ⚠️")
else:
    print(f"✅ With {num_servers} servers, response time is {avg_time:.3f} sec, meeting the 500ms target!")

print(f"🔹 Server utilization: {utilization:.2f}%")
print(f"🔹 Dropped requests: {dropped} (Requests that waited too long or exceeded the queue limit)")

# Answering the Key Questions
print("\n📌 Answers to Important Questions:")

# Question 1: How does response time change as the number of users increase?
print("\n 1️⃣ How does response time change as the number of users increase?")
print("   - More users = higher response time if the system has limited servers.")
print("   - A single server struggles, leading to long waits and dropped requests.")
print("   - Adding more servers helps maintain performance.")

# Question 2: How many servers are needed to maintain an average response time below 500ms?
print("\n 2️⃣ How many servers are needed to maintain an average response time below 500ms?")
if avg_time <= 0.5:
    print(f"   ✅ {num_servers} servers are sufficient to keep response time below 500ms.")
else:
    print(f"   ⚠️ {num_servers} servers are not enough. More servers may be needed.")

# Question 3: What is the impact of different scaling strategies (fixed vs. auto-scaling)?
print("\n 3️⃣ What is the impact of different scaling strategies (fixed vs. auto-scaling)?")
print("   - Fixed Scaling: Performance drops when traffic spikes. Many users experience slow loading.")
print("   - Auto-Scaling: The system automatically adds or removes servers based on demand.")
print("   - Impact: Saves cost and ensures users get a smooth experience!")

# Relationship Between Server Utilization & Number of Servers
print("\n📊 Relationship Between Server Utilization & Number of Servers:")
print("   - Server utilization represents how much time the servers are actively processing requests.")
print("   - Fewer servers → Higher utilization → Risk of overload → Increased response time & dropped requests.")
print("   - More servers → Lower utilization → Better performance, but possible resource waste.")
print("   - The goal is to balance performance and cost, ensuring smooth operation without over-provisioning.")
print("   - Auto-scaling can dynamically adjust server count for optimal performance and efficiency.")

# Plot Results
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(["Avg Response Time", "Utilization", "Dropped Requests"], [avg_time, utilization, dropped], color=['blue', 'green', 'red'])
ax.set_title("Performance Metrics")
ax.set_ylabel("Values")
plt.show()
