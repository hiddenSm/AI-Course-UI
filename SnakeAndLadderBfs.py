# Sepehr Moniri
# 981813205

from collections import deque

class SnakeLadderGame:
    def __init__(self, dimensions, snakes, ladders):
        self.dimensions = dimensions
        self.snakes = snakes
        self.ladders = ladders

    def is_valid_move(self, position):
        return 1 <= position <= self.dimensions[0] * self.dimensions[1]

    def play_game(self):
        start = 1
        target = self.dimensions[0] * self.dimensions[1]

        visited = set()
        # (position, cost, path)
        queue = deque([(start, 0, [])])  

        while queue:
            current_position, current_cost, current_path = queue.popleft()
            visited.add(current_position)

            if current_position == target:
                return current_path, current_cost

            # Can move 1 or 2 spaces in each direction (right or left)
            for move in range(1, 3):  
                for direction in [move, -move]:
                    new_position = current_position + direction

                    if new_position not in visited and self.is_valid_move(new_position):
                        new_cost = current_cost + 1

                        # Check if the new position is a snake or ladder
                        for snake in self.snakes:
                            if new_position == snake[1]:
                                new_position = snake[0]
                                break

                        for ladder in self.ladders:
                            if new_position == ladder[0]:
                                new_position = ladder[1]
                                break

                        queue.append((new_position, new_cost, current_path + [new_position]))

        return [], float('inf')  # No valid path found

def main():
    # dimensions = (10, 10)
    dimension_row, dimension_col = input('\nEnter dimension you want for the game board (exaplme: 5 6): ').split()
    dimension_row, dimension_col = int(dimension_row), int(dimension_col)
    dimensions = (dimension_row, dimension_col)


    # snakes = [(3, 37), (10, 25), (16, 47), (32, 75), (71, 94), (42, 96)]
    # ladders = [(4, 56), (12, 50), (14, 55), (22, 58), (41, 79), (54, 88)]

    # Add snakes and ladders
    snakes = []
    ladders = []

    snakes_num = int(input('\nEnter the number of Snakes: '))
    print('For entring each snake, enter it like this: 3 37 ; 3 is the position of the "tail" and 37 is for "head" of the snake.')
    for _ in range(snakes_num):
        snake = input().split(' ')
        snakes.append((int(snake[0]), int(snake[1])))

    ladders_num = int(input('\nEnter the number of Ladders: '))
    print('For entring each ladder, enter it like this: 12 50 ; 12 is the position of the "end" and 50 is for the "top" of the ladder.')
    for _ in range(ladders_num):
        ladder = input().split(' ')
        ladders.append((int(ladder[0]), int(ladder[1])))

    
    # Create an instance of the SnakeLadderGame class
    snake_ladder_game = SnakeLadderGame(dimensions, snakes, ladders)

    # Find the optimal path and cost
    optimal_path, cost = snake_ladder_game.play_game()

    start_position = 1
    target_position = dimension_col * dimension_row

    # Print the result
    if optimal_path:
        print("\nOptimal Path:", optimal_path)
        print("Cost of Optimal Path:", cost)
    else:
        print("\nNo path exists from {} to {}.".format(start_position, target_position))

    input('\nexit: ')

# main()