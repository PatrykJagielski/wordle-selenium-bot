
def save_file(path, data):
    with open(path, 'w') as file:
        file.write(data)

NUM_OF_LETTERS = 11

if __name__ == '__main__':
    with open('slowa.txt', 'r') as file:
        data = ''
        for line in file:
            if len(line) == NUM_OF_LETTERS+1:
                data += line

        save_file(f'{NUM_OF_LETTERS}.txt', data)
