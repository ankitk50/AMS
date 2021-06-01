"""
This file should be used to keep all necessary code that is used for the verification and simulation section in part 4
of the programming assignment. It contains tasks 4.2.1, 4.3.1 and 4.3.2.
"""


from counter import TimeIndependentAutocorrelationCounter
from simulation import Simulation

def task_4_2_1():
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    # TODO Task 4.2.1: Your code goes here
    tiacc= TimeIndependentAutocorrelationCounter(max_lag=5)

    #sequence 1:
    seq_len=10

    for i in range(seq_len):
        tiacc.count((-1)**i)
    print("Sequence: ", tiacc.x.values)
    for lag in range(1,tiacc.max_lag+1):
        print("Lag",lag,"; Auto Cor: ", tiacc.get_auto_cor(lag))
    tiacc.reset()

    print("-"*80)
    count=0
    for i in range(seq_len):
        if count==2:
            tiacc.count(-1)
            count=0
        else:
            tiacc.count(1)
            count+=1
    print("Sequence: ", tiacc.x.values)
    for lag in range(1, tiacc.max_lag+1):
        print("Lag",lag,"; Auto Cor: ", tiacc.get_auto_cor(lag))


def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    # TODO Task 4.3.1: Your code goes here
    sim=Simulation()
    sim.sim_param.S=10000
    sim.sim_param.SIM_TIME=10000000
    print('Results for simulation time of 10000s')
    for rho in [0.01,0.5,0.8, 0.9]:
        sim.sim_param.RHO= rho
        sim.reset()
        sim.do_simulation()
        print("Rho", rho)
        print("Correlation IAT_WT", sim.counter_collection.cnt_iat_wt.get_cor())
        print("Correlation IAT_ServT", sim.counter_collection.cnt_iat_st.get_cor())
        print("Correlation IAT_SysUtilT", sim.counter_collection.cnt_iat_syst.get_cor())
        print("Correlation ServT_SysT", sim.counter_collection.cnt_st_syst.get_cor())
        print("AutoCorrelation WT")
        for lag in range(1,sim.counter_collection.acnt_wt.max_lag+1):
            print('Lag:', lag, '; Auto Cor: ', sim.counter_collection.acnt_wt.get_auto_cor(lag))
        print('--'*80)


def task_4_3_2():
    """
    Exercise to plot the scatter plot of (a) IAT and serving time, (b) serving time and system time
    The scatter plot helps to better understand the meaning of bit/small covariance/correlation.
    For every rho, two scatter plots are needed.
    The simulation parameters are the same as in task_4_3_1()
    """
    # TODO Task 4.3.2: Your code goes here
    pass


def task_4_3_3():
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the waiting time is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.01 and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    # TODO Task 4.3.3: Your code goes here
    


if __name__ == '__main__':
    task_4_2_1()
    task_4_3_1()
    task_4_3_2()
    task_4_3_3()
