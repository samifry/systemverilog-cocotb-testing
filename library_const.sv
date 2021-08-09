/*-----------------------------------------------------------------
-- Projet d'approfondissement - library constants
--
-- File : library_const.sv
-- Description : Grouping of constants listed and used in the DUT
--
-- Author : Sami Foery
-- Master : MSE Mechatronics
-- Date : 10.05.2021
-----------------------------------------------------------------*/

// Random values
package library_const;
	int rand_value_clock = $urandom_range(20,0); //Random propagation delay to the outputs for synchronous mode
	int clock_max_value = 22; // Maximum propagation time for synchronous mode
	int rand_value_res_set = $urandom_range(21,0); //Random propagation delay to the outputs for asynchronous mode
	int pulse_value = 12; // Minimum pulse time for set and reset
	int pulse_data_high = 16; // Minimum pulse time of the input d for risign edge
	int pulse_data_low = 3; // Minimum pulse time of the input d for falling eddge
endpackage
