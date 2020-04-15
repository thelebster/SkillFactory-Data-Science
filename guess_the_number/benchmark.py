from guess_the_number import game_core_v1
from guess_the_number import game_core_v2
from guess_the_number import game_core_v3
from guess_the_number import score_game


def run_benchmarking():
    """Run benchmarking to score effectiveness of all algorithms."""
    print('Run benchmarking for game_core_v1: ', end='')
    score_game(game_core_v1)

    print('Run benchmarking for game_core_v2: ', end='')
    score_game(game_core_v2)

    print('Run benchmarking for game_core_v3: ', end='')
    score_game(game_core_v3)


run_benchmarking()
