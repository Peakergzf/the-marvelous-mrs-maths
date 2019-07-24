import itertools


class Matrix:

    def __init__(self, mat):

        self.mat = mat
        self.m = len(mat)  # the number of rows
        self.n = len(mat[0])  # the number of columns
        for row in mat:
            assert len(row) == self.n

    def __getitem__(self, idx):
        return self.mat[idx]

    def __setitem__(self, idx, lst):
        self.mat[idx] = lst

    def __str__(self):
        str_rep = ""
        for row in self.mat:
            for elem in row:
                str_rep += str(elem) + ' '
            str_rep += '\n'
        return str_rep

    def __mul__(self, other):
        assert other.m == self.n
        m, n = self.m, self.n
        r = other.n

        prod = [[0 for _ in range(r)] for _ in range(n)]

        for i in range(m):
            for j in range(r):
                for k in range(n):
                    prod[i][j] += self[i][k] * other[k][j]

        return Matrix(prod)

    @staticmethod
    def identity(n):
        return Matrix([[1 if i == j else 0 for i in range(n)] for j in range(n)])

    def __pow__(self, exponent):
        assert self.m == self.n
        power = Matrix.identity(self.n)
        for _ in range(exponent):
            power = self * power
        return power

    def __eq__(self, other):
        return self.mat == other.mat

    def __add__(self, other):
        assert self.m == other.m
        assert self.n == other.n
        return Matrix([[self[i][j] + other[i][j] for j in range(self.n)] for i in range(self.m)])

    def __sub__(self, other):
        assert self.m == other.m
        assert self.n == other.n
        return Matrix([[self[i][j] - other[i][j] for j in range(self.n)] for i in range(self.m)])

    def scalar_mul(self, k):
        return Matrix([[k * self[i][j] for j in range(self.n)] for i in range(self.m)])

    def transpose(self):
        return Matrix([[self[j][i] for j in range(self.m)] for i in range(self.n)])

    def is_symmetric(self):
        return self == self.transpose()

    def trace(self):
        assert self.m == self.n
        return sum([self[i][i] for i in range(self.n)])

    def gaussian_elimination(self):
        """
        transform the matrix to (row) echelon form
        """
        # perform the following on each row
        for k in range(self.m):

            for i in range(k, self.m):  # for each row
                if self[i][k] != 0:  # if the first entry is nonzero
                    self[k], self[i] = self[i], self[k]  # interchange with top row
                    break

            for i in range(1 + k, self.m):  # for each row below the top row
                mul = self[i][k] / self[k][k]
                for j in range(self.n):
                    # subtract multiples of the top row from each row so that the pivot becomes zero
                    self[i][j] -= mul * self[k][j]

    def gauss_jordan_elimination(self):
        """
        transform the matrix to reduced (row) echelon form
        """
        # perform gaussian elimination
        self.gaussian_elimination()

        # multiply each nonzero row by the reciprocal of the pivot in that row
        for i in range(self.m):
            if sum(self[i]) != 0:
                k = 0
                while self[i][k] == 0:
                    k += 1
                pivot = self[i][k]
                for j in range(k, self.n):
                    self[i][j] /= pivot

        # make each pivot the only nonzero entry in that column
        for k in range(self.m - 1, 0, -1):
            if sum(self[k]) != 0:
                for i in range(k - 1, -1, -1):  # for each row above the bottom row
                    mul = self[i][k] / self[k][k]
                    for j in range(len(self[i])):
                        self[i][j] -= mul * self[k][j]

    def is_invertible(self):
        if self.m != self.n:
            return False

        copy = Matrix([[self[i][j] for j in range(self.n)] for i in range(self.m)])
        copy.gauss_jordan_elimination()

        return copy == Matrix.identity(self.n)

    def inverse(self):
        assert self.is_invertible()

        # construct the partitioned matrix [A|I]
        ai = Matrix([self[i] + Matrix.identity(self.n)[i] for i in range(self.m)])

        # perform elementary row operations on [A|I]
        # bringing A to its reduced echelon form I and [A|I] to some matrix [I|B]
        ai.gauss_jordan_elimination()

        # B = A^(-1)
        return Matrix([[row[i] for i in range(self.m, 2 * self.m)] for row in ai])

    def determinant(self):
        assert self.m == self.n

        def sgn(p):
            # the signature of a permutation := (-1)^inversion number (i.e. the # of inversions)
            inv = 0
            for i in range(self.n):
                for j in range(i + 1, self.m):
                    if p[i] > p[j]:  # an inversion found
                        inv += 1
            return (-1) ** inv

        det = 0
        for perm in list(itertools.permutations([i for i in range(self.n)])):
            prod = sgn(perm)
            for i in range(self.n):
                prod *= self[perm[i]][i]
            det += prod

        return det


def main():
    a = Matrix([[2, 1, 1, 5], [4, 1, 3, 9], [-2, 2, 1, 8]])
    a.gauss_jordan_elimination()
    assert [[int(entry) for entry in row] for row in a] == [[1, 0, 0, 0], [0, 1, 0, 3], [0, 0, 1, 2]]

    b = Matrix([[1, 2, -1, 1, 3], [1, 1, -1, 1, 1], [1, 3, -1, 1, 5]])
    b.gauss_jordan_elimination()
    assert [[int(entry) for entry in row] for row in b] == [[1, 0, -1, 1, -1], [0, 1, 0, 0, 2], [0, 0, 0, 0, 0]]

    c = Matrix([[0, 2, 1, -8], [1, -2, -3, 0], [-1, 1, 2, 3]])
    c.gauss_jordan_elimination()
    assert [[int(entry) for entry in row] for row in c] == [[1, 0, 0, -4], [0, 1, 0, -5], [0, 0, 1, 2]]

    d = Matrix([[1, 2, 4], [3, 1, 0], [5, 5, 8]])
    assert (not d.is_invertible())

    e = Matrix([[1, 1, 3], [0, 2, 0], [1, 4, 4]])
    assert e.inverse() == Matrix([[4.0, 4.0, -3.0], [0.0, 0.5, 0.0], [-1.0, -1.5, 1.0]])

    assert d.determinant() == 0
    assert e.determinant() == 2


if __name__ == '__main__':
    main()
