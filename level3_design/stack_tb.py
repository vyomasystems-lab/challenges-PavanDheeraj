# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_stack(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.rst_n.value = 0
    await Timer(10,"us")
    dut.rst_n.value = 1

    for i in range(17):
        if(i==0):
            print("checking empty flag when stack is empty")
            print("empty flag is {empty}".format(empty=dut.empty.value))
            print('\n')
        
        #since we are doing a push and pop operation alternatively, top_of_stack should always be 0.

        if(i%2==0):
            dut.push.value=1
            print("push operation")
        else:
            dut.pop.value=0
            print("pop operation")
            
        #print(cocotb.utils.get_sim_time("us"))
        await RisingEdge(dut.clk)
        await Timer(10,"us")
        top_of_stack=int(dut.top_of_stack.value)
        if(top_of_stack>0):
            print("top of stack is {top_of_stack}".format(top_of_stack=top_of_stack))
            print("test failed")
            break
        print('\n')
        
    cocotb.log.info('#### CTB: Test Developed! ######')