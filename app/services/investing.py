from datetime import datetime
from typing import List, Protocol


class InvestmentUnit(Protocol):
    full_amount: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime


def distribute_investment(
        source: InvestmentUnit,
        targets: List[InvestmentUnit]) -> List[InvestmentUnit]:
    changed_targets = []
    for target in targets:
        investment = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for unit in [source, target]:
            unit.invested_amount += investment
            if unit.full_amount == unit.invested_amount:
                unit.fully_invested = True
                unit.close_date = datetime.utcnow()
        changed_targets.append(target)

    return changed_targets
