# challenges-PavanDheeraj
# Mux Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

Gitpod Environment
![gitpod_env](https://user-images.githubusercontent.com/58168687/182022642-e18b2bdf-945e-49f4-8eda-034c0c2012eb.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (stack module here) which takes in "4" 1-bit inputs (clk,rst_n,push,pop), "1" 8 bit input (d_in) and gives "1" 8-bit output (d_out), "2" 1-bit outputs (full,empty), "1" 4-bit output(top_of_stack).

The values are assigned to the input port "clk" using clock class which is a built in class for toggling a clock signal. The design has a active low reset signal which is asserted and deasserted as follows:
```
dut.rst_n.value = 0
await Timer(10,"us")
dut.rst_n.value = 1
```
The assert statement is used for comparing a flag signal with a constant.

The following error is seen:
```
assert flag == 0, "Test failed"

```
## Test Scenario **(Important)**
clk signal is not mentioned in the test inputs section
1. - Test Inputs: dut.push.value=1 and dut.pop.value=1 are given for alternate clock cycles with push aseerted first
   - Expected Output: top_of_stack=0( after pop operation) 
   - Observed Output in the DUT dut.top_of_stack.value=2
   Output mismatches for the above inputs proving that there is a design bug

2. - Test Inputs: dut.rst_n.value = 0, dut.rst_n.value = 1
   - Expected Output: empty=1
   - Observed output: dut.empty.value=0
   Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test inputs and analysing the design, we see the following
```
//generate full and empty conditions
assign full = (ptr==depth-1)? 1'b1: 1'b0;
assign empty = (|ptr); -----> BUG

always@(posedge clk or negedge rst_n)
begin
if(~rst_n)
	ptr<=0;
else if(push & ~full) begin
	mem[ptr]<=d_in;
	ptr<=ptr+1;
	end
else if(pop & ~empty) begin
	d_out<=mem[ptr-1];
	ptr<=ptr+1; ------> BUG
	end
end
```
Test Case 1:
![stack_error_1](https://user-images.githubusercontent.com/58168687/182054592-2c3a499f-ff16-49cc-9ced-f75715083f38.PNG)
Test Case 2:
![stack_empty](https://user-images.githubusercontent.com/58168687/182054142-54f53bc7-50be-4c4f-97fa-e350e3ce3603.PNG)

In the stack design, for the empty flag generation after the reduction OR operation, the result should be given to NOT gate to get the correct output. 
In the always block, for pop statement, the pointer should get decremented instead of getting incremented.

## Design Fix
Updating the design and re-running the test makes the test pass.
![stack_pass_with_bug_fixes](https://user-images.githubusercontent.com/58168687/182054335-e02a84e8-cea4-4d01-ba76-19859361b4a2.PNG)

The updated design is checked in as stack.v

## Verification Strategy
The strategy was to do a push and pop operation alternatively, so that top_of_stack does not exceed 1, this is used to check if the pointer are getting incremented and  decremented for push and pop operation respectively. 

## Is the verification complete ?
No, the d_in and d_out signals have not been tested.

