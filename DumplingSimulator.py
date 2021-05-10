import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class DumplingSimulator:
    def __init__(self, num_dumplings, num_coins, num_people):
        self.num_dumplings = num_dumplings
        self.num_coins = num_coins
        self.num_people = num_people
    
    def _create_initialized_array(self):
        arr = ([1 for _ in range(self.num_coins)] +
             [0 for _ in range(self.num_dumplings - self.num_coins)])
        np.random.shuffle(arr)
        return arr
    
    def run_single(self):
        arr = self._create_initialized_array()
        people_dumplings = {n: [] for n in range(self.num_people)}
        for n, dumpling in enumerate(arr):
            person = n % self.num_people
            people_dumplings[person].append(dumpling)
        
        return people_dumplings

    def run_single_alt(self):
        arr = self._create_initialized_array()
        people_dumplings = {n: [] for n in range(self.num_people)}
        num_dumps_each = self.num_dumplings // self.num_people
        for n in range(self.num_people):
            start_idx = (n) * num_dumps_each
            end_idx = (n + 1) *(num_dumps_each)
            people_dumplings[n] = arr[start_idx: end_idx]
        
        return people_dumplings

if __name__ == '__main__':
    num_dumplings = 36
    num_coins = 5
    num_people = 4
    simulator = DumplingSimulator(num_dumplings, num_coins, num_people)
    runs = []
    outcomes = []
    num_runs = 1000000

    for _ in range(num_runs):
        run = simulator.run_single()
        #run = simulator.run_single_alt()
        outcome = tuple(sorted([sum(value) for _, value in run.items()]))
        runs.append(run)
        outcomes.append(outcome)
    
    reformat_runs = {n: [run[n] for run in runs] for n in range(num_people)}
    person_sums = {n: [sum(run) for run in runs] for n, runs in reformat_runs.items()}

    print("Mean coins per person: \n", {n: np.mean(runs) for n, runs in person_sums.items()})

    plt.hist([person_sum for _, person_sum in person_sums.items()], density=False, histtype='bar')
    plt.xlabel('Number of Coins')
    plt.ylabel('Number of Occurances')
    plt.title(f'''{num_runs} simulations of 
                {num_people} people picking 
                {num_coins} coins from 
                {num_dumplings} dumplings''')
    plt.legend([f'Person {n}' for n in range(num_people)])
    
    plt.savefig('Distributions.png', bbox_inches='tight')

    outcome_counter = Counter(outcomes)
    percent_outcomes = [(val[0], round(val[1] * 100 / num_runs, 1)) for val in outcome_counter.most_common()]
    print('Outcome Percentage Occurance')
    print(*percent_outcomes, sep='\n')
    
    
