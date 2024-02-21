import typing

from ._skim_lowest import skim_lowest


def skim_highest(
    samples: typing.Sequence[typing.Sequence[float]],
    labels: typing.Optional[typing.Sequence[typing.Union[str, int]]] = None,
    alpha: float = 0.05,
) -> typing.List[typing.Union[str, int]]:
    """Identify the set of highest-ranked groups that are statistically
    indistinguishable amongst themselves based on a Kruskal-Wallis H-test
    followed by multiple Mann-Whitney U-tests.

    See `pecking.skim_lowest` for parameter and return value descriptions.
    """
    return skim_lowest(
        samples,
        labels,
        alpha,
        reverse=True,
    )
