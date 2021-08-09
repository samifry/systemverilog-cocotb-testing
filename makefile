#-----------------------------------------------------------------
#-- Projet d'approfondissement - Makefile
#--
#-- File : makefile
#-- Description : Grouping of cocotb configurations
#-- and parameters for the execution of the simulation via the "make" command
#--
#-- Author : Sami Föry
#-- Master : MSE Mechatronics
#-- Date : 02.05.2021
#-----------------------------------------------------------------

# defaults
SIM ?= questa
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/dff.sv
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = dff

# MODULE is the basename of the Python test file
MODULE = dff_tb

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
