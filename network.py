import os

tr_dir = "results/tr/"
tcl_file = "network.tcl"
types = ["Newreno", "Tahoe", "Vegas"]
n_run = 10

received = []
dropped = []
enqueued = []
dequeued = []
cwnd = []
rtt = []


def execAllRuns():
    for each in types:
        for i in range (1, n_run + 1):
            command = "ns " + tcl_file + " " + each + " " + str(i) + " false"
            print(command)
            os.system(command)


def readAndParseAllData():
    for type_ in types:
        for i in range(1, n_run + 1):
            file = open(tr_dir + type_ + str(i) + ".tr", 'r')
            lines = file.readlines()

            for line in lines:
                if "cwnd_" in line:
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    cwnd.append(splt)
                elif "rtt_" in line:
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    rtt.append(splt)
                elif line[0] == '+':
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    enqueued.append(splt)
                elif line[0] == '-':
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    dequeued.append(splt)
                elif line[0] == 'r':
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    received.append(splt)
                elif line[0] == 'd':
                    splt = line.split()
                    splt.append(type_)
                    splt.append(i)
                    dropped.append(splt)
                

def calculateAvgRtt():
    global rtt
    newreno_f1 = []
    newreno_f2 = []
    tahoe_f1 = []
    tahoe_f2 = []
    vegas_f1 = []
    vegas_f2 = []
    curr_vals = [0] * n_run
    rtt = sorted(rtt) # sort by time
    # for each in rtt:
    #     print(each)
    #     print("\n")
    for each in rtt:
        time_ = float(each[0])
        rtt_ = float(each[6])
        src = int(each[1])
        type_ = each[7]
        run_id = int(each[len(each) - 1])
        curr_vals[run_id - 1] = rtt_
        avg = sum(curr_vals) / len(curr_vals)
        if type_ == "Newreno":
            newreno_f1.append([time_, avg]) if (src == 0) else newreno_f2.append([time_, avg])
        elif type_ == "Tahoe":
            tahoe_f1.append([time_, avg]) if (src == 0) else tahoe_f2.append([time_, avg])
        else:
            vegas_f1.append([time_, avg]) if (src == 0) else vegas_f2.append([time_, avg])
    
    newreno_result = []
    newreno_result.append(newreno_f1)
    newreno_result.append(newreno_f2)
    tahoe_result = []
    tahoe_result.append(tahoe_f1)
    tahoe_result.append(tahoe_f2)
    vegas_result = []
    vegas_result.append(vegas_f1)
    vegas_result.append(vegas_f2)

    return newreno_result, tahoe_result, vegas_result


def calculateAvgCwnd():
    global cwnd
    newreno_f1 = []
    newreno_f2 = []
    tahoe_f1 = []
    tahoe_f2 = []
    vegas_f1 = []
    vegas_f2 = []
    curr_vals = [0] * n_run
    cwnd = sorted(cwnd) # sort by time
    # for each in cwnd:
    #     print(each)
    #     print("\n")
    for each in cwnd:
        time_ = float(each[0])
        cwnd_ = float(each[6])
        src = int(each[1])
        type_ = each[7]
        run_id = int(each[len(each) - 1])
        curr_vals[run_id - 1] = cwnd_
        avg = sum(curr_vals) / len(curr_vals)
        if type_ == "Newreno":
            newreno_f1.append([time_, avg]) if (src == 0) else newreno_f2.append([time_, avg])
        elif type_ == "Tahoe":
            tahoe_f1.append([time_, avg]) if (src == 0) else tahoe_f2.append([time_, avg])
        else:
            vegas_f1.append([time_, avg]) if (src == 0) else vegas_f2.append([time_, avg])
    
    newreno_result = []
    newreno_result.append(newreno_f1)
    newreno_result.append(newreno_f2)
    tahoe_result = []
    tahoe_result.append(tahoe_f1)
    tahoe_result.append(tahoe_f2)
    vegas_result = []
    vegas_result.append(vegas_f1)
    vegas_result.append(vegas_f2)

    return newreno_result, tahoe_result, vegas_result


def calculateAvgDropped():
    global dropped
    newreno_f1 = []
    newreno_f2 = []
    tahoe_f1 = []
    tahoe_f2 = []
    vegas_f1 = []
    vegas_f2 = []
    curr_vals = [0] * n_run
    dropped = sorted(dropped) # sort by time
    # for each in dropped:
    #     print(each)
    #     print("\n")
    for each in dropped:
        time_ = float(each[1])
        flow_id = int(each[7])
        type_ = each[len(each) - 2]
        run_id = int(each[len(each) - 1])
        curr_vals[run_id - 1] += 1
        avg = sum(curr_vals) / len(curr_vals)
        if type_ == "Newreno":
            newreno_f1.append([time_, avg]) if (flow_id == 1) else newreno_f2.append([time_, avg])
        elif type_ == "Tahoe":
            tahoe_f1.append([time_, avg]) if (flow_id == 1) else tahoe_f2.append([time_, avg])
        else:
            vegas_f1.append([time_, avg]) if (flow_id == 1) else vegas_f2.append([time_, avg])
    
    newreno_result = []
    newreno_result.append(newreno_f1)
    newreno_result.append(newreno_f2)
    tahoe_result = []
    tahoe_result.append(tahoe_f1)
    tahoe_result.append(tahoe_f2)
    vegas_result = []
    vegas_result.append(vegas_f1)
    vegas_result.append(vegas_f2)

    return newreno_result, tahoe_result, vegas_result


if __name__ == '__main__':
    execAllRuns()
    readAndParseAllData()

    # each list below is 3d : [flows][records][fields]
    rtt_newreno_result, rtt_tahoe_result, rtt_vegas_result = calculateAvgRtt()
    cwnd_newreno_result, cwnd_tahoe_result, cwnd_vegas_result = calculateAvgCwnd()
    drp_newreno_result, drp_tahoe_result, drp_vegas_result = calculateAvgDropped()