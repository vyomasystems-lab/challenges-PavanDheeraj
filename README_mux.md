# challenges-PavanDheeraj
# Mux Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

Gitpod Environment
![gitpod_env](https://user-images.githubusercontent.com/58168687/182022642-e18b2bdf-945e-49f4-8eda-034c0c2012eb.PNG)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (mux module here) which takes in "1" 5-bit input (sel) and "31" 2 bit inputs (inp*) and gives "1" 2-bit output (out)

The values are assigned to the input port "sel" using a "for" loop which runs between 0 to 30 and is used to select 1 of 31 inputs at any given time.
Input port's "inp*" are tied to a fixed value of 1. 
```
 for i in range(31):
        dut.sel.value=i
 A=1
 dut.inp*.value=A
```

The assert statement is used for comparing the mux's output to the expected value.

The following error is seen:
```
assert dut.out.value == A, "Randomised test failed with: {sel} with {out}".format(
         sel=dut.sel.value, out=dut.out.value)

```
## Test Scenario **(Important)**
1.- Test Inputs: sel=12 inp12=1
  - Expected Output: out=1
  - Observed Output in the DUT dut.out.value=0
  Output mismatches for the above inputs proving that there is a design bug

2. Test Inputs: sel=30 inp30=1
   Expected Output: out=1
   Observed output: out=0
   Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test inputs and analysing the design, we see the following
```
case(sel)
      5'b00000: out = inp0;  
      5'b00001: out = inp1;  
      5'b00010: out = inp2;  
      5'b00011: out = inp3;  
      5'b00100: out = inp4;  
      5'b00101: out = inp5;  
      5'b00110: out = inp6;  
      5'b00111: out = inp7;  
      5'b01000: out = inp8;  
      5'b01001: out = inp9;  
      5'b01010: out = inp10;
      5'b01011: out = inp11;
      5'b01101: out = inp12; -----> BUG
      5'b01101: out = inp13;
      5'b01110: out = inp14;
      5'b01111: out = inp15;
      5'b10000: out = inp16;
      5'b10001: out = inp17;
      5'b10010: out = inp18;
      5'b10011: out = inp19;
      5'b10100: out = inp20;
      5'b10101: out = inp21;
      5'b10110: out = inp22;
      5'b10111: out = inp23;
      5'b11000: out = inp24;
      5'b11001: out = inp25;
      5'b11010: out = inp26;
      5'b11011: out = inp27;
      5'b11100: out = inp28;
      5'b11101: out = inp29; // condition missing for inp30 -----> BUG
      default: out = 0;
    endcase
![mux_1](https://user-images.githubusercontent.com/58168687/182023475-876cb8a3-6cbd-4b4c-a30f-f0fa58585e6c.PNG)
![mux_2](https://user-images.githubusercontent.com/58168687/182023484-91fd678d-dfd1-4010-8415-134cd4c9bd92.PNG)
```
For the mux design, the case condition for inp12 must have been "01100" instead of "01101" as in the design code.
The case condition for inp30 is missing in the design.

## Design Fix
Updating the design and re-running the test makes the test pass.
![mux_pass](https://user-images.githubusercontent.com/58168687/182023508-31118159-7c80-46d0-adba-14175104faca.PNG)

The updated design is checked in as mux.v

## Verification Strategy
Keeping the data line inputs to a fixed value except 0(as it is a part of the default condition) and to vary "sel" line input between 0 and 30 to see 
if the "out" output line produces the fixed value to which the input line is tied to.

## Is the verification complete ?
Yes
