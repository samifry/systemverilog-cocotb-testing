#-----------------------------------------------------------------
#-- Projet d'approfondissement - coroutine test bench D Flip-Flop
#--
#-- File : coroutine.py
#-- Description : Functions called from the test bench before being
#-- executed and returning results.
#--
#-- Author : Sami Foery
#-- Master : MSE Mechatronics
#-- Date : 10.05.2021
#-----------------------------------------------------------------

#Coroutines Python
import random
import cocotb
from cocotb.clock import Timer

@cocotb.coroutine
async def wait_delay_rand(tmin,tmax): #Function that retrieves the range of values to be randomised.
    await Timer(random.randint(tmin,tmax), units='ns')

async def wait_delay(tmax): #Function that retrieves the maximum value to be tested
    await Timer(tmax, units='ns')

async def assert_sync(d_chk_prop):
    assert d_chk_prop == 1, "The output q does not have the right value at the right time"

async def assert_set_async(q,qbar):
    assert q == 1, "The output q does not have the right value at the right time"
    assert qbar == int(~q), "Inverse output signal of q was incorrect"

async def assert_res_async(q,qbar):
    assert q == 0, "The output q does not have the right value at the right time"
    assert qbar == int(~q), "Inverse output signal of q was incorrect"

async def assert_nd_async(q,qbar):
    assert q == 1, "The output q is not at the high level."
    assert qbar == 1, "The output qbar is not at the high level."

async def assert_pulse_time(int):
    assert  int == 1 , "Pulse time of set or reset is too short."

async def assert_data_check(d_check):
    assert  d_check  == 1 , "Pulse time of data is too short."

async def assert_clock_test(mes):
    tmin = 32
    assert mes >= tmin, "The maximum frequency of the clock has been exceeded."

async def assert_simult_nd(nd_pt):
    assert nd_pt == 1, "After a simultaneous return of set and reset to high level, the outputs are not undefined"
