/*-----------------------------------------------------------------
-- Projet d'approfondissement - DUT D Flip-Flop
--
-- File : dff.sv
-- Description : Functional design of the D Flip-Flop
--
-- Author : Sami Foery
-- Master : MSE Mechatronics
-- Date : 10.05.2021
-----------------------------------------------------------------*/

`timescale 1ns/1ps
`include "library_const.sv"

import library_const::*;
module dff (
	input logic lset = 1, res = 1, clk, d,
	output logic q, qbar,
	logic int_state = 0, int_state_gap = 0, data_check_pulse, data_check_prop, fin_point, simult_nd_pt
);

	// Clocking block -> Necessary for working with clock strokes
	default clocking cb @(posedge clk);
	endclocking

	//Variable declarations
	real diff_val;
	logic save_data;
	realtime time_1, time_2;
	logic qs, qas, qar, qu; //Intermediate work signals

	// Synchronous mode
	always @(posedge clk iff (res == 1 && lset == 1)) begin

		save_data = $past(d,1); //Assigning the value of d to a previous clock stroke
		//Condition with d at its high level
		fork : wait_data
			begin //Pulse data
				fork : wait_pulse
					begin //data high
						time_1 = $realtime;
						@(negedge clk)
						if ((save_data !== d) && (d == 1))	begin
							@(posedge clk)
							time_2 = $realtime;
							diff_val = time_2-time_1;
							if (diff_val >= pulse_data_high) begin
								data_check_pulse = 1;
								disable wait_pulse;
							end else
								data_check_pulse = 0;
								disable wait_pulse;
						end
					end

					begin //data low
						if (d !== 0) begin
							#pulse_data_low;
							if (d === 0) begin
								data_check_pulse = 0;
								disable wait_pulse;
							end else
								data_check_pulse = 1;
						end
					end
				join
			end

			begin //Propagation delay
				fork : wait_prop
					begin
						#rand_value_clock;
						data_check_prop = 1;
						disable wait_prop;
					end

					begin
						#clock_max_value;
						data_check_prop = 0;
						disable wait_prop;
					end
				join

			end
		join

		fin_point = 1; //Point at which parallel processes end

		if (data_check_prop == 1)
			qs = d;

		fin_point = 0;
	end

	//Asynchronous mode where set has been called
	always @(negedge lset iff (res == 1)) begin

		//Parallel execution of processes
		fork : wait_or_timeout_set
  		begin
    		#pulse_value; //#12ns
				int_state = 1;
				#(rand_value_res_set-pulse_value);
				qas = 1;
    		disable wait_or_timeout_set;
  		end
  		begin
    		@(posedge lset);
				int_state = 0;
    		disable wait_or_timeout_set;
  		end
		join

	end

	 //Asynchronous mode where reset has been called
	always @(negedge res iff (lset == 1)) begin

		//Parallel execution of processes
		fork : wait_or_timeout_reset
			begin
				#pulse_value; //#12ns
				int_state = 1;
				#(rand_value_res_set-pulse_value);
				qar = 0;
				disable wait_or_timeout_reset;
			end
			begin
				@(posedge res);
				int_state = 0;
				disable wait_or_timeout_reset;
			end
		join

	end

	//Asynchronous mode where set and reset has been called
	always @(negedge lset iff (res == 0)) begin
		#rand_value_res_set;
		qu = 1; // Both outputs remain high as long as set and reset are low at the same time.
	end

	always @(negedge res iff (lset == 0)) begin
		#rand_value_res_set;
		qu = 1; //Both outputs remain high as long as set and reset are low at the same time.
	end

	//Set and reset to their high states simultaneously
	always @(posedge lset or posedge res) begin
		fork : simult_test //Competing processes between SET or RESET state change and delay.
			begin
				@(posedge res iff lset==1 or posedge lset iff res==1)
				simult_nd_pt = 1;
				qs = 5'bx;
				disable simult_test;
			end
			begin
				#5; //Maximum time defined before state changes are not considered "simultaneous".
				simult_nd_pt = 0;
				disable simult_test;
			end
		join
	end

	//Assigning the correct signal to the real output
	//Multiplexer design
	always_comb begin
		if (res == 1 && lset == 1) begin
			q = qs;
			qbar = ~qs;
		end else if (res == 1 && lset == 0) begin
			q = qas;
			qbar = ~qas;
		end else if (res == 0 && lset == 1) begin
			q = qar;
			qbar = ~qar;
		end else if (res == 0 && lset == 0) begin
			q = qu;
			qbar = qu;
		end
	end

	// the "macro" to dump signals
	`ifdef COCOTB_SIM
	initial begin
	  $dumpfile ("dff.vcd");
	  $dumpvars (0, dff);
	  #1;
	end
	`endif

endmodule
