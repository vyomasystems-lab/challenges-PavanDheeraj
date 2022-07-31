# challenges-PavanDheeraj
# Sequence Detector Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

Gitpod Environment
![gitpod_env](https://user-images.githubusercontent.com/58168687/182022642-e18b2bdf-945e-49f4-8eda-034c0c2012eb.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (seq detector module here) which takes in "3" 1-bit inputs (clk,reset,inp_bit) and gives "1" 1-bit output (seq_seen)

The values are assigned to the input port "clk" using clock class which is a built in class for toggling a clock signal. The design has a active high reset signal which is asserted and deasserted as follows:
```
dut.reset.value = 1
await Timer(10,"us")
dut.reset.value = 0

```
Input port "inp_bit" is given a sequence of 1's and 0's based on which seq_seen is asserted. 
```
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
            dut.inp_bit.value=int(bi_list[i],2)
```
We do not terminate the test using an assert statement, as input range to be tested is large. 

## Test Scenario **(Important)**
clk and reset inputs are not mentioned in the test inputs section.
Test inputs are mentioned in the following format:
"decimal" "binary equivalent"
1. - Test Inputs: "11" "00001011"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

2. - Test Inputs: "27" "00011011"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug
   
3. - Test Inputs: "43" "00101011"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug
   
4. - Test Inputs: "54" "00110110"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

5. - Test Inputs: "55" "00110111"  
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

6. - Test Inputs: "59" "00111011"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

7. - Test Inputs: "75" "01001011"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug
   
8. - Test Inputs: "86" "01010110"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

9. - Test Inputs: "87" "01010111"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

10. - Test Inputs: "107" "01101011"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

11. - Test Inputs: "108" "01101100"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

12. - Test Inputs: "109" "01101101"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

13. - Test Inputs: "110" "01101110"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

14. - Test Inputs: "111" "01101111"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

15. - Test Inputs: "123" "01111011"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

16. - Test Inputs: "155" "10011011" 
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug

17. - Test Inputs: "172" "10101100"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug
 
18. - Test Inputs: "173" "10101101"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug
   
19. - Test Inputs: "174" "10101110"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug
   
20. - Test Inputs: "175" "10101111"
   - Expected Output: out=1
   - Observed Output in the DUT dut.seq_seen.value=0
   Output mismatches for the above inputs proving that there is a design bug
   
21. - Test Inputs: "187" "10111011" ---> Special Case
   
## Design Bug
Based on the above test inputs and analysing the design, we see the following
```
  // state transition based on the input and current state
  always @(inp_bit or current_state)
  begin
    case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE; -----> BUG
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE; -----> BUG
      end
      SEQ_1011:
      begin
        next_state = IDLE;
      end
    endcase
  end
```
1. For the sequence detector design, in the "IDLE" state after detecting a "1" we go to "SEQ_1" state. In "SEQ_1", if we again receive "1" we move to "IDLE" state, this is a design bug, instead we should remain on "SEQ_1" to be aligned with the design specifications.
2. Similarly, in the "SEQ_101" state after detecting a "1" we go to SEQ_1011 state. In SEQ_101, if we receive "0" we move to "IDLE" state, this is a design bug, instead we should move to "SEQ_10" to be aligned with the design specifications.
3. Also a special case to be considered is "10111011", we should see "seq_seen" asserted twice but in the design "seq_seen" needs an one extra clock cycle to get asserted during which the initial "1" for the next sequence gets missed and the pattern is not detected. 

## Design Fix
Updating the design and re-running the test makes the test pass.
![seq_det_pass](https://user-images.githubusercontent.com/58168687/182028774-dc5a0f5b-7dc4-4a3e-a994-4a63e8f16e48.PNG)

The updated design is checked in as seq_detect_1011.v

## Verification Strategy
The strategy to test this design was to use different patterns as input to the DUT. This was done by running a loop from "0" to "187". 1 bit at a time was extracted from the binary value and was given as the input to the DUT. End point was chosen to be "187" because of it's binary value "10111011" to test if the design could detect two consecutive matching patterns. Also an extra zero was padded to the LSB part to overcome the situation where the pattern "1011" occurs at the end of the string.

## Is the verification complete ?
Yes
