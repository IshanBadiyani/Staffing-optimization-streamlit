import numpy as np
from scipy.optimize import linprog

def optimize_staffing(
    required_staff,
    hourly_wage,
    max_staff=None,
    overstaff_penalty=0.0
):
    """
    Solves a staffing optimization problem using SciPy.

    Objective:
        Minimize total labor cost (with optional overstaffing penalty)

    Constraints:
        staff[t] >= required_staff[t]
        staff[t] <= max_staff (optional)
        staff[t] >= 0 and integer (approximated via rounding)

    Parameters:
        required_staff (array-like): Required staff per hour
        hourly_wage (array-like): Wage per staff per hour
        max_staff (int, optional): Maximum staff allowed per hour
        overstaff_penalty (float): Penalty per extra staff-hour

    Returns:
        staff_plan (np.array): Integer staffing plan
        total_cost (float): Total labor cost
    """

    required_staff = np.array(required_staff, dtype=float)
    hourly_wage = np.array(hourly_wage, dtype=float)
    n = len(required_staff)

    # Cost coefficients
    c = hourly_wage + overstaff_penalty

    # Constraints: -staff <= -required_staff
    A_ub = -np.eye(n)
    b_ub = -required_staff

    # Bounds
    bounds = []
    for _ in range(n):
        if max_staff is not None:
            bounds.append((0, max_staff))
        else:
            bounds.append((0, None))

    # Solve LP
    result = linprog(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=bounds,
        method="highs"
    )

    if not result.success:
        raise RuntimeError("Optimization failed: " + result.message)

    # Conservative rounding to preserve feasibility
    staff_plan = np.ceil(result.x).astype(int)

    # Cost calculation
    total_cost = np.sum(staff_plan * hourly_wage)

    return staff_plan, total_cost
