
def ffrange(min_val, max_val, step_val):
    if step_val == 0:
        print("Error: Step cannot be 0.")
        return

    current_val = min_val

    while (step_val > 0 and current_val <= max_val) or (step_val < 0 and current_val >= max_val):
        yield round(current_val, 10)
        current_val += step_val

