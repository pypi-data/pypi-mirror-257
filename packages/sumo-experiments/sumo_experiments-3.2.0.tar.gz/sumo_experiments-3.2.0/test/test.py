import time

from src.sumo_experiments import Experiment
from src.sumo_experiments.preset_networks import GridNetwork, OneCrossroadNetwork
from src.sumo_experiments.traci_util import *
from src.sumo_experiments.strategies import *

import matplotlib.pyplot as plt

net = OneCrossroadNetwork()
infrastructures = net.generate_infrastructures(200, 30, 3, 50)
flows = net.generate_flows_all_directions(60 * 240, 200)
detectors = net.generate_all_detectors(20)

exp = Experiment(
    name='test',
    infrastructures=infrastructures,
    flows=flows,
    detectors=detectors
)

#min_phases_duration = {f'x{x}-y{y}': [10, 10] for y in range(6) for x in range(6)}
max_phases_duration = {f'x{x}-y{y}': None for y in range(6) for x in range(6)}
#yellow_times = {f'x{x}-y{y}': None for y in range(6) for x in range(6)}
thresholds = {f'x{x}-y{y}': 5 for y in range(6) for x in range(6)}
min_phases_duration = {f'c': 30}
#max_phases_duration = {f'c': None}
periods = {f'c': 10}
#thresholds_switch = {f'x{x}-y{y}': 100 for y in range(6) for x in range(6)}
#thresholds_force = {f'x{x}-y{y}': 10 for y in range(6) for x in range(6)}
thresholds_switch = {'c': 100}
thresholds_force = {'c': 10}
counted_vehicles = 'all'
#phases_duration = {f'x{x}-y{y}': None for y in range(6) for x in range(6)}
yellow_times = {'c': 3}
#yellow_times = {f'x{x}-y{y}': None for y in range(6) for x in range(6)}
period_durations = {'c': 5}
#period_durations = {f'x{x}-y{y}': 5 for y in range(6) for x in range(6)}


epsilons = {'c': 1}
#epsilons = {f'x{x}-y{y}': 1 for y in range(6) for x in range(6)}
epsilon_updaters = {'c': 0.999}
#epsilon_updaters = {f'x{x}-y{y}': 0.999 for y in range(6) for x in range(6)}
min_epsilons = {'c': 0.1}
#min_epsilons = {f'x{x}-y{y}': 0.01 for y in range(6) for x in range(6)}
decreasing_episodes = 30
#decreasing_episodes = {f'x{x}-y{y}': 30 for y in range(6) for x in range(6)}
episode_lengths = 60
#episode_lengths = {f'x{x}-y{y}': 60 for y in range(6) for x in range(6)}
batch_sizes = 30
#batch_sizes = {f'x{x}-y{y}': 30 for y in range(6) for x in range(6)}
gammas = {'c': 0.9}
#gammas = {f'x{x}-y{y}': 0.9 for y in range(6) for x in range(6)}
nbs_epochs = {'c': 100}
#nbs_epochs = {f'x{x}-y{y}': 100 for y in range(6) for x in range(6)}
frequences_target_network_update = {'c': 5}
#frequences_target_network_update = {f'x{x}-y{y}': 5 for y in range(6) for x in range(6)}


strategy = RL2Strategy(infrastructures,
                       detectors,
                       yellow_times=yellow_times,
                       period_durations=period_durations,
                       epsilons=epsilons,
                       epsilon_updaters=epsilon_updaters,
                       min_epsilons=min_epsilons,
                       decreasing_episode=decreasing_episodes,
                       episode_length=episode_lengths,
                       nb_not_correlated_episodes=50,
                       max_batch_size=batch_sizes,
                       gammas=gammas,
                       nbs_epochs=nbs_epochs,
                       frequences_target_network_update=frequences_target_network_update)


tw = TraciWrapper(60 * 240)# * 60 * 24)
tw.add_behavioural_function(strategy.run_all_agents)

t = time.time()

#data = exp.run_traci(tw.final_function, nb_threads=8)
data = exp.run_traci(tw.final_function, gui=True, no_warnings=True, nb_threads=8)
print(data)
plt.plot(range(len(data) // 120), data['mean_travel_time'].fillna(method='bfill').groupby(data.index // 120).mean())
plt.show()

exp.clean_files()

print(time.time() - t)




