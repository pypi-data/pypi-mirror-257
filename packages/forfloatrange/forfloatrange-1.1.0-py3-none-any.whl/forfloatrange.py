def ffrange(*args):
    if len(args) == 1:
        min_val = 0
        max_val = args[0]
        step_val = 1
    elif len(args) == 2:
        min_val = args[0]
        max_val = args[1]
        step_val = 1
    elif len(args) == 3:
        min_val, max_val, step_val = args
    else:
        print("Error: ffrange() takes 1 to 3 arguments.")
        return

    if step_val == 0:
        print("Error: Step cannot be 0.")
        return

    current_val = min_val

    while (step_val > 0 and current_val <= max_val) or (step_val < 0 and current_val >= max_val):
        yield round(current_val, 10)
        current_val += step_val