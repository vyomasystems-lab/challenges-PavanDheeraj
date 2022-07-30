# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock
import secrets
from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1

    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    flag=1
    #rand_idx=0
    while(flag==1):

        # initializing list containing opcodes of the instrcution
        # used for selecting the instruction to be executed
        test1 = [1073770547, 1073766451, 1073758259, 536875059, 
        536891443, 1610616883, 1610633267, 536879155, 536887347, 536895539,
        1207963699, 671092787, 1744834611, 1207980083, 671109171, 1744850995,
        100667443, 100683827, 67113011, 67129395, 1610616851, 1611665427, 
        1612714003, 1614811155, 1615859731, 1627394067, 1628442643, 1629491219,
        1635782675, 1636831251, 1637879827, 167776307, 167784499, 167780403, 
        167788595, 167792691, 167796787, 167800883, 1207984179, 134242355, 
        134234163, 1207975987, 134246451, 536875027, 536891411, 1610633235, 
        1207963667, 671092755, 1744834579, 1207980051, 671109139, 1744850963, 
        134221875, 134238259, 134221843, 134238227, 67129363, 1207988275]
        
        #print("Original list is : " + str(test1))
        
        rand_idx = int(random.random() * len(test1))
        
        #print("random index is ",end=" ")
        #print(rand_idx)
        #if(rand_idx==len(test1)):
        #    print("all intsructions executed except for ANDN")
        #    break

        random_num = test1[rand_idx]

        random_num=test1[rand_idx]
        
        #rand_idx=rand_idx+1

        # printing random number
        #print("Random selected number is : " + str(random_num))
        
        mav_putvalue_src1 = random.randint(0,4294967295)
        mav_putvalue_src2 = random.randint(0,4294967295)
        mav_putvalue_src3 = random.randint(0,4294967295)
        mav_putvalue_instr = random_num
        #le=mav_putvalue_instr
        #le=bin(le)[2:] #convert int to binary
        #le=le.zfill(32)
        #length=len(le)
        #opcode = le[-7::]
        #print(opcode)
        print("inputs to the dut are:")
        print("mav_putvalue_instr = ",end=" ")
        print(hex(mav_putvalue_instr))
        print("mav_putvalue_scr1 = ",end=" ")
        print(hex(mav_putvalue_src1))
        print("mav_putvalue_src2 = ",end=" ")
        print(hex(mav_putvalue_src2))
        print("mav_putvalue_src3 = ",end=" ")
        print(hex(mav_putvalue_src3))
        print('\n')
        # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        #dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
    
        yield Timer(1) 

        # obtaining the output
        dut_output = dut.mav_putvalue.value
        if(dut_output!=expected_mav_putvalue):
            flag=0
        cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
        assert dut_output == expected_mav_putvalue, error_message
        print('\n')
