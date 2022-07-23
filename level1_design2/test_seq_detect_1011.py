# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await Timer(10,"us")
    dut.reset.value = 0
    #await RisingEdge(dut.clk)

    # try generating values between 0 to 31 and giving this as the input to seq det.
   
    for i in range(188):
        bi_list=[]
        a=bin(i)[2:].zfill(8)
        # an extra zero is added on the right side to overcome the issue of 1011 pattern occuring in the final part of input and to detect the pattern. 
        a=a[::-1].zfill(9)[::-1]
        print(i,end=" ")
        print(a)
        for i in range(len(a)):
            bi_list.append(a[i])
        
        for i in range(len(bi_list)):
            #print("original input",end=" ")
            #print(a[i])
            #dut.inp_bit.value = BitArray(bin=bi[list[i]]).int
            dut.inp_bit.value=int(bi_list[i],2)
            
            #print(cocotb.utils.get_sim_time("us"))
            await RisingEdge(dut.clk)
            await Timer(10,"us")
            #print("input is",end=" ")
            #print( dut.inp_bit.value)
            #print('output from design')
            #print(dut.seq_seen.value)
            if(dut.seq_seen.value == 1):
                print("Randomised test with input and output for sequence detected cases respectively: {inp_stream} & {seq_detected}".format(inp_stream=a, seq_detected=dut.seq_seen.value))
            #print("current state is",end=" ")
            #print(dut.current_state.value)
            #print("next state is",end=" ")
            #print(dut.next_state.value)
            if(i+1 == len(a)):
                #print("resetting the circuit")
                dut.reset.value=1
                await Timer (10,"us")
                dut.reset.value=0
                await Timer (10,"us")
        print('\n')
        
    cocotb.log.info('#### CTB: Test Developed! ######')
