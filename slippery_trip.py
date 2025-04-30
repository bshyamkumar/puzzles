"""
This is a puzzle from Meta's website:
https://www.metacareers.com/profile/coding_puzzles?puzzle=2881982598796847
I put this solution here when I realized that what I thought was a straightforward
solution doesn't pass their tests. So, I spent some time trying to figure out why
and realized that the solution accepted at that link is incorrect. It wasn't trivial
to figure this out since their tests don't show the output. I added an
example to show why this solution is correct. You can uncomment line 55 to pass the
tests at that link, or accept this correct solution.
Solution:
There are three choices in any row j: keep going down, go right and then down, or
keep going to the right because there is a ">" but no "V". With the first choice,
we get at most one coin. With the second choice we need to maximize the coins collected
for that row. The third choice competes with the first -is it better to collect one
coin and go to the next row, or is it better to collect all the coins in that row?
If you encounter this in row j, then you need to process all the rows after j
in order to make that decision. Let's say that we calculate the three options for every
row. That is for each row, we compute (M, and C) where C implies that we stop
with that row because there is no "V" in that row.
If there is no ">" in the row, the choice for the row is just
   M = min(1, num coins in the row)
If there is no "V" in the row, but there is ">", then the choice is between M=1 and C.
If there is an ">" and a "V", then there is an optimal M to be computed.
In addition, if  we choose C for some row j in the second scenario, there are no
choices for the remaining rows after j. We can also stop computing after some row j
if there is no way to get past row j (sample test case #3).
Let S_i,j be the optimal sum collected from rows i to j inclusive. Then,
S_j,R = max(M_j + S_(j+1,R), C_j)
"""
from typing import List


def get_max_coins(R: int, C: int, G: List[List[str]]) -> int:
    def get_max_from_row(row: str) -> [int, bool, bool]:
        # Return max count, whether you can go down, and whether row is terminal.
        ncols = len(row)
        assert ncols == C
        first_down, max_c, rights = -1, 0, 0
        for ii, cc in enumerate(row):
            if cc == "v":
                first_down = ii
            elif cc == '*':
                max_c += 1
            elif cc == '>':
                rights += 1
        if rights == ncols:
            return 0, False, True
        if first_down == -1:
            return (max_c if rights > 0 else min(1, max_c), False, False)
        if max_c == 0:
            return 0, True, False
        found_right = False
        steps, index, count = 1, first_down, 0
        max_c = 1
        # uncomment the next line to pass official tests at the link provided above.
        # max_c = 0 if rights > 0 else 1
        while steps <= ncols:
            cc = row[index]
            if cc == "*":
                if found_right:
                    count += 1
            elif cc == "v":
                if found_right:
                    max_c = max(max_c, count)
                else:
                    max_c = max(max_c, min(1, count))
                count = 0
                found_right = False
            elif cc == ">":
                found_right = True
            steps += 1
            index = (index + 1) % ncols
        return max(max_c, count), True, False

    stack = []
    for ii in range(R):
        m_r, has_down, terminal = get_max_from_row(G[ii])
        if terminal:
            break
        stack.append((m_r, has_down))
    running_sum = 0
    while stack:
        m_r, has_down = stack.pop()
        if not has_down:
            running_sum = max(min(1, m_r) + running_sum, m_r)
        else:
            running_sum += m_r
    return running_sum


if __name__ == '__main__':
    assert 4 == get_max_coins(3, 4, [".***", "**v>", ".*.."])
    assert 4 == get_max_coins(3, 3, [">**", "*>*", "**>"])
    assert 0 == get_max_coins(2, 2, [">>", "**"])
    assert 6 == get_max_coins(4, 6, [">*v*>*", "*v*v>*", ".*>..*",
                                     ".*..*V"])
    rows = ["*v*>**vv*>", ".**v*.>*v>", ">>vv.*.v>*", ".vvv>..*>>", "*>>v*.*v>.",
            ">*>v..>>..", "*>*>.v*>v*", "v>*v..**.v", "v*****v>>*", ".*vv*.v**>",
            "v.v.>>..vv", ".*.>*vv>v.", "...v.**vv.", ">>v*.*>.v.", ">v.>>v.*v>",
            ">v>v>...v.", ".v>*>*.vv*", "**.>*vv*v.", ">*v.>.>v>*", ".>.v****>>",
            "..*v.*.>*.", "**>>v*.v>v", "v.vvv.>v.>", ">>v>**v...", ".*v*vv.>v*",
            ".v>v.**vv*", "v.*.vv.*.v", ">>>v*.*v.*", ">>**...>*>", "vv*vv>.*v.",
            "vvvv**.vvv", ".>.>>>.v.*", "vv*>vv*>>>", "*.*.>.>.>v"]
    assert 37 == get_max_coins(34, 10, rows)
