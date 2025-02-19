import os

current_dir = os.path.dirname(os.path.abspath(__file__))

sample_inputs_dir = os.path.join(current_dir, '..', '..', 'sample_inputs')

file_path = os.path.join(sample_inputs_dir, 'easy_sample_01_2.txt')

rows = cols = 0
sparse_matrix = {}

def parse_line(line):
    line = line.strip()
    if line.startswith('rows='):
        return 'rows', int(line.split('=')[1])
    elif line.startswith('cols='):
        return 'cols', int(line.split('=')[1])
    elif line.startswith('(') and line.endswith(')'):
        line = line[1:-1]
        row, col, val = map(int, line.split(','))
        return 'entry', (row, col, val)
    else:
        return None, None
def open_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line_type, data = parse_line(line)
            if line_type == 'rows':
                rows = data
            elif line_type == 'cols':
                cols = data
            elif line_type == 'entry':
                row, col, val = data
                sparse_matrix[(row, col)] = val
    return sparse_matrix
open_file(file_path)
print(f"Matrix dimensions: {rows}x{cols}")
print("Non-zero entries:")
for (row, col), val in sparse_matrix.items():
    print(f"Row {row}, Column {col}: {val}")
