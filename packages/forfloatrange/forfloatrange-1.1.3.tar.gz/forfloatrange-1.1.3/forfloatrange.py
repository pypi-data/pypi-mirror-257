def ffrange(*args):
    length = len(args)
    if length == 0 or length > 3:
        raise ValueError("Error: ffrange() takes 1 to 3 arguments.")

    min_val = args[0] if length > 0 else 0
    max_val = args[1] if length > 1 else args[0]
    step_val = args[2] if length > 2 else 1

    if step_val == 0:
        raise ValueError("Error: Step cannot be 0.")

    if step_val > 0:
        while min_val < max_val:
            yield min_val
            min_val += step_val
    else:
        while min_val > max_val:
            yield min_val
            min_val += step_val