from decimal import Decimal

def ffrange(*args):
    length = len(args)
    if length == 0 or length > 3:
        raise ValueError("Error: ffrange() takes 1 to 3 arguments.")

    min_val = Decimal(str(args[0])) if length > 0 else Decimal(0)
    max_val = Decimal(str(args[1])) if length > 1 else Decimal(str(args[0]))
    step_val = Decimal(str(args[2])) if length > 2 else Decimal(1)

    if step_val == 0:
        raise ValueError("Error: Step cannot be 0.")

    results = []

    def calculate_range(start, end, step):
        current_val = start
        while (step > 0 and current_val < end+step) or (step < 0 and current_val > end+step):
            results.append(current_val)
            current_val += step

    calculate_range(min_val, max_val, step_val)

    return results