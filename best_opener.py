if __name__ == '__main__':
    freq = {
        'a': 0, 'ą': 0, 'b': 0, 'c': 0, 'ć': 0, 'd': 0, 'e': 0, 'ę': 0,
        'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'ł': 0,
        'm': 0, 'n': 0, 'ń': 0, 'o': 0, 'ó': 0, 'p': 0, 'q': 0, 'r': 0,
        's': 0, 'ś': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0,
        'z': 0, 'ź': 0, 'ż': 0
    }
    letter_count = 0
    NUM_OF_LETTERS = 11

    with open(f'{NUM_OF_LETTERS}.txt') as file:
        for line in file:
            for c in line[:-1]:
                freq[c] += 1
                letter_count += 1


    normalized = {}
    for letter, count in freq.items():
        normalized[letter] = count / letter_count

    openers = {}
    with open(f'{NUM_OF_LETTERS}.txt') as file:
        for line in file:
            if len(line) == len(set(line)):
                openers[line[:-1]] = sum(normalized[c] for c in line[:-1])

    
    with open(f'best_openers_{NUM_OF_LETTERS}.txt', 'w') as file:
        data = ''
        for word, points in sorted(openers.items(), key=lambda x: x[1], reverse=True):
            data += word + ' ' + str(points) + '\n'
        file.write(data)
    