import random
import operator

class DiscreteDistribution:
    def __init__(self, distr_dict):
        self._distribution = distr_dict
        self._distribution = {i: distr_dict[i] for i in distr_dict.keys()}

    def __add__(self, other):
        return self._add_distribution(other, operator.add)

    def __radd__(self, other):
        #great hidden python feature: sum() tries to add 0 to the iterable,
        #so you always need to be able to handle zero even if you don't handle integer addition
        if other is 0:
            return self
        return self.__add__(other)

    def __mul__(self, other):
        return self._add_distribution(other, operator.mul)

    def _add_distribution(self, other_distr, operation):
        distr_dict = {}
        for my_key in self._distribution:
            for other_key in other_distr._distribution:
                try:
                    distr_dict[operation(my_key, other_key)] += self[my_key]*other_distr[other_key]
                except KeyError:
                    distr_dict[operation(my_key, other_key)] = self[my_key]*other_distr[other_key]
        return DiscreteDistribution(distr_dict)

    def __getitem__(self, key):
        return self._distribution[key]

    def values(self):
        return tuple(self._distribution.keys())

    def chances(self):
        return tuple(self._distribution.values())

    def sample(self):
        total = sum(self._distribution.values())
        choice = random.randint(1, total)

        running = 0
        for i in sorted(self._distribution.keys()):
            running += self._distribution[i]
            if running>=choice:
                return i

    def get_cumulative(self):
        sorted_keys = sorted(self._distribution.keys())
        cumulative = {sorted_keys[i]:sum(   self[j]
                                        for j in sorted_keys[:i+1])
                                        for i in range(len(sorted_keys))}
        return DiscreteDistribution(cumulative)

class DiceDistribution(DiscreteDistribution):
    def __init__(self, n):
        super(DiceDistribution, self).__init__({i+1:1 for i in range(n)})
