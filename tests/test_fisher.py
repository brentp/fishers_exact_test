import numpy as np
import pytest

from fisher import pvalue, pvalue_npy
from fisher.cfisher import pvalue_population, PValues


EPSILON = 1e-10


# ---------------------------------------------------------------------------
# Accuracy against R's fisher.test (R 3.2.2, sprintf(".16f"))
# ---------------------------------------------------------------------------
# Each entry: (2x2 table, (left_tail, right_tail, two_tail))
R_VALIDATED_CASES = [
    ([[100, 2], [1000, 5]],
     (0.1300759363430016, 0.9797904453147230, 0.1300759363430016)),
    ([[2, 100], [5, 1000]],
     (0.9797904453147230, 0.1300759363430016, 0.1300759363430016)),
    ([[2, 7], [8, 2]],
     (0.0185217259520665, 0.9990149169715733, 0.0230141375652212)),
    ([[5, 1], [10, 10]],
     (0.9782608695652173, 0.1652173913043478, 0.1973244147157191)),
    ([[5, 15], [20, 20]],
     (0.0562577507439996, 0.9849086665340765, 0.0958044001247763)),
    ([[5, 16], [20, 25]],
     (0.0891382278309642, 0.9723490195633506, 0.1725864953812995)),
    ([[10, 5], [10, 1]],
     (0.1652173913043479, 0.9782608695652174, 0.1973244147157192)),
    ([[10, 5], [10, 0]],
     (0.0565217391304348, 1.0000000000000000, 0.0612648221343874)),
    ([[5, 0], [1, 4]],
     (1.0000000000000000, 0.0238095238095238, 0.0476190476190476)),
    ([[0, 5], [1, 4]],
     (0.5000000000000000, 1.0000000000000000, 1.0000000000000000)),
    ([[5, 1], [0, 4]],
     (1.0000000000000000, 0.0238095238095238, 0.0476190476190476)),
    ([[0, 1], [3, 2]],
     (0.4999999999999999, 1.0000000000000000, 1.0000000000000000)),
]


@pytest.mark.parametrize("table,expected", R_VALIDATED_CASES)
def test_pvalue_against_r(table, expected):
    """Core accuracy: p-values must match R's fisher.test."""
    p = pvalue(table[0][0], table[0][1], table[1][0], table[1][1])
    assert abs(p.left_tail - expected[0]) < EPSILON
    assert abs(p.right_tail - expected[1]) < EPSILON
    assert abs(p.two_tail - expected[2]) < EPSILON


# ---------------------------------------------------------------------------
# P-value mathematical properties
# ---------------------------------------------------------------------------
class TestPvalueProperties:
    """Verify mathematical invariants that must hold for any valid input."""

    @pytest.mark.parametrize("table", [t for t, _ in R_VALIDATED_CASES])
    def test_pvalues_in_unit_interval(self, table):
        """All p-values must be in [0, 1]."""
        p = pvalue(table[0][0], table[0][1], table[1][0], table[1][1])
        for val in (p.left_tail, p.right_tail, p.two_tail):
            assert 0.0 <= val <= 1.0

    def test_symmetric_table_gives_pvalue_one(self):
        """A perfectly balanced table should have two_tail = 1."""
        p = pvalue(5, 5, 5, 5)
        assert abs(p.two_tail - 1.0) < EPSILON

    def test_swapping_rows_swaps_tails(self):
        """Swapping rows should swap left and right tails."""
        p1 = pvalue(2, 7, 8, 2)
        p2 = pvalue(8, 2, 2, 7)
        assert abs(p1.left_tail - p2.right_tail) < EPSILON
        assert abs(p1.right_tail - p2.left_tail) < EPSILON
        assert abs(p1.two_tail - p2.two_tail) < EPSILON

    def test_swapping_columns_swaps_tails(self):
        """Swapping columns should swap left and right tails."""
        p1 = pvalue(2, 7, 8, 2)
        p2 = pvalue(7, 2, 2, 8)
        assert abs(p1.left_tail - p2.right_tail) < EPSILON
        assert abs(p1.right_tail - p2.left_tail) < EPSILON
        assert abs(p1.two_tail - p2.two_tail) < EPSILON

    def test_two_tail_le_sum_of_one_tails(self):
        """two_tail <= left_tail + right_tail (they overlap at the observed cell)."""
        p = pvalue(5, 15, 20, 20)
        assert p.two_tail <= p.left_tail + p.right_tail + EPSILON


# ---------------------------------------------------------------------------
# Degenerate / edge-case tables
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_all_in_one_cell(self):
        """All observations in a single cell."""
        p = pvalue(10, 0, 0, 0)
        assert abs(p.left_tail - 1.0) < EPSILON
        assert abs(p.right_tail - 1.0) < EPSILON
        assert abs(p.two_tail - 1.0) < EPSILON

    def test_zero_row(self):
        """One row is all zeros."""
        p = pvalue(0, 0, 3, 4)
        assert abs(p.left_tail - 1.0) < EPSILON
        assert abs(p.right_tail - 1.0) < EPSILON
        assert abs(p.two_tail - 1.0) < EPSILON

    def test_zero_column(self):
        """One column is all zeros."""
        p = pvalue(0, 5, 0, 10)
        assert abs(p.left_tail - 1.0) < EPSILON
        assert abs(p.right_tail - 1.0) < EPSILON
        assert abs(p.two_tail - 1.0) < EPSILON

    def test_strong_association(self):
        """Extreme association should give a very small two-tailed p-value."""
        p = pvalue(50, 0, 0, 50)
        assert p.two_tail < 1e-5

    def test_single_observation_per_cell(self):
        """Minimal non-degenerate table: [[1,0],[0,1]]."""
        p = pvalue(1, 0, 0, 1)
        # Only two possible tables, each with probability 0.5
        assert abs(p.two_tail - 1.0) < EPSILON


# ---------------------------------------------------------------------------
# pvalue_population (study/population parameterization)
# ---------------------------------------------------------------------------
class TestPvaluePopulation:
    def test_equivalent_to_pvalue(self):
        """pvalue_population should give identical results to pvalue
        when the same table is expressed in study/population form."""
        # Table: [[12, 5], [29, 2]]
        # a_true=12, a_false=5, b_true=29, b_false=2
        # => k=12, n=17, K=41, N=48
        p_direct = pvalue(12, 5, 29, 2)
        p_pop = pvalue_population(12, 17, 41, 48)
        assert abs(p_direct.left_tail - p_pop.left_tail) < EPSILON
        assert abs(p_direct.right_tail - p_pop.right_tail) < EPSILON
        assert abs(p_direct.two_tail - p_pop.two_tail) < EPSILON

    @pytest.mark.parametrize("table", [t for t, _ in R_VALIDATED_CASES])
    def test_population_matches_direct_all_cases(self, table):
        """Verify equivalence across all R-validated cases."""
        a, b, c, d = table[0][0], table[0][1], table[1][0], table[1][1]
        k = a
        n = a + b
        K = a + c
        N = a + b + c + d
        p_direct = pvalue(a, b, c, d)
        p_pop = pvalue_population(k, n, K, N)
        assert abs(p_direct.left_tail - p_pop.left_tail) < EPSILON
        assert abs(p_direct.right_tail - p_pop.right_tail) < EPSILON
        assert abs(p_direct.two_tail - p_pop.two_tail) < EPSILON


# ---------------------------------------------------------------------------
# pvalue_npy (vectorized NumPy interface)
# ---------------------------------------------------------------------------
class TestPvalueNpy:
    def test_matches_scalar_pvalue(self):
        """Vectorized results must match scalar pvalue for each row."""
        tables = [t for t, _ in R_VALIDATED_CASES]
        a = np.array([t[0][0] for t in tables], dtype=np.uint32)
        b = np.array([t[0][1] for t in tables], dtype=np.uint32)
        c = np.array([t[1][0] for t in tables], dtype=np.uint32)
        d = np.array([t[1][1] for t in tables], dtype=np.uint32)

        lefts, rights, twos = pvalue_npy(a, b, c, d)

        for i, (table, expected) in enumerate(R_VALIDATED_CASES):
            assert abs(lefts[i] - expected[0]) < EPSILON, f"left_tail mismatch at index {i}"
            assert abs(rights[i] - expected[1]) < EPSILON, f"right_tail mismatch at index {i}"
            assert abs(twos[i] - expected[2]) < EPSILON, f"two_tail mismatch at index {i}"

    def test_returns_correct_length(self):
        """Output arrays should have the same length as input."""
        n = 5
        a = np.ones(n, dtype=np.uint32)
        b = np.ones(n, dtype=np.uint32) * 2
        c = np.ones(n, dtype=np.uint32) * 3
        d = np.ones(n, dtype=np.uint32) * 4
        lefts, rights, twos = pvalue_npy(a, b, c, d)
        assert len(lefts) == n
        assert len(rights) == n
        assert len(twos) == n

    def test_single_element(self):
        """Should work with length-1 arrays."""
        a = np.array([12], dtype=np.uint32)
        b = np.array([5], dtype=np.uint32)
        c = np.array([29], dtype=np.uint32)
        d = np.array([2], dtype=np.uint32)
        lefts, rights, twos = pvalue_npy(a, b, c, d)
        p = pvalue(12, 5, 29, 2)
        assert abs(lefts[0] - p.left_tail) < EPSILON
        assert abs(rights[0] - p.right_tail) < EPSILON
        assert abs(twos[0] - p.two_tail) < EPSILON

    def test_output_dtype_is_float(self):
        """Output arrays should be float64."""
        a = np.array([1], dtype=np.uint32)
        b = np.array([2], dtype=np.uint32)
        c = np.array([3], dtype=np.uint32)
        d = np.array([4], dtype=np.uint32)
        lefts, rights, twos = pvalue_npy(a, b, c, d)
        assert lefts.dtype == np.float64
        assert rights.dtype == np.float64
        assert twos.dtype == np.float64


# ---------------------------------------------------------------------------
# PValues object behavior
# ---------------------------------------------------------------------------
class TestPValuesObject:
    def test_attributes_accessible(self):
        """PValues exposes left_tail, right_tail, two_tail as attributes."""
        p = pvalue(12, 5, 29, 2)
        assert hasattr(p, "left_tail")
        assert hasattr(p, "right_tail")
        assert hasattr(p, "two_tail")

    def test_repr(self):
        """repr should contain all three p-value labels."""
        p = pvalue(12, 5, 29, 2)
        r = repr(p)
        assert "left_tail=" in r
        assert "right_tail=" in r
        assert "two_tail=" in r
        assert r.startswith("PValues(")

    def test_comparison_raises(self):
        """Comparing a PValues object directly should raise an exception."""
        p = pvalue(12, 5, 29, 2)
        with pytest.raises(Exception, match="must compare with one of the attributes"):
            p < 0.05
        with pytest.raises(Exception, match="must compare with one of the attributes"):
            p == 0.05


# ---------------------------------------------------------------------------
# Table printer
# ---------------------------------------------------------------------------
class TestTablePrinter:
    def test_known_output(self):
        """Verify table printer produces expected ReST-formatted output."""
        from fisher.tableprinter import print_2x2_table

        table = [12, 5, 29, 2]
        s = print_2x2_table(
            table,
            row_labels=["Selected", "Not selected"],
            col_labels=["Having the property", "Not having the property"],
        )
        # Check structure
        assert "Selected" in s
        assert "Not selected" in s
        assert "Having the property" in s
        assert "total" in s
        # Check totals are computed correctly
        assert "17" in s   # row 1 total: 12 + 5
        assert "31" in s   # row 2 total: 29 + 2
        assert "41" in s   # col 1 total: 12 + 29
        assert "7" in s    # col 2 total: 5 + 2
        assert "48" in s   # grand total

    def test_output_has_rst_separators(self):
        """Output should have ReST-style '=' separator lines."""
        from fisher.tableprinter import print_2x2_table

        s = print_2x2_table([1, 2, 3, 4], ["A", "B"], ["X", "Y"])
        lines = s.strip().split("\n")
        # First and last lines should be separator lines (all = and spaces)
        for line in [lines[0], lines[-1]]:
            assert all(c in ("=", " ") for c in line)
