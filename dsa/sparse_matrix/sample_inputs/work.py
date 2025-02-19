class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        self.matrix = {}  # Dictionary to store non-zero elements
        self.rows = 0
        self.cols = 0

        if matrixFilePath:
            self._load_from_file(matrixFilePath)
        elif numRows is not None and numCols is not None:
            self.rows = numRows
            self.cols = numCols
        else:
            raise ValueError("Either matrixFilePath or both numRows and numCols must be provided.")

    def _load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('rows='):
                        self.rows = int(line.split('=')[1])
                    elif line.startswith('cols='):
                        self.cols = int(line.split('=')[1])
                    elif line.startswith('(') and line.endswith(')'):
                        line = line[1:-1]
                        row, col, val = map(int, line.split(','))
                        self.setElement(row, col, val)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except ValueError:
            print(f"Error: Incorrect file format in '{file_path}'.")

    def getElement(self, currRow, currCol):
        return self.matrix.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)] 

    def __str__(self):
        result = []
        for row in range(self.rows):
            current_row = []
            for col in range(self.cols):
                current_row.append(str(self.getElement(row, col)))
            result.append(' '.join(current_row))
        return '\n'.join(result)

    def save_to_file(self, file_path):
        """ Saves the sparse matrix to a file in the same format as the input. """
        with open(file_path, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            for (row, col), value in self.matrix.items():
                file.write(f"({row},{col},{value})\n")

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Addition not possible: Matrices have different dimensions.")
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)
        for (r, c), v in self.matrix.items():
            result.setElement(r, c, v + other.getElement(r, c))
        for (r, c), v in other.matrix.items():
            if (r, c) not in self.matrix:
                result.setElement(r, c, v)
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Subtraction not possible: Matrices have different dimensions.")
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)
        for (r, c), v in self.matrix.items():
            result.setElement(r, c, v - other.getElement(r, c))
        for (r, c), v in other.matrix.items():
            if (r, c) not in self.matrix:
                result.setElement(r, c, -v)
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("Multiplication not possible: Number of columns in first matrix must equal number of rows in second matrix.")
        result = SparseMatrix(numRows=self.rows, numCols=other.cols)
        for (r1, c1), v1 in self.matrix.items():
            for c2 in range(other.cols):
                v2 = other.getElement(c1, c2)
                if v2 != 0:
                    result.setElement(r1, c2, result.getElement(r1, c2) + v1 * v2)
        return result


def main():
    try:
        file1 = input("Enter first matrix file path: ")
        file2 = input("Enter second matrix file path: ")

        matrix1 = SparseMatrix(matrixFilePath=file1)
        matrix2 = SparseMatrix(matrixFilePath=file2)

        print("Choose an operation:\n1. Addition\n2. Subtraction\n3. Multiplication")
        choice = input("Enter choice (1/2/3): ")

        result = None
        output_file = "result_matrix.txt"

        if choice == "1":
            result = matrix1.add(matrix2)
            print("Addition performed successfully. Result saved in 'result_matrix.txt'.")
        elif choice == "2":
            result = matrix1.subtract(matrix2)
            print("Subtraction performed successfully. Result saved in 'result_matrix.txt'.")
        elif choice == "3":
            result = matrix1.multiply(matrix2)
            print("Multiplication performed successfully. Result saved in 'result_matrix.txt'.")
        else:
            print("Invalid choice!")
            return
        
        result.save_to_file(output_file)

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
