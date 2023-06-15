import os
import re

def extract_experiment_id(filename):
    pattern = r"train_(\d+)"
    match = re.search(pattern, filename)
    
    if match is not None:
        return match.group(1)  # return the first group that matches
    else:
        return None



def search_logs(directory):
    results = {}

    for filename in os.listdir(directory):
        experiment_id = extract_experiment_id(filename)
        with open(os.path.join(directory, filename), 'r') as file:
            for line in file:
                if "Early stop" in line:
                    ema_line = "stop"
                    normal_line = "stop"
                    break
                    
                if "Acc@1" in line and "Test: Epoch:" in line:
                    pattern = r"Test: Epoch: (\d+)"
                    match = re.search(pattern, line)
                    epoch = int(match.group(1))
                    if "EMA" in line:
                        ema_line = line.strip()
                    else:
                        normal_line = line.strip()

        if experiment_id in results:
            if epoch > results[experiment_id][0]:
                results[experiment_id] = (epoch, normal_line, ema_line)
        else:
            results[experiment_id] = (epoch, normal_line, ema_line)

    
    for key in sorted(results.keys()):
        print(key, results[key][0], results[key][1], results[key][2])


search_logs('/home/jiachen/Workspace/logs')
