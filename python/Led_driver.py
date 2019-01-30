# This is the dirver of the digital tube
# for raspy-berry
#
# 5 function can be used
# # assign_bit(): used to re assign the pin for every bit
# # set_eps(): used to set the eps of each number to be shown
# # set_number(): used to set value of each number
# # start(): call this to make digital tube work
# # stop(): call this to make it stop
# # 
# # notice:
# # 1. set_eps() must to be called if there exist more than 1 number to be shown
# # 2. please assign_bit() and set_eps() before you call start() ( if you need to re set )
# # 3. there is no need to set_number() before you start() it, you can set_number() at any time
# # 4. be atention to the stop(), you should call it after use, if you terminate the process before you stop() it, there will exist a zombie process in your memory, remember to kill it manually
#
# Attention: the multiplexing mode not be tested yet , try it yourself, ^-^

import RPi.GPIO as GPIO
import time
import multiprocessing
import math

# the GPIO interface
_pin_0_7 = [17, 18, 27, 22, 23, 24, 25, 4]
_pin_21_29 = [5, 6, 13, 19, 26, 12, 16, 20, 21]

# the code of number 0~9
_code = [0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b]

# the way to multiplexing
_multi_code = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


class led:
    # constant
    __multi = 0  # set 0 for no multiplexing, 1 for multiplexing
    __comm = 1  # set 1 for common anode, 0 for cathode
    __seg_pin = []  # segment select pin
    __bit_pin = []  # bit select pin
    __bit_total = 8  # how many bits are in use (digital tube)
    __multi_mode = []  # the way to multiplexing
    __bit_assign = []  # used to re assign the bit signal
    __eps = []

    # variable
    __THE_SHOWN_NUMBER = multiprocessing.Array('d', 4)  # the number need to be shown, use a list to store
    __p = None  # the process variable
    # __running_flag = multiprocessing.Value('i', 1)  # running flag, if this flag have been turned to false, stop the child process

    # make the GPIO usable
    def __init_GPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    # set the GPIO pin to output
    def __init_pin(self, list):
        for i in list:
            GPIO.setup(i, GPIO.OUT)

    # used to re-assign the bit
    # e.g. [2,4,2] means the first number use 2 bit to show, the second number use 4 bit, ...
    def assign_bit(self, assign_list):
        if len(assign_list) > 5:
            return
        if sum(assign_list) > 16:
            return
        self.__bit_assign = assign_list

    # if the eps is not set, it will be 2
    # if you need show more than 2 numbers ( 2 include ), you must to set the eps by this function
    def set_eps(self, eps_list):
        self.__eps = eps_list

    def __init__(self, bits=8, multi=0, bsi=_pin_21_29, mulc=_multi_code, comm=1, ssi=_pin_0_7):

        # config operating parameters
        self.__bit_total = bits
        self.__multi = multi
        if self.__multi == 0:
            self.__bit_pin = bsi[:self.__bit_total]
        else:
            self.__bit_pin = bsi[:int(math.ceil(math.log(self.__bit_total, 2)))]
            self.__multi_mode = mulc[:self.__bit_total]
        self.__comm = comm
        self.__seg_pin = ssi
        self.__bit_assign = [bits]

        # initial
        self.__init_GPIO()
        self.__init_pin(self.__seg_pin)
        self.__init_pin(self.__bit_pin)

        self.set_eps([2])

    # math function below #########################################
    ###############################################################

    # find the index of a char from a string, return -1 if not found
    def __get_index(self, st, c):
        try:
            index = st.index(c)
        except ValueError:
            index = -1
        return index

    # format the number
    # num: the number need to split into single bit
    # eps: the decimals need to keep
    # total: the total bits
    #
    # return st
    def __get_format_number(self, num, eps, total):
        format_str = '%' + str(total + 1) + '.' + str(eps) + 'f'
        st = str(format_str % num)

        dot = self.__get_index(st, '.')
        if dot == -1:
            if st[0] != ' ':
                return -1
            else:
                st = st[1:]
        else:
            if dot > total:
                return -1
            elif dot == total:
                st = st[:total]
            else:
                st = st[:total+1]
        return st

    # transform the string format number to the code
    def __get_code(self, st):
        list = []
        buff = 0x00

        for i in range(len(st)):
            if st[i] == ' ':
                buff = 0x00
            elif st[i] == '-':
                buff = 0x01
            elif st[i] == '.':
                list[-1] = list[-1] | 0x80
                continue
            else:
                buff = _code[int(st[i])]
            list.append(buff)
        return list

    # led function below ######################################
    ###########################################################

    # segment select signal
    # the code is a 2-bit-hex,
    def __segment_select(self, code):
        for i in range(8):
            if (code & (0x80 >> i)):
                GPIO.output(self.__seg_pin[i], not self.__comm)
            else:
                GPIO.output(self.__seg_pin[i], self.__comm)

    # bit select signal
    # used to chose which bit to show
    # use hex code as weel
    def __bit_select(self, code):
        bits = self.__bit_total
        if self.__multi:
            bits = int(math.ceil(math.log(self.__bit_total, 2)))
        for i in range(bits):
            if (code & (1 << (bits - 1 - i))):
                GPIO.output(self.__bit_pin[i], self.__comm)
            else:
                GPIO.output(self.__bit_pin[i], not self.__comm)

    # used to clear the bit signal
    def __bit_off(self):
        bits = self.__bit_total
        if self.__multi:
            bits = int(math.ceil(math.log(self.__bit_total, 2)))
        for i in range(bits):
            GPIO.output(self.__bit_pin[i], not self.__comm)

    # show one bit
    # the argument 'bit' should be in the range of 0 to 16
    # if not re-setted, the 0 bit means the GPIO.21, 1 bit is GPIO.22
    def __light_on_1(self, code, bit):
        self.__segment_select(code)
        bit_code = bit
        if self.__multi == 0:
            bit_code = 1 << (self.__bit_total - 1 - bit)
        self.__bit_select(bit_code)

    # set the number to be shown
    def set_number(self, number, index):
        self.__THE_SHOWN_NUMBER[index] = number

    # show numbers
    def __light_on(self, f):
        t1 = time.time()
        while True:
            for i in range(len(self.__bit_assign)):
                number = self.__THE_SHOWN_NUMBER[i]
                hex_code = self.__get_code(self.__get_format_number(number, self.__eps[i], self.__bit_assign[i]))
                for j in range(self.__bit_assign[i]):
                    self.__bit_off()
                    self.__light_on_1(hex_code[j], sum(self.__bit_assign[:i]) + j)
                    time.sleep(f)

    # start the led
    def start(self, f = 0.0002):
        self.__p = multiprocessing.Process(target=self.__light_on, args=(f,))
        self.__p.start()

    # stop the led
    def stop(self):
        # self.__running_flag = 0
        self.__p.terminate()
        self.__p.join()
        self.__bit_off()
        self.__bit_select(0x00)
