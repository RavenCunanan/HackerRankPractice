from heapq import heappop, heappush
from collections import defaultdict

def minimum_energy_to_exit(door_information, keycard_information, energy_activation_cost, override_activation_cost, override_activation_discount):
    # Parse door info
    doors = {}  # door -> required keycards
    for entry in door_information:
        parts = entry.split(':')
        if len(parts) < 1:
            continue
        door = parts[0].strip()
        keycards = set(parts[1].strip().split()) if len(parts) > 1 and parts[1].strip() else set()
        doors[door] = keycards

    # Parse keycard info
    keycard_to_door = defaultdict(list)
    for entry in keycard_information:
        parts = entry.split(':')
        if len(parts) < 2:
            continue
        keycard = parts[0].strip()
        door = parts[1].strip()
        keycard_to_door[keycard].append(door)

    # Priority queue (Dijkstra's Algorithm) (cost, door, collected keycards)
    pq = [(0, 'D1', set())]  # Start at door 'D1' with zero cost and no keycards
    visited = set()

    while pq:
        cost, door, collected = heappop(pq)

        # Debug: Print current state
        print(f"Processing: cost={cost}, door={door}, collected={collected}")

        # Reach last door, return the cost
        if door == 'D3':  # Compare with the last door
            return cost

        # Avoid revisiting the same state
        state = (door, frozenset(collected))
        if state in visited:
            continue
        visited.add(state)

        # Collect keycards behind the current door
        if door in doors:
            new_collected = collected | doors[door]
        else:
            new_collected = collected  # If door has no keycards, keep collected as is

        # Debug: Print new_collected
        print(f"New collected keycards: {new_collected}")

        # Unlock and queue up new doors
        for keycard in new_collected:
            for next_door in keycard_to_door[keycard]:
                if next_door not in doors:
                    continue  # Skip invalid doors
                required_keys = doors[next_door]
                if required_keys.issubset(new_collected):
                    # Calculate unlock cost
                    keycard_count = len(required_keys)
                    unlock_cost = energy_activation_cost + keycard_count

                    # If override is cheaper, use it
                    override_cost = override_activation_cost - override_activation_discount
                    if override_cost < unlock_cost:
                        unlock_cost = override_cost

                    # Debug: Print next door and cost
                    print(f"Unlocking {next_door} with cost {unlock_cost}")

                    heappush(pq, (cost + unlock_cost, next_door, new_collected))

    return -1  # If we never reach the last door
