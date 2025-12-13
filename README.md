# Staffing Optimization Engine (SciPy)

> A prescriptive analytics application that transforms historical demand data into cost-optimal hourly staffing plans for operations managers.

---

## 🎯 The Problem

Staffing is one of the most persistent operational challenges in service-based businesses such as cafés, retail stores, call centers, and hospitality operations. Demand fluctuates by hour, labor costs vary, and even small misalignments between staffing and demand can lead to poor customer experience, employee burnout, or unnecessary cost.

In many organizations, staffing decisions are still made using intuition, static schedules, or simple averages. These approaches fail to respond to real demand variability and do not scale as operations grow or conditions change.

Because labor is often the **largest controllable operating cost**, inefficient staffing decisions compound quickly—making this a high-impact problem worth solving with analytics.

---

## 💡 The Solution

This project delivers a **staffing optimization engine** that converts historical demand data into **actionable, cost-minimized staffing recommendations**.

Rather than stopping at descriptive analysis, the system applies **prescriptive analytics**. Demand is translated into labor requirements using configurable productivity assumptions, and an optimization model determines the minimum-cost staffing plan that guarantees coverage.

The result is a decision-support tool that does not just analyze the past—but **recommends what to do next**, hour by hour.

---

## 🚀 Live Demo

**[Try it here →](https://your-streamlit-app-url)**  
*(Replace with your deployed Streamlit URL)*

---

## ⚙️ How It Works

1. **Upload demand data**  
   Users upload a CSV containing date, hour, demand, and hourly wage.

2. **Optimization engine runs**  
   The system converts demand into required staffing levels and solves a cost-minimization problem using SciPy.

3. **Staffing plan generated**  
   Users receive a downloadable, manager-ready staffing plan with costs and coverage guarantees.

---

### The Analytics Behind It

- **Inputs**
  - Hourly demand
  - Hourly wage rates
  - Productivity assumptions
  - Optional service buffers and staffing caps

- **Optimization**
  - Objective: Minimize total labor cost
  - Constraints:
    - Staffing must meet or exceed demand each hour
    - Optional caps on maximum staff
    - Optional penalties for overstaffing
  - Solver:
    - `scipy.optimize.milp` (integer optimization when available)
    - Fallback to linear programming with conservative rounding

- **Outputs**
  - Planned staff per hour
  - Hourly and total labor cost
  - Demand vs. staffing comparison

---

## 📊 Example Output

The app produces:
- Hour-by-hour staffing recommendations
- Labor cost per hour
- Total labor cost across the planning horizon
- Downloadable CSV for scheduling or reporting

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit  
- **Optimization:** SciPy (`scipy.optimize.milp`, `linprog`)  
- **Data Processing:** Pandas, NumPy  
- **Visualization:** Streamlit charts, Matplotlib  
- **Deployment:** Streamlit Community Cloud  

---

## 🎓 About This Project

Built for **ISOM 839 – Prescriptive Analytics** at **Suffolk University**.

This project demonstrates how optimization models can be operationalized into deployable, decision-ready analytics products.

**Author:** Ishan Badiyani  
**LinkedIn:** https://www.linkedin.com/in/your-link](https://www.linkedin.com/in/ishanbadiyani/  
 

---

## 🔮 Future Possibilities

With additional time and scope, this framework could evolve into:
- Shift-based scheduling
- Multi-skill workforce optimization
- Demand forecasting integration
- Overtime and labor-law constraints
- Multi-location staffing models
- POS and workforce management integrations

From a business perspective, this can scale into a l
