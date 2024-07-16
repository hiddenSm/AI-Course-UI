# Sepehr Moniri
# 981813205

import SnakesAndLaddersQl, SnakeAndLadderBfs


if __name__ == '__main__':
    print('Q-Learning : 1\nDFS : 2')
    choosen_algorithm = int(input('Enter the algorithm you like: '))
    # print('\n')

    if choosen_algorithm == 1:
        SnakesAndLaddersQl.main()

    elif choosen_algorithm == 2:
        SnakeAndLadderBfs.main()

    else:
        print('The input must be 1 (for Q-Learning) or 2 (for DFS).')