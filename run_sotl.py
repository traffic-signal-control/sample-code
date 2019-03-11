from cityflow_env import CityFlowEnv
from sotl_agent import SOTLAgent
from utility import parse_roadnet
from utility import parse_arguments

args = parse_arguments()
roadnet = 'data/{}/roadnet.json'.format(args.scenario)

## configuration for both environment and agent
config = {
    'scenario': args.scenario,
    'data': 'data/{}'.format(args.scenario),
    'roadnet': roadnet,
    'flow': 'data/{}/flow.json'.format(args.scenario),
    #'replay_data_path': 'data/frontend/web',
    'num_step': args.num_step,
    'lane_phase_info': parse_roadnet(roadnet) # get lane and phase mapping by parsing the roadnet
}

env = CityFlowEnv(config)
agent = SOTLAgent(config)

# reset initially
t = 0
env.reset()
last_action = agent.choose_action(env.get_state())

while t < config['num_step']:
    state = env.get_state()
    action = agent.choose_action(state)
    if action == last_action:
        env.step(action)
    else:
        for _ in range(env.yellow_time):
            env.step(0)  # required yellow time
            t += 1
            flag = (t >= config['num_step'])
            if flag:
                break
        if flag:
            break
        env.step(action)
    last_action = action
    t += 1
    print("Time: {}, Phase: {}, lane_vehicle_count: {}".format(state['current_time'], state['current_phase'],
                                                                       state['lane_vehicle_count']))

# log environment files
env.log()