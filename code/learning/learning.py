__author__ = 'Marcelo d\'Almeida'

import math
import random
import threading

from code.learning import util


class Q_Learning:

    def __init__(self, power):

        self.lock = threading.Lock()

        self._total_power = power

        self.q_power_table = [[random.random() for j in range(10)] for i in range(6)]
        self.q_cost_table = [[random.random() for j in range(10)] for i in range(6)]
        self.q_delay_table = [[random.random() for j in range(10)] for i in range(6)]
        self.q_unified_metric = [0 for i in range(10)]

        self._alpha = 0.01
        self._epsilon = 0.1

        #pow(math.e, -x)

        self._cost_goal = 0
        self._time_goal = 0
        self._goal = None
        self._adaptive_cost = None
        self._adaptive_time = None

        self._power_goal_state = 0
        self._cost_goal_state = 0
        self._delay_goal_state = 0

        self._previous_cost_measurement = None
        self._previous_time_measurement = None
        self._best_cost_measurement = None
        self._best_time_measurement = None

        self._taken_action_task = {}

        self._setup()

    def _setup(self):
        self._decisions_log = [[], []]
        self._available_decisions_log = [[], []]

        self._rewards_log = [[], [], []]
        self._cost_rewards_detailed_info_log = [[], [], [], []]
        self._time_rewards_detailed_info_log = [[], [], [], []]

    def learn(self, raw_state, finished_task_id):

        if finished_task_id not in self._taken_action_task:
            return

        #print(raw_state)
        system_state = self.discretize_state(raw_state[0])
        goal_oriented_state = raw_state[1]

        next_power_state = system_state.power_state
        next_cost_state = system_state.cost_state
        next_delay_state = system_state.delay_state

        self.lock.acquire()
        reward = self.reward(goal_oriented_state)
        self._rewards_log[0].append(reward)
        self._rewards_log[1].append(goal_oriented_state.power_state)
        self._rewards_log[2].append(len(self._taken_action_task))
        for task_id, info in self._taken_action_task.items():
            raw_state, action = info

            state = self.discretize_state(raw_state[0])
            action = util.actions_dict[action]

            power_state = state.power_state
            cost_state = state.cost_state
            delay_state = state.delay_state

            print(util.SEPARATOR)
            print("REWARD", state, util.actions_dict[action], reward, "", sep="\n")

            self.q_power_table[power_state][action] += \
                reward + self._alpha*max(self.q_power_table[next_power_state])

            self.q_cost_table[cost_state][action] += \
                reward + self._alpha*max(self.q_cost_table[next_cost_state])

            self.q_delay_table[delay_state][action] += \
                reward + self._alpha*max(self.q_delay_table[next_delay_state])

        del self._taken_action_task[finished_task_id]
        self.lock.release()


    def decide(self, raw_state, machine_classification_available, task_classification_available):
        #Q(s,a) = recompensa(s) + alpha * max(Q(s')) (Q learning, observe a gula em max)

        system_state = self.discretize_state(raw_state[0])
        goal_oriented_state = raw_state[1]

        current_power_state = system_state.power_state
        current_cost_state = system_state.cost_state
        current_delay_state = system_state.delay_state

        power_progression = goal_oriented_state.power_state

        #available_actions = [util.actions_dict[util.DO_NOTHING]]
        available_actions = []

        print("AVAILABLE MACHINES CLASSIFICATION", machine_classification_available, "", sep='\n')
        print("AVAILABLE TASKS CLASSIFICATION", task_classification_available, "", sep='\n')
        print("AVAILABLE ACTIONS", self.repr(available_actions, util.actions_dict), "", sep='\n')

        for machine_classification in machine_classification_available:
            for task_classification in task_classification_available:
                action = util.actions_dict[task_classification + "+" + machine_classification]
                available_actions.append(action)
                self._available_decisions_log[0].append(action)
                self._available_decisions_log[1].append(power_progression)

        import pdb

        print("CURRENT STATE", self.state_repr(system_state), "", sep='\n')
        print("POWER Q-TABLE", self.table_repr(util.POWER, self.q_power_table), "", sep='\n')
        print("COST Q-TABLE", self.table_repr(util.COST, self.q_cost_table), "", sep='\n')
        print("DELAY Q-TABLE", self.table_repr(util.DELAY, self.q_delay_table), "", sep='\n')

        # explore
        if random.random() <= self._epsilon:
            action = available_actions[random.randrange(len(available_actions))]
        else:
        # exploit
            for action in range(len(self.q_unified_metric)):
                if action in available_actions:
                    self.q_unified_metric[action] = \
                        (self.q_power_table[current_power_state][action] +
                         self.q_cost_table[current_cost_state][action] +
                         self.q_delay_table[current_delay_state][action])/3
                else:
                    self.q_unified_metric[action] = -math.inf

            action, value = self.argmax(self.q_unified_metric)

            print("UNIFIED Q-TABLE", self.table_repr("Unified", [self.q_unified_metric], row_label=False), "", sep='\n')
            print("ACTION INDEX - ACTION - ACTION VALUE", action, util.actions_dict[action], value, "", sep="\n")

        if action == -1:
            return util.actions_dict[0]

        self._decisions_log[0].append(action)
        self._decisions_log[1].append(power_progression)

        next_action = util.actions_dict[action]

        return next_action

    def inform_taken_action_started(self, started_task_id, raw_state, action):
        self.lock.acquire()
        self._taken_action_task[started_task_id] = [raw_state, action]
        self.lock.release()

    def goal(self, cost=None, time=None):

        #if it is equals 0, it means the user wants que quicker/cheaper as possible
        #If is is None, it means the user doesn't care so much for that parameter

        if cost is None and time is None:
            cost = 0
            time = 0

        self._cost_goal = cost
        self._time_goal = time

        if cost is not None:
            if cost == 0:
                # min cumulative_cost/cumulative_power |||| adaptive
                self._adaptive_cost = True
                pass
            else:
                # cumulative_cost/cumulative_power ==~ total_cost/total_power
                self._adaptive_cost = False
                pass

        if time is not None:
            if time == 0:
                # min cumulative_time/cumulative_power |||| adaptive
                self._adaptive_time = True
                pass
            else:
                # cumulative_time/cumulative_power ==~ total_time/total_power
                self._adaptive_time = False
                pass


    def reward(self, goal_oriented_state):

        power_progression = goal_oriented_state.power_state
        cost_progression = goal_oriented_state.cost_state
        time_progression = goal_oriented_state.time_state

        if power_progression != 0:
            if self._adaptive_cost is not None:

                cost_measurement = cost_progression/power_progression

                if self._best_cost_measurement is None:
                    self._best_cost_measurement = cost_measurement
                if self._previous_cost_measurement is None:
                    self._previous_cost_measurement = cost_measurement

                if self._adaptive_cost:
                    # min cumulative_cost/cumulative_power |||| adaptive

                    cost_reward_measurement = self._previous_cost_measurement - cost_measurement
                    self._previous_cost_measurement = cost_measurement

                    cost_reward_measurement += 1

                    if self._best_cost_measurement > cost_measurement:
                        self._best_cost_measurement = cost_measurement
                        cost_reward_measurement += pow(cost_reward_measurement, 2)

                    cost_goal_reward = cost_reward_measurement
                else:
                    # cumulative_cost/cumulative_power ==~ total_cost/total_power
                    cost_goal = self._cost_goal/self._total_power

                    cost_measurement = math.sqrt(pow(cost_goal - cost_measurement, 2))
                    cost_reward_measurement = self._previous_cost_measurement - cost_measurement
                    self._previous_cost_measurement = cost_measurement

                    cost_reward_measurement += 1

                    if self._best_cost_measurement > cost_measurement:
                        self._best_cost_measurement = cost_measurement

                    cost_goal_reward = cost_reward_measurement

                self._cost_rewards_detailed_info_log[0].append(self._best_cost_measurement)
                self._cost_rewards_detailed_info_log[1].append(cost_measurement)
                self._cost_rewards_detailed_info_log[2].append(power_progression)
                self._cost_rewards_detailed_info_log[3].append(cost_goal_reward)

            else:
                cost_goal_reward = 1

            if self._adaptive_time is not None:

                time_measurement = time_progression/power_progression
                if self._best_time_measurement is None:
                    self._best_time_measurement = time_measurement
                if self._previous_time_measurement is None:
                    self._previous_time_measurement = time_measurement

                if self._adaptive_time:
                    # min cumulative_time/cumulative_power |||| adaptive

                    time_reward_measurement = self._previous_time_measurement - time_measurement
                    self._previous_time_measurement = time_measurement

                    time_reward_measurement += 1

                    if self._best_time_measurement > time_measurement:
                        self._best_time_measurement = time_measurement
                        time_reward_measurement += pow(time_reward_measurement, 2)

                    time_goal_reward = time_reward_measurement
                else:
                    # cumulative_time/cumulative_power ==~ total_time/total_power
                    time_goal = self._time_goal/self._total_power

                    time_measurement = math.sqrt(pow(time_goal - time_measurement, 2))
                    time_reward_measurement = self._previous_time_measurement - time_measurement
                    self._previous_time_measurement = time_measurement

                    time_reward_measurement += 1

                    if self._best_time_measurement > time_measurement:
                        self._best_time_measurement = time_measurement

                    time_goal_reward = time_reward_measurement

                self._time_rewards_detailed_info_log[0].append(self._best_time_measurement)
                self._time_rewards_detailed_info_log[1].append(time_measurement)
                self._time_rewards_detailed_info_log[2].append(power_progression)
                self._time_rewards_detailed_info_log[3].append(time_goal_reward)

            else:
                time_goal_reward = 1

            # Review
            reward = cost_goal_reward + time_goal_reward

        else:
            reward = 0

        return reward

    def report_decision(self):
        return self._decisions_log, self._available_decisions_log

    def report_reward(self):
        return self._rewards_log, [self._cost_rewards_detailed_info_log, self._time_rewards_detailed_info_log]

    def report_q_tables(self):
        return self.q_power_table, self.q_cost_table, self.q_delay_table

    def log_reset(self):
        self._setup()

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

    def state_repr(self, state):

        result = str(util.power_state_dict[state.power_state]) + " - " + \
                 str(util.cost_state_dict[state.cost_state]) + " - " + \
                 str(util.delay_state_dict[state.delay_state]) + " - " +\
                 "Time " + str(state.time_state)

        return result

    def table_repr(self, title, table, row_label=True):
        matrix = []
        row = []
        row.append(title)
        for j in range(len(table[0])):
            row.append(util.actions_dict[j])
        matrix.append(row)
        for i in range(len(table)):
            row = []
            if row_label:
                row.append(util.percentage_dict[i])
            else:
                row.append("")
            for j in range(len(table[0])):
                row.append(round(table[i][j], 3))
            matrix.append(row)

        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        result = '\n'.join(table)

        return result

        #http://stackoverflow.com/questions/13214809/pretty-print-2d-python-list

    def repr(self, values, dict):

        result = []
        for value in values:
            result.append(dict[value])

        return result
