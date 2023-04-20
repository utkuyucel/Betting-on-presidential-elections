import random
from enum import Enum, auto


class ElectionOutcome(Enum):
    """Enumeration for possible election outcomes."""
    ERDOGAN_WIN_FIRST = auto()
    OPPOSITE_WIN_FIRST = auto()
    ERDOGAN_WIN_SECOND = auto()
    OPPOSITE_WIN_SECOND = auto()
    INCE_WIN_FIRST = auto()
    INCE_WIN_SECOND = auto()
    OGAN_WIN_FIRST = auto()
    OGAN_WIN_SECOND = auto()
    WAR = auto()


class Election:
    """Represents an election with bet amounts for each possible outcome."""

    def __init__(self):
        self.bet_amounts = {outcome: 0 for outcome in ElectionOutcome}


class Bet:
    """Represents a single bet made by a user."""

    def __init__(self, user, election_outcome, amount):
        self.user = user
        self.election_outcome = election_outcome
        self.amount = amount

    def __str__(self):
        return f'{self.user} bets {self.amount} on {self.election_outcome.name}'


class BettingSystem:
    """Manages bets and calculates odds for an election."""

    def __init__(self, election: Election):
        self.election = election
        self.bets = []

    def place_bet(self, user: str, election_outcome: ElectionOutcome, amount: float) -> None:
        """Places a bet on a given election outcome."""
        bet = Bet(user, election_outcome, amount)
        self.bets.append(bet)
        self.election.bet_amounts[election_outcome] += amount

    def calculate_odds(self) -> dict[ElectionOutcome, float]:
        """Calculates the odds for each election outcome based on total bet amounts."""
        total_bet_amounts = sum(self.election.bet_amounts.values())
        odds = {
            outcome: total_bet_amounts / amount if amount > 0 else 1
            for outcome, amount in self.election.bet_amounts.items()
        }
        return odds

    def settle_bets(self, actual_outcome: ElectionOutcome) -> list[tuple[str, float]]:
        """Settles bets based on the actual election outcome and returns the winnings for each winner."""
        winners = [bet for bet in self.bets if bet.election_outcome == actual_outcome]
        total_correct_bets = sum(bet.amount for bet in winners)
        total_bet_amounts = sum(self.election.bet_amounts.values())
        results = [(winner.user, (winner.amount / total_correct_bets) * total_bet_amounts) for winner in winners]
        return results


def main() -> None:
    """Main function to simulate the betting system for an election."""
    election = Election()
    betting_system = BettingSystem(election)

    bet_placements = [
        ('UXXX', ElectionOutcome.ERDOGAN_WIN_FIRST, 50),
        ('BXXX', ElectionOutcome.ERDOGAN_WIN_FIRST, 50),
        ('HXXX', ElectionOutcome.ERDOGAN_WIN_FIRST, 50),
        ('MXXX', ElectionOutcome.OPPOSITE_WIN_FIRST, 50),
        ('GXXX', ElectionOutcome.OPPOSITE_WIN_FIRST, 50),
        ('DXXX', ElectionOutcome.WAR, 50),
    ]

    for user, outcome, amount in bet_placements:
        betting_system.place_bet(user, outcome, amount)
        print(f'{user} placed ₺{amount} bet.')

    odds = betting_system.calculate_odds()
    print("\nOdds for each outcome:")
    for outcome, odd in odds.items():
        print(f'{outcome.name}: {odd:.2f}')

    actual_outcome = ElectionOutcome.WAR
    results = betting_system.settle_bets(actual_outcome)

    print(f'\nElection outcome is: {actual_outcome.name}')
    print('\nWinners and their winnings:')
    for user, winnings in results:
        print(f'{user}: ₺{winnings:.2f}')


if __name__ == "__main__":
    main()

