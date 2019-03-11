import engine
from sim_setting import sim_setting_control
from utility import parse_arguments
import pandas as pd

args = parse_arguments()
num_step = args.num_step
eng = engine.Engine(sim_setting_control["interval"],
                    sim_setting_control["threadNum"],
                    sim_setting_control["saveReplay"],
                    sim_setting_control["rlTrafficLight"],
                    sim_setting_control["changeLane"])
roadnetFile = "data/{}/roadnet.json".format(args.scenario)
flowFile = "data/{}/flow.json".format(args.scenario)
planFile = "data/{}/signal_plan.txt".format(args.scenario)
eng.load_roadnet(roadnetFile)
eng.load_flow(flowFile)
plan = pd.read_csv(planFile, sep="\t", header=0, dtype=int)
intersection_id = plan.columns[0]

for step in range(num_step):
    phase = int(plan.loc[step])
    eng.set_tl_phase(intersection_id, phase)  # set traffic light of intersection_id to phase (phases of intersection is defined in roadnetFile)
    eng.next_step()

    current_time = eng.get_current_time()                      # return a double, time past in seconds
    lane_vehicle_count = eng.get_lane_vehicle_count()                # return a dict, {lane_id: lane_count, ...}
    lane_waiting_vehicle_count = eng.get_lane_waiting_vehicle_count()        # return a dict, {lane_id: lane_waiting_count, ...}
    lane_vehicles = eng.get_lane_vehicles()                     # return a dict, {lane_id: [vehicle1_id, vehicle2_id, ...], ...}
    vehicle_speed = eng.get_vehicle_speed()                     # return a dict, {vehicle_id: vehicle_speed, ...}
    vehicle_distance = eng.get_vehicle_distance()                  # return a dict, {vehicle_id: vehicle_distance, ...}

    print("Time: {}, Phase: {}, lane_vehicle_count: {}".format(current_time, phase, lane_vehicle_count))