def make_control_to_index(first_index, num_controls):
    return {first_index + control: index for index, control in enumerate(range(num_controls))}
