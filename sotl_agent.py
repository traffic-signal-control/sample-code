class SOTLAgent():
    ''' Agent using Fixed-time algorithm to control traffic signal
        '''

    def __init__(self, config):
        self.config = config
        self.lane_phase_info = config['lane_phase_info']  # "intersection_1_1"

        self.intersection_id = list(self.lane_phase_info.keys())[0]
        self.phase_list = self.lane_phase_info[self.intersection_id]["phase"]
        self.phase_startLane_mapping = self.lane_phase_info[self.intersection_id]["phase_startLane_mapping"]

        self.phi = 20
        self.min_green_vehicle = 20
        self.max_red_vehicle = 30

        self.action = self.phase_list[0]

    def choose_action(self, state):
        cur_phase = state["current_phase"]
        if state["current_phase_time"] >= self.phi:
            num_green_vehicle = sum([state["lane_waiting_vehicle_count"][i] for i in self.phase_startLane_mapping[cur_phase]])
            num_red_vehicle = sum([state["lane_waiting_vehicle_count"][i] for i in self.lane_phase_info[self.intersection_id]["start_lane"]]) - num_green_vehicle
            if num_green_vehicle <= self.min_green_vehicle and num_red_vehicle > self.max_red_vehicle:
                self.action = cur_phase % len(self.phase_list) + 1
        return self.action
