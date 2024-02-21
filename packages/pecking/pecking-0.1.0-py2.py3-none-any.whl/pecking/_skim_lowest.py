import itertools as it
import statistics
import typing
import warnings

import numpy as np
from scipy import stats as scipy_stats


def skim_lowest(
    samples: typing.Sequence[typing.Sequence[float]],
    labels: typing.Optional[typing.Sequence[typing.Union[str, int]]] = None,
    alpha: float = 0.05,
    reverse: bool = False,
) -> typing.List[typing.Union[str, int]]:
    """Identify the set of lowest-ranked groups that are statistically
    indistinguishable amongst themselves based on a Kruskal-Wallis H-test
    followed by multiple Mann-Whitney U-tests.

    Parameters
    ----------
    samples : Sequence[Sequence[float]]
        A sequence of sequences, where each inner sequence represents a sample group with numerical data.
    labels : Optional[Sequence[Union[str, int]]], optional
        A sequence of labels corresponding to each sample group.

        If not provided, numeric labels starting from 0 are assigned.
    alpha : float, default 0.05
        Significance level for the statistical tests.

        Used to determine if the difference between groups is significant.
    reverse : bool, default False
        If True, skims the highest ranked samples instead of the lowest.

        Prefer `pecking.skim_highest` for better readability.

    Returns
    -------
    List[Union[str, int]]
        A list of labels corresponding to the skimmed sample groups. Returns an empty list if no groups are significantly different.

    Raises
    ------
    ValueError
        If fewer than two samples are provided.

    Notes
    -----
    The function first applies a Kruskal-Wallis H-test to determine if there is a significant difference between any of the sample groups. If a significant difference is found, it proceeds to rank the sample groups and uses multiple Mann-Whitney U-tests to skim the lowest ranked groups, adjusting the significance level (`alpha`) for multiple comparisons according to a
    sequential Holm-Bonferroni program.

    Examples
    --------
    >>> samples = [[1, 2, 3, 4, 5], [2, 3, 4, 4, 4], [8, 9, 7, 6, 4]]
    >>> labels = ['Group 1', 'Group 2', 'Group 3']
    >>> skim_lowest(samples, labels)
    ['Group 1']
    """
    if len(samples) < 2:
        raise ValueError("At least two samples are required.")

    if labels is None:
        labels = [*range(len(samples))]

    h, p_kruskal = scipy_stats.kruskal(*samples)
    assert 0 <= p_kruskal <= 1
    if p_kruskal > alpha:
        return []

    population = sorted([*it.chain(*samples)], reverse=reverse)

    def get_rank(value: float) -> float:
        return np.mean(
            [
                np.searchsorted(population, value, side="left"),
                np.searchsorted(population, value, side="right"),
            ],
        )

    rank_means = [statistics.mean(map(get_rank, sample)) for sample in samples]
    slice_ = slice(None, None, -1) if reverse else slice(None, None)
    rank_mean_order = np.argsort(rank_means)[slice_]

    skimmed = []
    for i, position in enumerate(rank_mean_order):
        if i == 0:
            skimmed.append(labels[position])
            continue

        alpha_ = alpha / i
        u, p = scipy_stats.mannwhitneyu(
            samples[position],
            samples[rank_mean_order[0]],
            alternative="less" if reverse else "greater",
        )
        assert 0 <= p <= 1
        if p > alpha_:
            skimmed.append(labels[position])
        else:
            break

    if len(skimmed) == len(labels):
        warnings.warn(
            "Lowest ranked group and highest ranked group are "
            "indistinguishable by Mann-Whitney U test, in contradiction to "
            f"Kruskal-Wallis test result p={p_kruskal}.",
        )
        return []
    else:
        return skimmed
