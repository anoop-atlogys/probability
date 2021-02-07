from enum import Enum

from collections import Counter
from itertools import combinations


Color = Enum('Color', [('red', 'r'), ('green', 'g'), ('blue', 'b')])


class Ball:

    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __repr__(self):
        return f'{self.color.value}{self.number}'

    @classmethod
    def generate_balls(cls, red_count, green_count, blue_count):
        balls = list()
        for color, count in zip(list(Color), [red_count, green_count, blue_count]):
            for number in range(1, count+1):
                balls.append(
                    cls(color, number)
                )

        return balls


class CombinationNode:

    def __init__(self, balls, selection):
        self.balls = balls

        self._selection = selection

    def __repr__(self):
        return f'{self.identity} {self._selection}'

    @property
    def identity(self):
        c = Counter([ball.color.value for ball in self.balls])

        return tuple(
            sorted(
                list(c.values())
            )
        )

    def is_success_case(self):
        ball1, ball2 = self._selection
        return ball1.color.value == ball2.color.value

    @classmethod
    def next_choices(cls, balls):
        nodes = list()
        for selection in list(combinations(balls, 2)):
            nodes.append(
                cls(
                    tuple(set(balls)-set(selection)),
                    selection,
                )
            )
        return nodes


def calculator(nodes, level=1):

    if level == 3:
        success_cases = 0
        for node in nodes:
            if node.is_success_case():
                success_cases += 1
        return success_cases, len(nodes)

    node_counter = Counter([node.identity for node in nodes])

    l_nodes = list()
    for key, value in node_counter.items():
        for node in nodes:
            if node.identity == key:
                node.replica = value
                l_nodes.append(node)
                break

    #print([(node, node.replica) for node in l_nodes])
    success_cases = 0
    total_cases = 0
    for node in l_nodes:
        x_success, x_total = calculator(
            CombinationNode.next_choices(node.balls),
            level+1,
        )
        success_cases += node.replica * x_success
        total_cases += node.replica * x_total

    return success_cases, total_cases


if __name__ == '__main__':
    print('Enter red balls count: ', end='')
    red_count = int(input())

    print('Enter green balls count: ', end='')
    green_count = int(input())

    print('Enter blue balls count: ', end='')
    blue_count = int(input())

    print(f'Total number of balls: {red_count+green_count+blue_count}')

    assert red_count + green_count + blue_count > 5, "Number of balls are less than 6"

    balls = Ball.generate_balls(red_count, green_count, blue_count)
    #print(balls)

    nodes = CombinationNode.next_choices(balls)

    #print(nodes)
    success_cases, total_cases = calculator(nodes)
    print(f"Probability: {success_cases/total_cases}")
