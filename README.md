# 🎟️ Web-Based Ticket Booking System Simulation

## 📌 Project Overview
This simulation models a **web-based ticket booking system** using `SimPy`, analyzing how server count affects system performance under peak load conditions.

Key performance metrics tracked:
- Average response time
- Server utilization
- Dropped requests (due to long wait or queue overflow)

## 🛠️ Technologies Used
- Python 3.x
- [SimPy](https://simpy.readthedocs.io/)
- matplotlib
- tabulate
- statistics & random (built-in modules)

## 🧠 Key Concepts
- **Discrete Event Simulation** for modeling request processing.
- **Queuing Theory** for analyzing system load.
- **Auto-scaling strategy** vs. **Fixed server capacity**.
- Real-time system behavior under user traffic spikes.

## 📁 Project Structure

ticket-booking-simulation/ ├── project.py # Main simulation script ├── README.md # Project documentation ├── requirements.txt # Python dependencies └── plots/ # (Optional) Store generated performance charts

