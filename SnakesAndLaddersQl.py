# Sepehr Moniri
# 981813205

import numpy as np
import random

class SnakesAndLaddersQl:
    def __init__(self, dimensions, snakes, ladders, p, num_episodes):
        self.dimensions = dimensions
        self.snakes = snakes
        self.ladders = ladders
        self.p = p
        self.num_episodes = num_episodes
        self.q_table = self.initialize_q_table()

    def edge_houses(self):
        # dimension = self.dimensions[0]
        # rows = [[int(f'{(j+1) + (i*dimension):4}') for j in range(dimension)] for i in range(dimension)]

        board_row, board_col = self.dimensions
        rows = [[int(f'{(j+1) + (i*board_col):4}') for j in range(board_col)] for i in range(board_row)]
        rows = rows[::-1]
        board = []
        if len(rows) % 2:
            for row in range(len(rows)):
                if row % 2 == 0:
                    board.append(rows[row])
                else:
                    board.append(rows[row][::-1])
        else:
            for row in range(len(rows)):
                if row % 2 == 0:
                    board.append(rows[row][::-1])
                else:
                    board.append(rows[row])

        first_column = []
        last_column = []

        for i in board:
            first_column.append(i[0])
            last_column.append(i[len(i)-1])

        return first_column, last_column

    def initialize_q_table(self):
        num_states = self.dimensions[0] * self.dimensions[1]
        num_actions = 5
        return np.zeros((num_states, num_actions))

    def choose_action(self, state, epsilon):
        first_column, last_column = self.edge_houses()
        available_actions = [1, 2, -1, -2]

        if state in first_column:
            state_first_index = first_column.index(state)
            if (state_first_index + 1) < len(last_column):
                available_actions.append(3)

        elif state in last_column:
            state_last_index = last_column.index(state)
            if (state_last_index + 1) < len(last_column):
                available_actions.append(3)

        if np.random.rand() < epsilon:
            return random.choice(available_actions), available_actions
        else:
            return available_actions[np.argmax(self.q_table[state, :len(available_actions)])], available_actions

    def update_q_value(self, state, action, reward, next_state, available_actions):
        action = available_actions.index(action)
        self.q_table[state][action] = (1 - self.alpha) * self.q_table[state, action] + \
                                      self.alpha * (reward + self.gamma * np.max(self.q_table[next_state]))

    def play_game(self):
        num_rows, num_columns = self.dimensions
        num_states = num_rows * num_columns
        first_column, last_column = self.edge_houses()

        epsilon = 0.5
        self.alpha = 0.5
        self.gamma = 0.9

        state = 0
        path = []
        total_reward = 0

        while state != num_states - 1:
            next_state = state
            action, available_actions = self.choose_action(state, epsilon)

            # Simulate the uncertain environment
            action_flag = 0
            if np.random.rand() < self.p:
                if (state in first_column) and (action == 3):
                    state_index = first_column.index(state)
                    if state_index + 1 < len(first_column):
                        next_state = first_column[state_index + 1]
                    action_flag = 1
                    action = 1

                elif (state in last_column) and (action == 3):
                    state_index = last_column.index(state)
                    if state_index + 1 < len(last_column):
                        next_state = last_column[state_index + 1]
                    action_flag = 1
                    action = 1

                else:
                    next_state = state + action

            else:  # np.random.rand() > p
                if (state in first_column) and (action == 3):
                    state_index = first_column.index(state)
                    if state_index - 1 >= 0:
                        next_state = first_column[state_index - 1]
                    action_flag = -1
                    action = -1

                elif (state in last_column) and (action == 3):
                    state_index = last_column.index(state)
                    if state_index - 1 >= 0:
                        next_state = last_column[state_index - 1]
                    action_flag = -1
                    action = -1

                else:
                    action *= -1
                    next_state = state + action

            reward = -1

            # Check if the next state is a snake or ladder
            for snake_tail, snake_head in self.snakes:
                if next_state == snake_head:
                    next_state = snake_tail
                    break

            for ladder_bottom, ladder_top in self.ladders:
                if next_state == ladder_bottom:
                    next_state = ladder_top
                    break

            # Ensure the next state stays within the game bounds
            next_state = max(0, min(next_state, num_states - 1))

            # Update Q-value and move to the next state
            if action_flag != 0:
                up_action = 3
                self.update_q_value(state, up_action, reward, next_state, available_actions)
                path.append((state, up_action * action_flag, next_state))

            else:
                self.update_q_value(state, action, reward, next_state, available_actions)
                path.append((state, action, next_state))

            state = next_state

            if state == num_states - 1:
                reward = 1000
                total_reward += reward
                break

            total_reward += reward

        return path, total_reward

    def q_learning(self):
        for episode in range(self.num_episodes):
            path, total_reward = self.play_game()
            print(f'Episode {episode + 1}: Total Reward = {total_reward}')

        return self.q_table, path
    

 
def main():

    # dimensions = (10, 10)
    dimension_row, dimension_col = input('\nEnter dimension you want for the game board (exaplme: 5 6): ').split()
    dimensions = (int(dimension_row), int(dimension_col))

    # snakes = [(3, 37), (10, 25), (16, 47), (32, 75), (71, 94), (42, 96)]
    # ladders = [(4, 56), (12, 50), (14, 55), (22, 58), (41, 79), (54, 88)]

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

    print('\n')
    
    p = 0.7
    num_episodes = 300

    game = SnakesAndLaddersQl(dimensions, snakes, ladders, p, num_episodes)
    q_table, path = game.q_learning()
    print(f'\nThe path of the last episode is: \n{path}')
    print(f'\nThe Q-Values are: \n{q_table}')

    input('exit: ')

# main()