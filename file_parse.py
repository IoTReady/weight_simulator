from time import sleep

FNAME = "weights.txt"

previous_weight = 0
new_weight = 0
stable_count = 0
SCALE_RESOLUTION = 5
STABLE_COUNT_TARGET = 2

with open(FNAME, 'r') as f:
    weights = [int(line.strip()) for line in f.readlines()]

# print(weights)

for i in range(len(weights)):
    new_weight = weights[i]
    if new_weight < 0:
        previous_weight = 0
        continue
    if abs(new_weight - previous_weight) <= SCALE_RESOLUTION:
        stable_count += 1
    else:
        stable_count = 0
    # print(f"Previous weight: {previous_weight}, New weight: {new_weight}")
    previous_weight = new_weight
    if stable_count < STABLE_COUNT_TARGET:
        sleep(0.5)
        continue
    print(f"\nStable weight: {new_weight}, Stable count: {stable_count}\n")
    stable_count = 0
    sleep(0.5)