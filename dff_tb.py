#-----------------------------------------------------------------
#-- Projet d'approfondissement - Test Bench D Flip-Flop
#--
#-- File : dff_tb.py
#-- Description : Functional test and validation of the D Flip-Flop
#-- with assertion based verification
#--
#-- Author : Sami Foery
#-- Master : MSE Mechatronics
#-- Date : 10.05.2021
#-----------------------------------------------------------------

import random
import cocotb
from cocotb.clock import Clock
from cocotb.utils import get_sim_time
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles
from coroutine import wait_delay, wait_delay_rand, assert_sync, assert_set_async,\
assert_res_async, assert_nd_async, assert_pulse_time, assert_clock_test, assert_data_check, assert_simult_nd

@cocotb.test()
async def test_dff(dut):

    #Variable declarations
    clk_period_min = 35
    tmin_data_pulse_high = 16
    tmin_data_pulse_low = 3
    tmax_prop = 21
    tmin_pulse_set_reset = 15
    t_limit = 100

    clock = Clock(dut.clk, clk_period_min, units="ns")  # Create a 18ns period clock on port clk
    #and for respecting the minimum 16ns between d = 1 and the next rising edge of the clock

    clk_gen = cocotb.fork(clock.start())  #Start the clock

    #synchronous mode operation test section (set and reset = 1)
    async def sync_mode():

        await RisingEdge(dut.clk)  #Synchronize with the clock

        dut.d <= 1

        await RisingEdge(dut.fin_point) #Waiting for the end of the parallel execution of the synchronous mode

        await assert_data_check(dut.data_check_pulse.value)
        await assert_sync(dut.data_check_prop.value)

        await ClockCycles(dut.clk,1) #Wait for a clock stroke before restarting the test process for the low state of D
        await RisingEdge(dut.clk)

        await wait_delay(tmin_data_pulse_low) #Minimum acceptable delay between a rising edge of the clock and a low level setting of D

        dut.d <= 0

        await RisingEdge(dut.fin_point)

        await assert_data_check(dut.data_check_pulse.value)
        await assert_sync(dut.data_check_prop.value)

    #Asynchronous mode operation test section (set = 0)
    async def async_set_mode():

        dut.lset <= 0

        await wait_delay(tmin_pulse_set_reset) #Pulse time of the set input

        await assert_pulse_time(dut.int_state.value) #Test the intermediate state

        await wait_delay(tmax_prop-tmin_pulse_set_reset) #Waiting and check the max time acceptable before passing q value to 1
        await assert_set_async(dut.q.value, dut.qbar.value) #Test if q is at most 1 after 21ns

        dut.lset <= 1

    #Asynchronous mode operation test section (reset = 0)
    async def async_reset_mode():

        dut.res <= 0

        await wait_delay(tmin_pulse_set_reset) #Pulse time of the set input
        await assert_pulse_time(dut.int_state.value) #Test the intermediate state

        await wait_delay(tmax_prop-tmin_pulse_set_reset) #Waiting and check the max time acceptable before passing q value to 1
        await assert_res_async(dut.q.value, dut.qbar.value)

        dut.res <= 1

    #Asynchronous mode operation test section (set and reset = 0)
    async def async_nd_mode():

        #Test when reset and set is encircled
        dut.res <= 0
        dut.lset <= 0

        await wait_delay(tmax_prop) #Waiting and check the max time acceptable before passing q value to not define.
        await assert_nd_async(dut.q.value, dut.qbar.value)

    async def clock_test(clk_test):

        #Stopping the old clock and creating a new one with randomised values
        clk_test.kill()
        clock = Clock(dut.clk, random.randint(clk_period_min,t_limit), units="ns")
        clk_test = cocotb.fork(clock.start())  #Start the clock

        await sync_mode() #Test of the state that uses the clock with randomized values

        #Test of the minimum clock period which must be 35ns (fmax = 30MHz)
        await RisingEdge(dut.clk)
        t1_clk = get_sim_time('ns')
        await RisingEdge(dut.clk)
        t2_clk = get_sim_time('ns')

        mes_period_clk = t2_clk-t1_clk

        await assert_clock_test(mes_period_clk)

        #Stop and restart of the initial clock for a restart of the test process
        clk_test.kill()
        clock = Clock(dut.clk, clk_period_min, units="ns")
        clk_test = cocotb.fork(clock.start())

    async def simult_high():

        dut.lset <= 1
        await wait_delay(3)#Delays that allow a simultaneous state change to be considered in the design
        dut.res <= 1

        await wait_delay(3) #Slight delay before assertion
        await assert_simult_nd(dut.simult_nd_pt)

    #------------------Order of test execution -------------------
    for i in range(2):
        await sync_mode()
        await ClockCycles(dut.clk, 5) #Waiting times before starting each test
        await async_set_mode()
        await ClockCycles(dut.clk, 5)
        await async_reset_mode()
        await ClockCycles(dut.clk, 5)
        await async_nd_mode()
        await ClockCycles(dut.clk, 5)
        await simult_high()
        await ClockCycles(dut.clk, 5)
        await clock_test(clk_gen)
