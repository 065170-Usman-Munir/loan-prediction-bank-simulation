"""
Bank Queue Simulation (M/M/c queueing model) using SimPy.
- Poisson arrivals (rate lambda), exponential service times (rate mu)
- c parallel tellers, FIFO queue
Collects waiting times, queue length over time, teller utilization.
"""
import simpy, random, numpy as np, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
random.seed(42); np.random.seed(42)

class BankSim:
    def __init__(self, env, n_tellers, service_mean):
        self.env=env; self.tellers=simpy.Resource(env,capacity=n_tellers)
        self.service_mean=service_mean
        self.wait_times=[]; self.queue_log=[]; self.busy_time=0.0; self.n_tellers=n_tellers
        self.served=0
    def service(self, cust):
        t=random.expovariate(1.0/self.service_mean)
        yield self.env.timeout(t); self.busy_time+=t
    def customer(self, name):
        arrive=self.env.now
        self.queue_log.append((self.env.now,len(self.tellers.queue)))
        with self.tellers.request() as req:
            yield req
            self.wait_times.append(self.env.now-arrive)
            yield self.env.process(self.service(name)); self.served+=1

def source(env, sim, arrival_mean):
    i=0
    while True:
        yield env.timeout(random.expovariate(1.0/arrival_mean))
        i+=1; env.process(sim.customer(f'C{i}'))

def run(n_tellers=3, arrival_mean=4.0, service_mean=10.0, sim_time=480):
    env=simpy.Environment(); sim=BankSim(env,n_tellers,service_mean)
    env.process(source(env,sim,arrival_mean)); env.run(until=sim_time)
    util=sim.busy_time/(n_tellers*sim_time)
    return {
      'avg_wait':round(np.mean(sim.wait_times),2) if sim.wait_times else 0,
      'max_wait':round(np.max(sim.wait_times),2) if sim.wait_times else 0,
      'served':sim.served,'utilization':round(util,3),
      'wait_times':sim.wait_times,'queue_log':sim.queue_log,'n_tellers':n_tellers}

def make_plots(res, outdir):
    times=[t for t,_ in res['queue_log']]; qlen=[q for _,q in res['queue_log']]
    plt.figure(figsize=(10,4)); plt.plot(times,qlen,color='teal',lw=1)
    plt.title('Queue Length Over Time'); plt.xlabel('Time (min)'); plt.ylabel('Customers waiting')
    plt.tight_layout(); plt.savefig(f'{outdir}/sim_queue_length.png'); plt.close()

    plt.figure(figsize=(9,4)); plt.hist(res['wait_times'],bins=25,color='coral',edgecolor='k',alpha=.8)
    plt.axvline(res['avg_wait'],color='navy',ls='--',label=f"Avg={res['avg_wait']} min")
    plt.title('Customer Waiting Time Distribution'); plt.xlabel('Wait (min)'); plt.ylabel('Count')
    plt.legend(); plt.tight_layout(); plt.savefig(f'{outdir}/sim_waiting_time.png'); plt.close()

    # Utilization across teller configs
    configs=[1,2,3,4,5]; utils=[run(n_tellers=c)['utilization'] for c in configs]
    plt.figure(figsize=(8,4)); plt.bar([str(c) for c in configs],utils,color='mediumseagreen',edgecolor='k')
    plt.title('Teller Utilization vs Number of Tellers'); plt.xlabel('Tellers'); plt.ylabel('Utilization')
    plt.ylim(0,1); plt.tight_layout(); plt.savefig(f'{outdir}/sim_utilization.png'); plt.close()

if __name__=='__main__':
    ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    S=os.path.join(ROOT,'screenshots')
    res=run()
    print(f"Served={res['served']} | Avg wait={res['avg_wait']} min | "
          f"Max wait={res['max_wait']} min | Utilization={res['utilization']}")
    make_plots(res,S); print("Simulation plots saved.")
