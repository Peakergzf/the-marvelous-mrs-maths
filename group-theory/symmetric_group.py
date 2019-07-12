"""
Symmetric group Sn

1. Conversions between different notations for permutations.
2. Composition of permutations.
3. Cyclic subgroup in the Symmetric group Sn.

Note on notations for permutations:
1. one-line notation:
    since perm is a bijection from {1..n} to {1..n} but python list uses zero based index,
    we set perm[0] to be always -1.
    e.g. perm = [-1, 6, 5, 3, 7, 1, 2, 4]
         perm maps i to perm[i] for all 1 <= i <= n.
2. disjoint cycle notation:
    although "loners" (cycle of length 1) can be ignored, we always include them
    e.g. perm = [[1, 6, 2, 5], [4, 7], [3]]
         in each cycle perm maps cyc[i] to cyc[(i + 1) % cyc_len].
"""


def cycle_to_one_line(perm, n):
    """
    convert from disjoint cycle to one-line notation
    :param perm: a permutation in disjoint cycle notation
    :param n: Sn
    :return: the converted permutation in one-line notation
    e.g.
    from [[1, 6, 2, 5], [4, 7], [3]] to [-1, 6, 5, 3, 7, 1, 2, 4]
    """
    ans = [-1 for _ in range(n + 1)]
    for cyc in perm:
        for i in range(len(cyc)):
            ans[cyc[i]] = cyc[(i + 1) % len(cyc)]
    return ans


def one_line_to_cycle(perm, n):
    """
    convert from one-line to disjoint cycle notation
    :param perm: a permutation in one-line notation
    :param n: Sn
    :return: the converted permutation in disjoint cycle notation
    e.g.
    from [-1, 6, 5, 3, 7, 1, 2, 4] to [[1, 6, 2, 5], [4, 7], [3]]
    """

    # the permutation in disjoint cycle notation
    ans = []

    # current index in perm;
    # perm maps from idx to perm[idx],
    # idx and perm[idx] are the two adjacent numbers in a cycle
    idx = 1

    # current cycle
    cyc = [1]

    # seen[i] = True if i is already in ans, False otherwise
    seen = [False for _ in range(n + 1)]
    seen[1] = True

    while not _enough_elements(ans, n):
        # if there are still numbers in the current cycle
        if perm[idx] not in cyc:
            cyc.append(perm[idx])
            seen[perm[idx]] = True
            idx = perm[idx]
        # if the current cycle is complete (i.e. cycle back to the first number in the cycle)
        else:
            ans.append(cyc)
            # find the next unseen(unmapped) number
            for i in range(1, n + 1):
                if not seen[i]:
                    idx = i
                    break
            cyc = [idx]
            seen[idx] = True

    return ans


def _enough_elements(perm, n):
    """
    check if the given permutation in disjoint cycle notation in Sn maps n numbers
    """
    tot_len = 0
    for cyc in perm:
        tot_len += len(cyc)
    return tot_len == n


def identity(n):
    """
    :return: the identity in Sn in one-line notation [-1, 1, 2, ..., n]
    """
    return [-1] + [i for i in range(1, n + 1)]


def composition(sgm, tau, n):
    """
    compose two permutations sigma and tau in Sn (in one-line notation)
    (sgm.tau means "do tau first, then do sgm")
    e.g.
    if sgm = [3 1 2] and tau = [2 1 3]
    then 1 2 3 --tau--> 2 1 3 --sgm--> 1 3 2
    so sgm.tau = [1 3 2]
    """
    ans = [-1 for _ in range(n + 1)]
    for i in range(1, n + 1):
        ans[i] = sgm[tau[i]]
    return ans


def cyclic_subgroup(perm, n):
    """
    :return: the cyclic subgroup generated by perm in Sn (in disjoint cycle notation) and
    :return: the order of perm = the order of <perm> = the # of elements in <perm>
    """
    perm = cycle_to_one_line(perm, n)
    cur = perm
    subgroup = [one_line_to_cycle(cur, n)]

    # keep composing perm with itself until get the identity
    while cur != identity(n):
        cur = composition(cur, perm, n)
        subgroup.append(one_line_to_cycle(cur, n))

    return subgroup, len(subgroup)


def cycle_type(perm):
    """
    :param perm: a permutation (in disjoint cycle notation)
    :return: the cycle type of perm

    suppose perm consists of k disjoint cycles of lengths l1, ..., lk, where we include cycles of length 1,
    then we say the cycle type of perm is [l1, ..., lk] where the list is in non-increasing order
    e.g. [[1, 4, 3, 7, 10], [2], [5, 9], [6, 8]] has cycle type [5, 2, 2, 1]
    """
    cycle_len = [len(cycle) for cycle in perm]
    cycle_len.sort(reverse=True)
    return cycle_len


def is_even_permutation(perm):
    """
    :param perm: a permutation (in disjoint cycle notation)
    :return: True if perm is even, False otherwise

    the parity of a permutation with cycle type [l1, ..., lk] is equal to
    the parity of the integer l1 + ... + lk - k
    """
    cyc_type = cycle_type(perm)
    return (sum(cyc_type) - len(cyc_type)) % 2 == 0


def all_possible_permutations(n):
    """
    heap's algorithm
    generate all possible permutations of n objects (all elements in Sn)
    """

    ans = []

    # https://en.wikipedia.org/wiki/Heap%27s_algorithm#Details_of_the_algorithm

    def generate(k, a):
        if k == 1:
            ans.append([x for x in a])  # append the copied a
            return

        generate(k - 1, a)

        for i in range(k - 1):
            if k % 2 == 0:
                a[i], a[k - 1] = a[k - 1], a[i]
            else:
                a[0], a[k - 1] = a[k - 1], a[0]
            generate(k - 1, a)

    # # --------------------------------------------------------------------------
    # # https://en.wikipedia.org/wiki/Heap%27s_algorithm#Proof
    # # "the implementation below is not optimal but the analysis is easier"
    # # (please refer to the diagram) the green cycle arrows are the redundant works

    # def generate(k, a):
    #     if k == 1:
    #         ans.append([x for x in a])  # append the copied a
    #         return
    #
    #     for i in range(k):
    #         generate(k - 1, a)
    #         if k % 2 == 0:
    #             a[i], a[k - 1] = a[k - 1], a[i]
    #         else:
    #             a[0], a[k - 1] = a[k - 1], a[0]

    generate(n, [i for i in range(1, n + 1)])

    return ans


def main():
    subgroup = [
        [[1, 3, 4], [2, 6], [5]],
        [[1, 4, 3], [2], [5], [6]],
        [[1], [2, 6], [3], [4], [5]],
        [[1, 3, 4], [2], [5], [6]],
        [[1, 4, 3], [2, 6], [5]],
        [[1], [2], [3], [4], [5], [6]]
    ]
    assert cyclic_subgroup([[1, 3, 4], [2, 6], [5]], 6) == (subgroup, 6)

    assert all_possible_permutations(3) == [[1, 2, 3], [2, 1, 3], [3, 1, 2], [1, 3, 2], [2, 3, 1], [3, 2, 1]]

    assert cycle_type([[1, 4, 3, 7, 10], [2], [5, 9], [6, 8]]) == [5, 2, 2, 1]


if __name__ == '__main__':
    main()
