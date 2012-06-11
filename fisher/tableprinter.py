def print_2x2_table(table, row_labels, col_labels, fmt=None):
    """
    Prints a table used for Fisher's exact test. Adds row, column, and grand
    totals.

    :param table: The four cells of a 2x2 table: [r1c1, r1c2, r2c1, r2c2]
    :param row_labels: A length-2 list of row names
    :param col_labels: A length-2 list of column names

    """
    grand = sum(table)

    # Separate table into components and get row/col sums
    t11, t12, t21, t22 = table

    # Row sums, col sums, and grand total
    r1 = t11 + t12
    r2 = t21 + t22
    c1 = t11 + t21
    c2 = t12 + t22

    # Re-cast everything as the appropriate format
    t11, t12, t21, t22, c1, c2, r1, r2, grand = [
            "%d" % i for i in [t11, t12, t21, t22, c1, c2, r1, r2, grand]]

    # Construct rows and columns the long way...
    rows = [
            [""] + col_labels + ['total'],
            [row_labels[0], t11, t12, r1],
            [row_labels[1], t21, t22, r2],
            ['total', c1, c2, grand],
            ]

    cols = [
        row_labels,
        [col_labels[0], t11, t21, c1],
        [col_labels[1], t12, t22, c2],
        ['total', r1, r2, grand],
        ]

    # Get max column width for each column; need this for nice justification
    widths = []
    for col in cols:
        widths.append(max(len(i) for i in col))

    # ReST-formatted header
    sep = ['=' * i for i in widths]

    # Construct the table one row at a time with nice justification
    s = []
    s.append(' '.join(sep))
    s.append(' '.join(i.ljust(j) for i, j in zip(rows[0], widths)))
    s.append(' '.join(sep))
    for row in rows[1:]:
        s.append(' '.join(i.ljust(j) for i, j in zip(row, widths)))
    s.append(' '.join(sep) + '\n')
    return "\n".join(s)


if __name__ == "__main__":
    table = [12, 5, 29, 2]
    s = print_2x2_table(
            table,
            row_labels=['Selected', 'Not selected'],
            col_labels=['Having the property', 'Not having the property']
           )

    str_table = """
    ============ =================== ======================= =====
                 Having the property Not having the property total
    ============ =================== ======================= =====
    Selected     12                  5                       17   
    Not selected 29                  2                       31   
    total        41                  7                       48   
    ============ =================== ======================= =====
    """

    # For the test, remove the first newline and all common leading whitespace
    from textwrap import dedent
    str_table = "".join(str_table.splitlines(True)[1:])
    print s
    assert dedent(str_table) == s
