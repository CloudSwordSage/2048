# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:54:23 2020
@author: chenfeng
@description: 2048游戏的住游戏实现.
"""

import os
from copy import deepcopy
from typing import List, Tuple

import numpy as np

# np.random.seed(0)  # 随机种子

init_board = [[0] * 4 for _ in range(4)]


def is_win(grid: List[List[int]]) -> bool:
    """
    判断给定的二维整数网格中是否存在数字 2048，若存在则返回 True，否则返回 False。

    Args:
        grid (List[List[int]]): 二维整数网格，每个元素代表网格中的一个数字。

    Returns:
        bool: 若网格中存在数字 2048，则返回 True；否则返回 False。
    """
    win = False
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 2048:
                win = True
    return win


def is_lose(grid: List[List[int]]) -> bool:
    """
    判断当前游戏局面是否失败。

    Args:
        grid (List[List[int]]): 游戏局面，二维列表，每个元素表示对应位置上的数字。

    Returns:
        bool: 如果当前局面失败则返回True，否则返回False。

    """
    full = all(np.array(grid).flatten() != 0)
    if not full:
        return False

    for i in range(4):
        for j in range(4):
            if i - 1 >= 0 and grid[i][j] == grid[i - 1][j]:
                return False
            if i + 1 < 4 and grid[i][j] == grid[i + 1][j]:
                return False
            if j - 1 >= 0 and grid[i][j] == grid[i][j - 1]:
                return False
            if j + 1 < 4 and grid[i][j] == grid[i][j + 1]:
                return False
    return True


def print_board(grid: List[List[int]]) -> None:
    """
    打印给定的二维整数网格。

    Args:
        grid (List[List[int]]): 二维整数网格，每个元素代表网格中的一个数字。
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n', '—' * (11 * 4 + 5))
    for i in grid:
        print(' ', end="")
        i = [str(t) if t != 0 else '' for t in i]
        for j in i:
            print(f"|{j:^11}", end="")
        print('|\n', '—' * (11 * 4 + 5))


class Game:
    """
    2048游戏类，用于初始化游戏局面和移动操作。
    """

    def __init__(self):
        self.grid = deepcopy(init_board)
        coord1 = None
        coord2 = None

        while True:
            coord1 = (np.random.randint(0, 4), np.random.randint(0, 3))
            coord2 = (np.random.randint(0, 4), np.random.randint(0, 3))

            if coord1 != coord2:
                break
        self.grid[coord1[0]][coord1[1]] = np.random.choice([2, 4])
        self.grid[coord2[0]][coord2[1]] = np.random.choice([2, 4])

    def move(self, direction: int) -> Tuple[List[List[int]], bool, bool, int]:
        """
        执行一次移动操作。

        Args:
            direction (int): 移动方向，取值为0、1、2、3分别代表上、下、左、右四个方向。
        
        Returns:
            int: 移动后得分。
        """
        score = 0

        if direction == 0:
            score = self.move_up()
        elif direction == 1:
            score = self.move_down()
        elif direction == 2:
            score = self.move_left()
        elif direction == 3:
            score = self.move_right()

        lose = all(np.array(self.grid).flatten() != 0)

        if not lose:
            coord = None
            while True:
                coord = (np.random.randint(0, 4), np.random.randint(0, 4))
                if self.grid[coord[0]][coord[1]] == 0:
                    break
            self.grid[coord[0]][coord[1]] = np.random.choice([2, 2, 2, 2, 2, 2, 4])

        return self.get_grid, is_win(self.grid), is_lose(self.grid), score

    def move_up(self) -> int:
        """
        将grid中的非零元素上移并合并相同的元素。
        
        Args:
            grid (List[List[int]]): 4x4的整数矩阵，代表一个游戏的当前状态。
                                   元素值在[0, 2048]范围内，0表示空格。
        
        Returns:
            int: 合并元素后增加的分数。
        
        """
        score = 0
        for j in range(4):
            for i in range(3, 0, -1):
                if self.grid[i][j] != 0 and self.grid[i - 1][j] == 0:
                    self.grid[i][j], self.grid[i - 1][j] = self.grid[i - 1][j], self.grid[i][j]
                if self.grid[i][j] == self.grid[i - 1][j]:
                    self.grid[i][j], self.grid[i - 1][j] = self.grid[i][j] * 2, 0
                    score += self.grid[i][j] * 2
        for j in range(4):
            for i in range(3, 0, -1):
                if self.grid[i][j] != 0 and self.grid[i - 1][j] == 0:
                    self.grid[i][j], self.grid[i - 1][j] = self.grid[i - 1][j], self.grid[i][j]
        return score

    def move_down(self) -> int:
        """
        向下移动方块，并返回得分。
        
        Args:
            self.grid (List[List[int]]): 一个 4x4 的整数二维列表，表示方块的状态。
                                   0 表示该位置为空，其他值表示该位置的方块数值。
        
        Returns:
            int: 移动方块后获得的得分。
        
        """
        score = 0
        for j in range(4):
            for i in range(3):
                if self.grid[i][j] != 0 and self.grid[i + 1][j] == 0:
                    self.grid[i][j], self.grid[i +
                        1][j] = self.grid[i + 1][j], self.grid[i][j]
                if self.grid[i][j] == self.grid[i + 1][j]:
                    self.grid[i][j], self.grid[i + 1][j] = self.grid[i][j] * 2, 0
                    score += self.grid[i][j] * 2
        for j in range(4):
            for i in range(3):
                if self.grid[i][j] != 0 and self.grid[i + 1][j] == 0:
                    self.grid[i][j], self.grid[i + 1][j] = self.grid[i + 1][j], self.grid[i][j]
        return score

    def move_left(self) -> int:
        """
        向左移动方块，并计算得分。
        
        Args:
            self.grid (List[List[int]]): 4x4的二维列表，表示游戏网格，其中0表示空格，非0表示方块。
        
        Returns:
            int: 得分，即移动方块后合并方块得到的分数。
        
        """
        score = 0
        for i in range(4):
            for j in range(3, 0, -1):
                if self.grid[i][j] != 0 and self.grid[i][j - 1] == 0:
                    self.grid[i][j], self.grid[i][j -
                        1] = self.grid[i][j - 1], self.grid[i][j]
                if self.grid[i][j] == self.grid[i][j - 1]:
                    self.grid[i][j], self.grid[i][j - 1] = self.grid[i][j] * 2, 0
                    score += self.grid[i][j] * 2
        for i in range(4):
            for j in range(3, 0, -1):
                if self.grid[i][j] != 0 and self.grid[i][j - 1] == 0:
                    self.grid[i][j], self.grid[i][j - 1] = self.grid[1][j - 1], self.grid[i][j]
        return score

    def move_right(self) -> int:
        """
        向右滑动数字块并合并相同数字块，返回得分。
        
        Args:
            self.grid (List[List[int]]): 4x4的二维列表，表示数字块的位置，0表示空位。
        
        Returns:
            int: 合并数字块后得到的得分。
        
        """
        score = 0
        for i in range(4):
            for j in range(3):
                if self.grid[i][j] != 0 and self.grid[i][j + 1] == 0:
                    self.grid[i][j], self.grid[i][j +
                        1] = self.grid[i][j + 1], self.grid[i][j]
                if self.grid[i][j] == self.grid[i][j + 1]:
                    self.grid[i][j], self.grid[i][j + 1] = self.grid[i][j] * 2, 0
                    score += self.grid[i][j] * 2
        for i in range(4):
            for j in range(3):
                if self.grid[i][j] != 0 and self.grid[i][j + 1] == 0:
                    self.grid[i][j], self.grid[i][j + 1] = self.grid[1][j + 1], self.grid[i][j]
        return score

    @property
    def get_grid(self) -> List[List[int]]:
        """  
        获取当前游戏局面。  
        """
        return self.grid


if __name__ == "__main__":
    game = Game()
    running = True
    while running:
        print_board(game.get_grid)
        for i in range(4):
            next_grid, winner, lose, reward = game.move(i)
            if winner:
                print("Game Over!")
                running = False
                break
            if lose:
                print("Game Lose!")
                print(winner or lose)
                running = False
                break
