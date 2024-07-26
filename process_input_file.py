import json
def process_input_file():
    """Process an input file"""
    with open("input_file.json", "r") as f:
        data = json.load(f)
    data = data * 2
    with open("processed_file.json", "w") as f:
        json.dump(data, f, indent=2)