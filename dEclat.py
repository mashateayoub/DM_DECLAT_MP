import csv
import time
import tracemalloc

import sys
sys.setrecursionlimit(600000)


def declat(diffsets, min_support):
    start_timestamp = time.time()
    tracemalloc.start()
    # Create a dictionary to store the item sets and their support values
    item_sets = {}
    # Loop through all the diffsets
    for diffset in diffsets:
        # Loop through all the items in the diffset
        for item in diffset:
            # If the item is not in the item_sets dictionary, add it
            if item not in item_sets:
                item_sets[item] = 1
            # Otherwise, increment the support value for the item
            else:
                item_sets[item] += 1

    # Filter the item sets to remove those with support less than the minimum support
    item_sets = {item: support for item,
                 support in item_sets.items() if support >= min_support}

    # Sort the item sets by support in descending order
    item_sets = {k: v for k, v in sorted(
        item_sets.items(), key=lambda item: item[1], reverse=True)}

    # Initialize the frequent item sets list
    frequent_item_sets = []

    # Generate the frequent item sets using a loop
    generate_frequent_item_sets(
        item_sets, frequent_item_sets, set(), diffsets, min_support)

    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_timestamp = time.time()
    # Return the list of frequent item sets
    return frequent_item_sets, peak_memory / 1024, end_timestamp-start_timestamp


def generate_frequent_item_sets(item_sets, frequent_item_sets, current_item_set, diffsets, min_support):
    # Add the current item set to the frequent item sets list
    frequent_item_sets.append(current_item_set)

    # Initialize a list to store the new item sets
    new_item_sets = []

    # Loop through the item sets
    for item, support in item_sets.items():
        # Create a new item set by adding the current item to the current item set
        new_item_set = current_item_set | {item}

        #
        # Calculate the support for the new item set
        new_support = calculate_support(new_item_set, diffsets)

        # If the support is greater than or equal to the minimum support, add the new item set to the list
        if new_support >= min_support:
            new_item_sets.append(new_item_set)

    # While there are still new item sets to process
    t = 0
    while new_item_sets and t != len(item_sets):

        # Initialize a list to store the next round of new item sets
        next_item_sets = []

        # Loop through the new item sets
        for current_item_set in new_item_sets:

            # Add the current item set to the frequent item sets list
            if current_item_set not in frequent_item_sets:
                frequent_item_sets.append(current_item_set)

            # Loop through the item sets
            for item, support in item_sets.items():
                # Create a new item set by adding the current item to the current item set
                if current_item_set != {item}:
                    new_item_set = current_item_set | {item}

                # Calculate the support for the new item set
                new_support = calculate_support(new_item_set, diffsets)

                # If the support is greater than or equal to the minimum support, add the new item set to the list
                if new_support >= min_support and new_item_set not in next_item_sets:
                    next_item_sets.append(new_item_set)
        # Set the new item sets to be processed to the next round of new item sets
        new_item_sets = next_item_sets
        t += 1


def generate_association_rules(frequent_item_sets, transactions, min_lift, min_confidence):
    association_rules = []

    for item_set in frequent_item_sets:
        if len(item_set) > 1:
            for item in item_set:
                # Create the antecedent and consequent for the rule
                antecedent = item_set - {item}
                consequent = {item}

                # Calculate the support, confidence, and lift for the rule
                support = calculate_support(item_set, transactions)
                confidence = support / \
                    calculate_support(antecedent, transactions)
                lift = confidence / calculate_support(consequent, transactions)

                # If the lift and confidence are greater than the minimum values, add the rule to the list
                if lift > min_lift and confidence > min_confidence:
                    association_rules.append(
                        (antecedent, consequent, support, confidence, lift*1000))

    # Return the list of association rules
    return association_rules


def calculate_support(item_set, diffsets):
    # Initialize a counter to store the support for the item set
    support = 0

    # Loop through the diffsets
    for diffset in diffsets:
        # If the item set is a subset of the diffset, increment the support
        if item_set.issubset(diffset):
            support += 1

    # Return the support
    return support
