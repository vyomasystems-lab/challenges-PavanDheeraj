/**
 * @author  Pavan Dheeraj K
 * @version 1.0, 17/07/2022
 */
module stack(full, empty, d_out, top_of_stack, push, pop, d_in, clk, rst_n);

parameter data_bus_width = 8;
parameter address_bus_width = 4;
parameter depth = 1<<address_bus_width;

input clk,rst_n,push,pop;
input [data_bus_width-1:0] d_in;
output [address_bus_width-1:0] top_of_stack;
output full,empty;
output reg [data_bus_width-1:0] d_out;

reg [address_bus_width-1:0] ptr;
reg [data_bus_width-1:0] mem[0:depth-1];

//points to the top of stack, location where the latest data pushed into the stack is present.
assign top_of_stack=ptr;

//generate full and empty conditions
assign full = (ptr==depth-1)? 1'b1: 1'b0;
assign empty = (|ptr);

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
	ptr<=ptr+1;
	end
end

endmodule
