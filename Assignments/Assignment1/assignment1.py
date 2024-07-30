def analyze(results: list, roster: int, score: int) -> list:
    """
    This function will accept an unsorted list of matches,
    And return a list of top 10 matches in a descending score order and a list of matches with the target score.
    Both lists will return in lexicographical order.

    Time Complexity: O(NM); where N is the number of matches and M is the number of characters within a team
    Space Complexity: O(NM); where N is the number of matches and M is the number of characters within a team
    :param results: An unsorted list of matches
    :param roster: The number of characters among each team
    :param score: A given target score
    :return: A list of top 10 matches and a list of matches with the target score, both in lexicographical order
    """
    # Sorting all the letters in lexicographical order
    for i in range(len(results)):
        results[i][0] = count_sort_str(results[i][0], roster)
        results[i][1] = count_sort_str(results[i][1], roster)

    # Converting all the score to be greater than 50, to remove duplicate matches and sort them
    for i in range(len(results)):
        results.append([results[i][1], results[i][0], 100 - results[i][2]])

    # Sorting the matches based on team names in lexicographical order
    radix_sort(results, roster)
    # Sorting the matches based on score in descending order
    count_sort_int(results)

    # Removing all the duplicate matches
    results_nodups = removedups(results)

    # Retrieving the top 10 match results after sorting
    top10 = []
    if len(results_nodups) >= 10:
        for i in range(10):
            top10 += [results_nodups[i]]
    else:
        for i in range(len(results_nodups)):
            top10 += [results_nodups[i]]

    searched = []
    if not score > results_nodups[0][2]:
        # Searching for the index of the given target score
        index = binary_search_min(results_nodups, score)

        # Searching for all the matches that has either the larger and closest or the equal score to the target score
        for i in range(len(results_nodups)):
            if results_nodups[i][2] == results_nodups[index][2]:
                searched.append(results_nodups[i])

    return [top10, searched]


def binary_search_min(results: list, score: int) -> int:
    """
    This function will use the Binary Search algorithm to find the index of a given target score within a list of arrays
    If the target score is found,
        it will return the index of the target score.
    If the target score is not found,
        it will return the index of the larger and closest score to the target score.

    Time Complexity: O(logN); where N is the size of the input
    Aux Space Complexity: O(1); this uses an in-place algorithm, hence it does not require extra space
    :param results: A sorted list in descending score order
    :param score: A given target score
    :return: A list of arrays holding score that is equals to or the closest and larger than the target score
    """
    low = 0
    high = len(results) - 1
    index = 0

    while low <= high:
        index = (high + low) // 2
        if results[index][2] > score:
            low = index + 1
        elif results[index][2] < score:
            high = index - 1
        else:
            return index

    if results[index][2] < score:
        index -= 1

    return index


def radix_sort(arr: list, roster: int):
    """
    Using a stable counting sort, this function will be used to sort the teams in lexicographical order.
    It will keep track of which team the counting sort is sorting and which position of the string is being sorted.

    Time Complexity: O(NM); where N is the size of the input and M is the length of the longest string in the array
    Aux Space Complexity: O(1); this is an in-place algorithm, hence it does not require extra space,
                                even though it uses counting sort algorithm, which has an Aux Space Complexity of O(N+U)
    :param arr: An unsorted array
    :param roster: The length of the character set
    :return: A sorted array in lexicographical order
    """
    maxLength = len(arr[0][0])
    team = 1
    while team >= 0:
        place = 0
        while maxLength > place:
            count_sort_rad(arr, roster, place, team)
            place += 1
        team -= 1


def count_sort_rad(arr: list, roster: int, place: int, team: int):
    """
    This algorithm will be used to sort the teams in lexicographical order.
    It will sort the teams with different position of the string each time,
    From the rightmost letter to the leftmost letter.
    The position of the string is assigned by the radix_sort function.

    Time Complexity: O(N+U); where N is the size of the input and U is the size of the count array
    Aux Space Complexity: O(N+U); where N is the size of the input and U is the size of the count array
    :param arr: An unsorted array
    :param roster: The length of the character set
    :param place: The position of the string that is being sorted
    :param team: The team that is being sorted in that match
    :return: An array that is partially sorted (i.e. the position of the string that is being sorted)
    """
    count = [0] * roster
    pos = [0] * roster
    pos[len(pos) - 1] = 1
    output = [0] * len(arr)

    # Iterate through the input and count the number of times each letter in that particular position occurs
    for i in range(len(arr)):
        k = len(arr[i][team]) - place
        count[ord(arr[i][team][k - 1]) - 65] += 1

    # Finding the position of each string
    i = len(pos) - 2
    while i >= 0:
        pos[i] = pos[i+1] + count[i+1]
        i -= 1

    # Mapping each string to their correct position
    for i in range(len(arr)):
        k = len(arr[i][team]) - place
        output[pos[ord(arr[i][team][k - 1]) - 65] - 1] = arr[i]
        pos[ord(arr[i][team][k - 1]) - 65] += 1

    for i in range(len(output)):
        arr[i] = output[i]


def count_sort_str(a: str, roster: int):
    """
    This algorithm will sort each letter in a string in lexicographical order,
    which allows us to sort each string in lexicographical order.
    It uses the count array to count the number of times each letter in the string occurs,
    and use them to find and map the position of each letter in the string.

    Time Complexity: O(M+U); where M is the length of the string and U is the size of the count array
    Aux Space Complexity: O(M+U); where M is the length of the string and U is the size of the count array
    :param a: An unsorted string
    :param roster: The length of the character set
    :return: A sorted string in lexicographical order
    """
    count = [0] * roster
    pos = [0] * roster
    pos[0] = 1
    output = [''] * len(a)

    # Iterate through the input and count the number of times each letter occurs
    for i in range(len(a)):
        count[ord(a[i]) - 65] += 1

    # Finding the position of each letter
    for i in range(1, len(pos)):
        pos[i] = pos[i - 1] + count[i - 1]

    # Mapping each letter to their correct position
    for i in range(len(a)):
        output[pos[ord(a[i]) - 65] - 1] = a[i]
        pos[ord(a[i]) - 65] += 1

    string = ""

    # Copying each letter to a string and return the string
    for i in range(len(output)):
        string += output[i]

    return string


def count_sort_int(arr: list):
    """
    Counting Sort is a non-comparing sorting algorithm that can sort any non-negative integer.
    Counting Sort will first find the maximum value of an unsorted array.
    It will then create a count array with that size, which will be used to count the number of times each value occurs.
    Using the data collected in the count array,
    Each value will then be mapped to their correct position in the output array.

    Time Complexity: O(N+U); where N is the size of the input and U is the size of the count array
    Aux Space Complexity: O(N+U); where N is the size of the input and U is the size of the count array
    :param arr: An unsorted array
    :return: A sorted array in descending score order
    """
    maxNum = 100

    count = [0] * (maxNum + 1)
    pos = [0] * (maxNum + 1)
    pos[0] = 1
    output = [0] * len(arr)

    # Iterate through the input and count the number of times each value occurs
    for i in range(len(arr)):
        count[arr[i][2]] += 1

    # Finding the position of each value
    for i in range(1, len(pos)):
        pos[i] = pos[i-1] + count[i-1]

    # Mapping each value to their correct position
    for i in range(len(arr)):
        output[pos[arr[i][2]] - 1] = arr[i]
        pos[arr[i][2]] += 1

    # Sorting each value's position in descending order
    j = len(output) - 1
    i = 0
    while j >= 0:
        arr[i] = output[j]
        i += 1
        j -= 1


def removedups(arr: list):
    """
    This algorithm will be used to remove all the duplicate matches in a sorted list.
    Since the list is sorted, meaning that all the duplicate matches will be placed next to each other.
    With that logic we can traverse through the input,
    And check if the current match result is the same as the next match result in the list.
    All the unique match results will be appended to an output array.

    Time Complexity: O(N); where N is the size of the input
    Aux Space Complexity: O(N); where N is the size of the input
    :param arr: A sorted list with duplicate elements
    :return: A sorted list without any duplicate elements
    """
    k = len(arr) - 1
    i = 0
    # The first match result will always be unique
    output = [arr[0]]

    # While k is greater than i,
    while k > i:
        # If the current i element is the same as the i + 1 element, increment i by 1
        if [arr[i]] == [arr[i+1]]:
            i += 1
        # Else, append the i + 1 element to the output array and increment i by 1
        else:
            output += [arr[i+1]]
            i += 1

    return output
