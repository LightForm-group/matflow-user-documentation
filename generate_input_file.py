def generate_input_file(input_data: list):
    """Generate an input file, without input_file_generator"""
    with open("input_file.txt", "w") as f:
        f.write(" ".join(input_data))