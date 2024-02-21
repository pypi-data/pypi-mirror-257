def ffrange(*args):
    length = len(args)
    if length == 1:
        min_val = 0
        max_val = args[0]
        step_val = 1
    elif length == 2:
        min_val, max_val = args
        step_val = 1
    elif length == 3:
        min_val, max_val, step_val = args
    else:
        print("Error: ffrange() takes 1 to 3 arguments.")
        return

    if step_val == 0:
        print("Error: Step cannot be 0.")
        return

    if length == 1 or length == 2:
        for i in range(min_val, max_val, step_val):
            yield i
    else:
        current_val = min_val
        rounded_step = round(step_val, 10)
        while (step_val > 0 and current_val <= max_val) or (step_val < 0 and current_val >= max_val):
            yield current_val
            current_val += rounded_step