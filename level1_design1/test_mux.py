# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    for i in range(31):
        dut.sel.value=i
        A=1
        dut.inp0.value = A
        dut.inp1.value = A
        dut.inp2.value = A
        dut.inp3.value = A
        dut.inp4.value = A
        dut.inp5.value = A
        dut.inp6.value = A
        dut.inp7.value = A
        dut.inp8.value = A
        dut.inp9.value = A
        dut.inp10.value = A
        dut.inp11.value = A
        dut.inp12.value = A
        dut.inp13.value = A
        dut.inp14.value = A
        dut.inp15.value = A
        dut.inp16.value = A
        dut.inp17.value = A
        dut.inp18.value = A
        dut.inp19.value = A
        dut.inp20.value = A
        dut.inp21.value = A
        dut.inp22.value = A
        dut.inp23.value = A
        dut.inp24.value = A
        dut.inp25.value = A
        dut.inp26.value = A
        dut.inp27.value = A
        dut.inp28.value = A
        dut.inp29.value = A
        dut.inp30.value = A # condition missing in case 
        
        await Timer(2, units='ns')
        
 
        assert dut.out.value == A, "Randomised test failed with: {sel} with {out}".format(
         sel=dut.sel.value, out=dut.out.value)
