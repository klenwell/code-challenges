"""
The problem:

Given an array of numbers and a sum value. Find the first two numbers in the array
that add to the sum value. ([3, 5, 9, 6, 12, 15]; 18)
"""

def array_sum(array, sum):
    # Interviewer gave me this clue during interview. Didn't figure out how to use it until
    # I thought it through after interview.
    complement_cache = {}

    for i, num in enumerate(array):
        complement = sum - num
        comp_index = complement_cache.get(complement)

        if comp_index:
            return [array[comp_index], array[i]]
        else:
            # Initially screwed this up by using complement rather than num as key.
            complement_cache[num] = i

    return None

array = [3, 5, 9, 6, 12, 15]
sum = 18

array_pair = array_sum(array, sum)
print(array_pair)
assert array_pair == [6, 12]
