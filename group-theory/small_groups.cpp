#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

// ===============================================================================================
// generate all groups of order n (for small n) using batracking

// constraints: property of the identity, sudoku property

// suppose the elements in a group are represented by 0, 1, 2, ..., n-1 and 0 is the identity, 
// the binary operation is represented in cayley table:
// table[i][j] = i * j, for i,j between 0 and n-1, and * is the binary operation
// ===============================================================================================

const int EMPTY = -1;

set<vvi> visited;

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

    int n = table.size();
    for (int i = 1; i < n; i++) {
        for (int j = 1; j < n; j++) {
            if (table[i][j] == EMPTY) return false;
        }
    }
    return true;
}

vi sudoku_property(vvi table, int row, int col) {
    // return a list of available values for entry table[row][col]
    // that satisfy the sudoku property (so far)

    int n = table.size();

    vector<bool> avail(n, true);
    for (int i = 0; i < n; i++) {
        if (table[i][col] != EMPTY) avail[table[i][col]] = false;
        if (table[row][i] != EMPTY) avail[table[row][i]] = false;
    }

    vi avail_val = {};
    for (int i = 0; i < n; i++) {
        if (avail[i]) avail_val.push_back(i);
    } 

    return avail_val;
}

void rec(vvi table) {
    int n = table.size();

    if (visited.count(table)) return;

    visited.insert(table);

    if (table_complete(table)) {
        print_table(table);
        return;
    }

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
    vvi table = {};
    
    // using the property of the identity allows us to fill in 
    // the first row and the first column of the cayley table

    // e.g. when n = 4
    
    // group = {
    //     {0, 1, 2, 3},
    //     {1, EMPTY, EMPTY, EMPTY},
    //     {2, EMPTY, EMPTY, EMPTY},
    //     {3, EMPTY, EMPTY, EMPTY}
    // }

    vi fst_row(n);
    iota(fst_row.begin(), fst_row.end(), 0); // {0, 1, ..., n-1}
    table.push_back(fst_row);

    for (int i = 1; i < n; i++) {
        vi row(n, EMPTY);
        row[0] = i; // each entry of the first column
        table.push_back(row);
    }

    // using backtracking to fill in the rest of the cayley table
    rec(table);
}

// ===============================================================================================
// check if two groups are isomorphic
// by considering all possible renaming of one group and 
//    comparing with the other to see if the renaming is consistent
// ===============================================================================================

bool comp(vi v1, vi v2) {
    // used in rearranging entries in the cayley table for rename_elements
    return v1[0] < v2[0];
}

vvi transpose(vvi g) {
    // return the transpose of matrix g
    int n = g.size();
    vvi gt;
    for (int i = 0; i < n; i++) {
        vi row(n);
        gt.push_back(row);

        for (int j = 0; j < n; j++) {
            gt[i][j] = g[j][i];
        }
    }
    return gt;
}

vvi rename_elements(vi perm, vvi g) {
    int n = g.size();
    vvi g1;

    // apply renaming based on the permutation
    for (int i = 0; i < n; i++) {
        vi row(n);
        g1.push_back(row);

        for (int j = 0; j < n; j++) {
            g1[i][j] = perm[g[i][j]];
        }
    }

    // rearrage the table s.t. the first row and column are both {0, 1, ..., n-1}

    // sort rows
    sort(g1.begin(), g1.end(), comp);
    // sort columns (i.e. sort rows of g1 transpose)
    vvi g1t = transpose(g1);
    sort(g1t.begin(), g1t.end(), comp);
    vvi g2 = transpose(g1t);

    return g2;
}

bool same_group(vvi g, vvi h) {
    // two groups are the same if they have the same cayley table
    int n = g.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (g[i][j] != h[i][j]) return false;
        }
    }
    return true;
}

bool isomorphic(vvi g, vvi h) {
    // return true if g and h are isomorphic, false otherwise
    //     by generating all possible ways to rename elements in g
    //     and checking if it's the same as h
    
    // the renaming is based on each permutation
    int n = g.size();
    vi perm(n);
    iota(perm.begin(), perm.end(), 0);
    do {
        vvi g1 = rename_elements(perm, g);

        if (same_group(g1, h)) return true;

    } while (next_permutation(perm.begin(), perm.end()));
    
    return false;
}

// ===============================================================================================

int main() {
    group_of_order(4);
    
    vvi g1 = {
        {0, 1, 2, 3},
        {1, 0, 3, 2},
        {2, 3, 0, 1},
        {3, 2, 1, 0}
    };

    vvi g2 = {
        {0, 1, 2, 3},
        {1, 0, 3, 2},
        {2, 3, 1, 0},
        {3, 2, 0, 1}
    };

    vvi g3 = {
        {0, 1, 2, 3},
        {1, 2, 3, 0},
        {2, 3, 0, 1},
        {3, 0, 1, 2}
    };

    vvi g4 = {
        {0, 1, 2, 3},
        {1, 3, 0, 2},
        {2, 0, 3, 1},
        {3, 2, 1, 0}
    };

    // g2, g3, g4 are isomorphic to each other
    // and they are not isomorphic to g1
    vector<vvi> groups = {g2, g3, g4};
    for (auto g : groups) {
        assert(!isomorphic(g, g1));
        for (auto h : groups) {
            assert(isomorphic(g, h));
        }
    }

    return 0;
}
