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

    @staticmethod
    def gauss_eli_aux(rows, k):
        if k == len(rows) - 1:
            return rows

        for i in range(k, len(rows)):  # for each row
            if rows[i][k] != 0:  # if the first entry is nonzero
                rows[k], rows[i] = rows[i], rows[k]  # interchange with top row
                break

        for i in range(1 + k, len(rows)):  # for each row below the top row
            mul = rows[i][k] / rows[k][k]
            for j in range(len(rows[i])):
                # subtract multiples of the top row from each row so that the pivot becomes zero
                rows[i][j] -= mul * rows[k][j]

        return Matrix.gauss_eli_aux(rows, k + 1)

    def gaussian_elimination(self):
        return Matrix(Matrix.gauss_eli_aux(self.mat, 0))

    @staticmethod
    def gau_jor_eli_aux(rows, k):
        if k == 0:
            return rows

        if sum(rows[k]) != 0:
            for i in range(k - 1, -1, -1):  # for each row above the bottom row
                mul = rows[i][k] / rows[k][k]
                for j in range(len(rows[i])):
                    rows[i][j] -= mul * rows[k][j]

        return Matrix.gau_jor_eli_aux(rows, k - 1)

    def gauss_jordan_elimination(self):
        # perform gaussian elimination
        self.gaussian_elimination()

        # multiply each nonzero row by the reciprocal of the pivot in that row
        for i in range(self.m):
            if sum(self[i]) != 0:
                k = 0
                while self[i][k] == 0:
                    k += 1
                p = self[i][k]
                for j in range(k, self.n):
                    self[i][j] /= p

        # make each pivot the only nonzero entry in that column
        return Matrix(Matrix.gau_jor_eli_aux(self.mat, self.m - 1))


def main():
    a = Matrix([[2, 1, 1, 5], [4, 1, 3, 9], [-2, 2, 1, 8]])
    b = Matrix([[1, 2, -1, 1, 3], [1, 1, -1, 1, 1], [1, 3, -1, 1, 5]])
    c = Matrix([[0, 2, 1, -8], [1, -2, -3, 0], [-1, 1, 2, 3]])
    print(a.gauss_jordan_elimination())
    print(b.gauss_jordan_elimination())
    print(c.gauss_jordan_elimination())


if __name__ == '__main__':
    main()
