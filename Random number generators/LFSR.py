import time

global register_len
global xor_positions
global iterations
global input_data

# register_len = int(input("Length of the shift register:"))
# xor_positions = [int(i) for i in input("Give xor positions: ").split()]
setting = int(input("Give feedback function configuration: "))


# input_data = [int(i) for i in input("Give seed: ").split()]
# iterations = int(input("Give number of iterations: "))


def feedback_function(setting):
    global register_len
    global xor_positions
    global iterations
    global input_data
    if setting == 1:
        register_len = 9
        xor_positions = [4, 8]  # 1+ x^5 + x^9
        iterations = 511  # 2^n - 1
        input_data = [int(i) for i in input("Give seed of length 9: ").split()]
    if setting == 2:
        register_len = 10
        xor_positions = [6, 9]
        iterations = 1023
        input_data = [int(i) for i in input("Give seed of length 10: ").split()]
    if setting == 3:  # very big input
        register_len = 18
        xor_positions = [10, 17]
        iterations = 262143
        input_data = [int(i) for i in input("Give seed of length 18: ").split()]
        # 1 1 0 0 0 1 1 0 1 0 0 1 1 0 1 0 1 0
    if setting == 4:  # input for performance testing, same number of iterations as the other tests
        register_len = 14
        xor_positions = [1, 11, 12, 13]
        iterations = 16383
        input_data = [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0]


def xor(input_data, xor_positions):
    xor = 0
    for i in xor_positions:
        xor = xor ^ input_data[i]
    return xor


def main():
    output = []
    feedback_function(setting)

    begin_time = time.time()

    for j in range(100):
        for i in range(0, iterations):
            output.append(input_data[register_len - 1])
            x = xor(input_data, xor_positions)
            input_data.insert(0, x)
            input_data.pop()

        for i in output:
            print(i, end='')
        print('\n')
        print('#0: ', output.count(0))
        print('#1: ', output.count(1))
        print("Bit sequence:")
        output.clear()
    end_time = time.time()



    print('Runtime: ', end_time - begin_time)


main()
