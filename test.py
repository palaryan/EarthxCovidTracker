import sys
import random
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
def create_sample_data(num_weeks):
    # only for demonstration purposes
    data_set = np.zeros(84 * num_weeks)
    index = 0
    for i in range(num_weeks):
        base = 30
        for j in range(7):
            if j == 4:
                base = random.randint(40, 44)
            elif j == 5:
                base = random.randint(48, 52)  # peaks friday/saturday/sunday
            elif j == 6:
                base = random.randint(37, 39)
            else:
                base = random.randint(28, 32)
            for k in range(12):
                data_set[index] = base + random.randint(-3, 3)
                if k < 6:
                    base += 2
                else:
                    base -= 2
                index += 1
    return data_set
print(create_sample_data(12))
