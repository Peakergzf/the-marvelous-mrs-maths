#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

// generate all groups of order n (for small n) using batracking

// constraints: property of the identity, sudoku property, group isomorphism

// suppose the elements in a group are represented by 0, 1, 2, ..., n-1 and 0 is the identity, 
// the binary operation is represented in cayley table:
// table[i][j] = i * j, for i,j between 0 and n-1, and * is the binary operation

const int EMPTY = -1;

set<vvi> visited;
set<vvi> ans;

void print_table(vvi table) {
    for (auto row : table) {
        for (auto elem : row) {
            cout << elem << " ";
        }
        cout << endl;
    }
    // print a dash line at the end
    for (int i = 0; i < (int)table.size(); i++) {
        cout << "- "; 
    }
    cout << endl;
}

bool table_complete(vvi table) {
    // return true if the cayley table is complete (all entries are filled)
    // false otherwise

    for (auto row : table) {
        for (auto elem : row) {
            if (elem == EMPTY) return false;
        }
    }
    return true;
}

vi sudoku_property(vvi table, int row, int col) {
    // return a list of available values for entry table[row][col]
    // that satisfy the sudoku property (so far)

    int n = table.size();

    vi avail(n);
    iota(avail.begin(), avail.end(), 0); // initially {0, 1, ..., n - 1}

    // remove all the values that already occur in the current row
    for (int i = 0; i < n; i++) {
        if (table[row][i] != EMPTY) {
            avail.erase(remove(avail.begin(), avail.end(), table[row][i]), avail.end());
        }
    }
    // remove all the values that already occur in the current column
    for (int i = 0; i < n; i++) {
        if (table[i][col] != EMPTY) {
            avail.erase(remove(avail.begin(), avail.end(), table[i][col]), avail.end());
        }
    }

    return avail;

}

void rec(vvi table) {
    int n = table.size();

    // stop searching if visited
    if (visited.count(table)) return;

    visited.insert(table);

    // add to ans if table is complete
    if (table_complete(table)) ans.insert(table);

    for (int i = 1; i < n; i++) {
        for (int j = 1; j < n; j++) {
            if (table[i][j] == EMPTY) {
                vi avail_elems = sudoku_property(table, i, j);
                for (auto elem : avail_elems) {
                    table[i][j] = elem;
                    rec(table);
                    // backtracking
                    table[i][j] = EMPTY;
                }
            }
        }
    }

}

void group_of_order(int n) {
    vvi group = {};
    
    // using the property of the identity allows us to fill in 
    // the first row and the first column of the cayley table

    // e.g. when n = 4
    
    // group = {
    //     {0, 1, 2, 3},
    //     {1, EMPTY, EMPTY, EMPTY},
    //     {2, EMPTY, EMPTY, EMPTY},
    //     {3, EMPTY, EMPTY, EMPTY}
    // }

    vi fst_row(n); // {1, 2, ..., n}
    iota(fst_row.begin(), fst_row.end(), 0);
    group.push_back(fst_row);

    for (int i = 1; i < n; i++) {
        vi row(n, EMPTY);
        row[0] = i; // each entry of the first column
        group.push_back(row);
    }

    // using backtracking to fill in the rest of the cayley table
    rec(group);
}

int main() {
    group_of_order(4);
    for (auto table : ans) print_table(table);

    return 0;
}
