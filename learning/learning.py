__author__ = 'Marcelo d\'Almeida'

from learning import util
import random
import math

class Q_Learning:

    def __init__(self):
        self.q_power_table = [[random.randint(0, 10) for j in range(10)] for i in range(6)]
        self.q_cost_table = [[random.randint(0, 10) for j in range(10)] for i in range(6)]
        self.q_delay_table = [[random.randint(0, 10) for j in range(10)] for i in range(6)]
        self.q_unified_metric = [0 for i in range(10)]

        self._current_state = util.StateInfo(
            util.power_state_dict[util.POWER_0_to_10_PERCENT],
            util.cost_state_dict[util.COST_0_to_10_PERCENT],
            util.delay_state_dict[util.DELAY_0_to_10_PERCENT],
            0)

        self._next_state = util.StateInfo(
            util.power_state_dict[util.POWER_0_to_10_PERCENT],
            util.cost_state_dict[util.COST_0_to_10_PERCENT],
            util.delay_state_dict[util.DELAY_0_to_10_PERCENT],
            0)

        self._raw_current_state = util.StateInfo(0, 0, 0, 0)

        self._raw_next_state = util.StateInfo(0, 0, 0, 0)

        self._current_action = -1

        self._alpha = 0.01

        self._total_power = 0
        self._total_cost = 0
        self._total_delay = 0
        self._total_time = 0

        self._power_goal = None
        self._cost_goal = None
        self._delay_goal = None

        self._power_goal_state = 0
        self._cost_goal_state = 0
        self._delay_goal_state = 0

        print([[self.q_power_table[i][j] for j in range(10)] for i in range(6)])

    def next_action(self, current_state, machine_classification_available, task_classification_available):
        self._learn(current_state)
        next_action = self._decide(machine_classification_available.keys(), task_classification_available.keys())
        return next_action

    def _learn(self, raw_state):

        current_action = self._current_action
        if current_action == -1:
            return

        state = self.discretize_state(raw_state)

        #print(raw_state)
        self._raw_next_state = raw_state
        self._next_state = state

        current_power_state = self._current_state.power_state
        current_cost_state = self._current_state.cost_state
        current_delay_state = self._current_state.delay_state

        next_power_state = self._next_state.power_state
        next_cost_state = self._next_state.cost_state
        next_delay_state = self._next_state.delay_state

        reward = self.reward(self._raw_current_state)

        self.q_power_table[current_power_state][current_action] += \
            reward[0] + \
            self._alpha*max(self.q_power_table[next_power_state])

        self.q_cost_table[current_cost_state][current_action] += \
            reward[1] + \
            self._alpha*max(self.q_cost_table[next_cost_state])

        self.q_delay_table[current_delay_state][current_action] += \
            reward[2] + \
            self._alpha*max(self.q_delay_table[next_delay_state])

    def _decide(self, machine_classification_available, task_classification_available):
        #Q(s,a) = recompensa(s) + alpha * max(Q(s')) (Q learning, observe a gula em max)

        current_power_state = self._current_state.power_state
        current_cost_state = self._current_state.cost_state
        current_delay_state = self._current_state.delay_state

        #available_actions = [util.actions_dict[util.DO_NOTHING]]
        available_actions = []

        for machine_classification in machine_classification_available:
            for task_classification in task_classification_available:
                available_actions.append(util.actions_dict[task_classification + "+" + machine_classification])

        print(machine_classification_available)
        print(task_classification_available)
        print(available_actions)

        self.print_state()
        self.print_table(util.POWER, self.q_power_table)
        self.print_table(util.COST, self.q_cost_table)
        self.print_table(util.DELAY, self.q_delay_table)

        for action in range(len(self.q_unified_metric)):
            if action in available_actions:
                self.q_unified_metric[action] = \
                    (self.q_power_table[current_power_state][action] +
                     self.q_cost_table[current_cost_state][action] +
                     self.q_delay_table[current_delay_state][action])/3
            else:
                self.q_unified_metric[action] = -math.inf

        action, value = self.argmax(self.q_unified_metric)
        print(self.q_unified_metric)
        print(action, util.actions_dict[action], value)

        self._current_action = action
        if action == -1:
            return util.actions_dict[0]

        next_action = util.actions_dict[action]

        self._current_state = self._next_state
        self._raw_current_state = self._raw_next_state

        return next_action

    def goal(self, power_goal, cost_goal, delay_goal):
        self._power_goal = power_goal
        self._cost_goal = cost_goal
        self._delay_goal = delay_goal

    def reward(self, state):

        current_raw_time_state = self._raw_current_state.time_state
        next_raw_time_state = self._raw_next_state.time_state

        elapsed_time = next_raw_time_state - current_raw_time_state

        if elapsed_time != 0:
            self._total_power += state.power_state
            self._total_cost += state.cost_state
            self._total_delay += state.delay_state
            self._total_time += elapsed_time

            #print("Elapsed time", elapsed_time)

            self._power_goal_state = self._total_power/self._total_time
            self._cost_goal_state = self._total_cost/self._total_time
            self._delay_goal_state = self._total_delay/self._total_time

            #print(self._power_goal_state)
            #print(self._cost_goal_state)
            #print(self._delay_goal_state)


        power_reward = 2 - pow(self._power_goal - self._power_goal_state, 2)
        cost_reward = 2 - pow(self._cost_goal - self._cost_goal_state, 2)
        delay_reward = 2 - pow(self._delay_goal - self._delay_goal_state, 2)
        return power_reward, cost_reward, delay_reward

    def discretize_state(self, state_metrics):
        power_state_metric = state_metrics.power_state
        cost_state_metric = state_metrics.cost_state
        delay_state_metric = state_metrics.delay_state

        power_state = self.discretize(power_state_metric)
        cost_state = self.discretize(cost_state_metric)
        delay_state = self.discretize(delay_state_metric)

        return util.StateInfo(power_state, cost_state, delay_state, state_metrics.time_state)

    def discretize(self, value):
        if value >= 0 and value <= 0.1:
            return util.percentage_dict[util.PERCENTAGE_0_to_10]
        else:
            if value <= 0.3:
                return util.percentage_dict[util.PERCENTAGE_10_to_30]
            else:
                if value <= 0.5:
                    return util.percentage_dict[util.PERCENTAGE_30_to_50]
                else:
                    if value <= 0.7:
                        return util.percentage_dict[util.PERCENTAGE_50_to_70]
                    else:
                        if value <= 0.9:
                            return util.percentage_dict[util.PERCENTAGE_70_to_90]
                        else:
                            if value <= 1:
                                return util.percentage_dict[util.PERCENTAGE_90_to_100]



    def argmax(self, iterable):
        arg_max = -1
        max_value = -math.inf
        for index, value in enumerate(iterable):
            if max_value < value:
                max_value = value
                arg_max = index
        return arg_max, max_value

    def print_state(self, state=None):
        if not state:
            state = self._current_state

        print(util.power_state_dict[state.power_state])
        print(util.cost_state_dict[state.cost_state])
        print(util.delay_state_dict[state.delay_state])
        print(state.time_state)

    def print_table(self, title, table):
        matrix = []
        row = []
        row.append(title)
        for j in range(len(table[0])):
            row.append(util.actions_dict[j])
        matrix.append(row)
        for i in range(len(table)):
            row = []
            row.append(util.percentage_dict[i])
            for j in range(len(table[0])):
                row.append(round(table[i][j], 3))
            matrix.append(row)

        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))