import json
def generate_input_file(input_data: list):
    """Generate an input file, without input_file_generator"""
    with open("input_file.json", "w") as f:
        json.dump(input_data, f, indent=2)
