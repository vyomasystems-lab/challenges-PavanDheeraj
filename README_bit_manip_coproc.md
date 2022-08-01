# challenges-PavanDheeraj
# Bit manipulation coprocessor Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

Gitpod Environment
![gitpod_env](https://user-images.githubusercontent.com/58168687/182022642-e18b2bdf-945e-49f4-8eda-034c0c2012eb.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (bit manipulation coprocessor module here) which takes in "4" 32-bit inputs (mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3) and gives "1" 33-bit output (mav_putvalue)

The values are assigned to the input port "mav_putvalue_instr" using a list which contains the instruction values which can be given to the DUT(for which behavior is defined). Values are assigned to the input ports "mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3" using "randint" function imported from "random"

```
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
       
        rand_idx = int(random.random() * len(test1))
        random_num = test1[rand_idx]
        random_num=test1[rand_idx]
        mav_putvalue_src1 = random.randint(0,4294967295)
        mav_putvalue_src2 = random.randint(0,4294967295)
        mav_putvalue_src3 = random.randint(0,4294967295)
        mav_putvalue_instr = random_num
```

The assert statement is used for comparing the DUT's output to the expected value from the bug free model.

The following error is seen:
```
error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
assert dut_output == expected_mav_putvalue, error_message

```

## Test Scenario **(Important)**
1. - Test Inputs: mav_putvalue_instr=0x40007033, mav_putvalue_scr1=0x81b5efc5,mav_putvalue_src2=0x342c471d,mav_putvalue_src3=0x8086c40f
   - Expected Output: out=0x103235181
   - Observed Output in the DUT dut.mav_putvalue.value=0x488e0b
   
   Output mismatches for the above inputs proving that there is a design bug

2. - Test Inputs: mav_putvalue_instr=0x40007033, mav_putvalue_scr1=0xb9c5e854, mav_putvalue_src2=0xecf7f6df, mav_putvalue_src3=0x43c68551
   - Expected Output: out=0x22001001
   - Observed output: out=0x1518bc0a9
   
   Output mismatches for the above inputs proving that there is a design bug

From the above scenario's, it is observed that there is a design bug in ANDN instruction in the instruction set.

## Design Bug
Based on the above test inputs and analysing the design, we see the following

Test Case 1:
![bit_manip_error_1](https://user-images.githubusercontent.com/58168687/182033351-d5f3e0e2-d414-4f4a-84b8-a76306190707.PNG)
Test Case 2:
![bit_manip_error_2](https://user-images.githubusercontent.com/58168687/182033366-8bd2f90e-92ad-4a0f-850c-ddbc96e4821e.PNG)

For this design, there is a bug in the implementation of ANDN function in the instruction set.

## Verification Strategy
The values corresponding to different instructions were created as a list. Test would continue until there is a mismatch between the DUT output and model output, when a mismatch is detected, the loop terminates. Everytime an instruction would be picked from a list containing different instructions. The operands are generated randomly with their lower limit and upper limit defined. After extensive testing, it is observed that there is design bug in ANDN instruction implementation.
Another test was run excluding "ANDN" instruction from the intsruction set, the test passed without any issues. Below is a screenshot attached for reference.

Test Pass:
![bit_manip_intrs_pass](https://user-images.githubusercontent.com/58168687/182033413-4741741d-c52f-4878-a9b4-63030de1d3e4.PNG)

## Is the verification complete ?
Yes

