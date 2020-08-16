from operator import itemgetter
import copy


def SJF(procs, given_switching_time):
    # dar har marhale ba peida kardan kutah tarin proce be komak min gereftan az burst time ha (duration time ha)
    # yek mored ra entekhab mikonim va ta akhar anjam shodan an proce pish miravim
    results = []
    current_time = min(procs, key=itemgetter(1))[1]
    while len(procs) != 0:
        eligibles = [(x, y, z) for x, y, z in procs if y <= current_time]
        if len(eligibles) != 0:
            chosen_proc = min(eligibles, key=itemgetter(2))
            results.append([chosen_proc[0], current_time, current_time + chosen_proc[2]])
            current_time += chosen_proc[2] + given_switching_time
            procs.remove(list(chosen_proc))
        else:
            current_time = min(procs, key=itemgetter(1))[1]
    return results


def FIFO(procs, given_switching_time):
    # be tartib anjam mishan pas ye for each mizanim ru kar ha va be tartib arrival timeshun dar list be jelo miravim
    procs = sorted(procs, key=itemgetter(1))
    results = []
    current_time = min(procs, key=itemgetter(1))[1]
    for each_proc in procs:
        results.append([each_proc[0], current_time, current_time + each_proc[2]])
        current_time += each_proc[2] + given_switching_time
    return results


def SRT(procs, given_switching_time):
    # dar srt marahel ra ghadam be ghadam ba ++ kardan clock be jelo miravim va dar har marhale tedad clock ha
    # (current_time) ra be onvan meyar dar nazar gerefte va kutah tarin process az beine process haye mojud ta zaman
    # ghal az current time ra dar nazar migirim.
    results = []
    current_time = min(procs, key=itemgetter(1))[1]
    current_proc = min(procs, key=itemgetter(1))[0]
    current_proc_start_time = min(procs, key=itemgetter(1))[1]
    done = False
    while not done:
        eligibles = [(x, y, z) for x, y, z in procs if y <= current_time and z != 0]
        if len(eligibles) != 0:
            chosen_proc = min(eligibles, key=itemgetter(2))
            if chosen_proc[0] == current_proc:
                procs = [[chosen_proc[0], chosen_proc[1], chosen_proc[2] - 1] if each == list(chosen_proc) else each for each in procs]
                current_time += 1
            else:
                previous_proc = [(x, y, z) for x, y, z in procs if x is current_proc]
                results.append([current_proc, current_proc_start_time, current_time])
                current_proc = chosen_proc[0]
                current_proc_start_time = current_time + given_switching_time
                procs = [[chosen_proc[0], chosen_proc[1], chosen_proc[2] - 1] if each == list(chosen_proc) else each for each in procs]
                current_time += given_switching_time + 1
        else:
            current_time = procs[0][1]

        done_temp = True
        for each in procs:
            if each[2] != 0:
                done_temp = False
        done = done_temp
        if done:
            results.append([current_proc, current_proc_start_time, current_time])
    return results


def RR(procs, given_switching_time, quantum_time):
    # RR mesle FIFO amal mikone ba in tafavot ke dar for each i ke ru ye list zadim harja duration bishtar az treshhold
    # ma bud zaman baghimande ra dar ghaleb proce jadid be tahe haman listi ke dar hal peimayeshash hastim add mikonim
    results = []
    procs = sorted(procs, key=itemgetter(1))
    current_time = procs[0][1]
    for each_proc in procs:
        if each_proc[2] > quantum_time:
            procs.append([each_proc[0], each_proc[1], each_proc[2] - quantum_time])
            results.append([each_proc[0], current_time, current_time + quantum_time])
            current_time += quantum_time + given_switching_time
        else:
            results.append([each_proc[0], current_time, current_time + each_proc[2]])
            current_time +=  each_proc[2] + given_switching_time
    return results


def PRIORITY(procs, given_switching_time):
    # dar in algorithm dar har marhale be proce haye mojud negahi andakhte va max priority (hamantor ke dar slide ha
    #  amade) ra entekhab mikonim
    results = []
    procs = sorted(procs, key=itemgetter(1))
    current_time = procs[0][1]
    while len(procs) != 0:
        eligibles = [(x, y, z, p) for x, y, z, p in procs if y <= current_time]
        if len(eligibles) != 0:
            chosen_proc = max(eligibles, key=itemgetter(3))
            results.append([chosen_proc[0], current_time, current_time + chosen_proc[2]])
            current_time += chosen_proc[2] + switching_time
            procs.remove(list(chosen_proc))
        else:
            current_time = procs[0][1]
    return results


def calculate(results, given_procs):
    print("GIVEN", given_procs)
    proc_info = []
    for each in given_procs:
        each_outs = [z for x, y, z in results if x <= each[0]]
        proc_info.append([each[1], each[2], max(each_outs)])

    mzen = sum([departure - burst - arrival for arrival, burst, departure in proc_info]) / len(given_procs)
    # miangin zaman entezar : majmoe (khoruj - duration - shoru) ha taghsim bar tedad
    mzej = sum([burst for arrival, burst, departure in proc_info]) / len(given_procs)
    # mianginzaman ejra : majmoe zman haye ejra bar kol tedad
    mzps = mzej + mzen
    # rabeteye kholase shode miangin zaman pasokh majmoe miangin zaman entezar va mianginzaman ejra ast
    mzbr = sum([departure - arrival for arrival, burst, departure in proc_info]) / len(given_procs)
    # miangin zaman bargasht majmoe khoruj ha - vorud hast bar tedad process ha
    throughput = (len(given_procs) / sum([start - finish for name, start, finish in results])) * -100
    # throughput haman tedad kar ha bar saniast
    utilization = (sum([start - finish for name, start, finish in results]) / results[-1][2]) * -100
    # cpu utilization ham modat zamane karkard bar kol zamane
    return [utilization, throughput, mzen, mzps, mzbr, mzej]


if __name__ == '__main__':
    while True:
        print("=" * 80)
        order = int(input("Choose the Algorithm: 1- FIFO  2- SJF  3- SRT  4- RR  5- PRIORITY  6- ALGO COMPARISON  7- Exit ==> "))
        if order == 7:
            break
        print("=" * 80)
        num_of_processes = int(input("Enter the number of processes: "))
        processes = []
        print("=" * 80)
        print("Enter a process by Name, Arrival time, Process Time (ex: A 0 5)")
        print("=" * 80)
        for i in range(num_of_processes):
            tmp = "Enter process " + str(i + 1) + ": "
            inp = input(tmp)
            if order == 5:
                proc_id, proc_arrival, proc_duration, priority = inp.split()[0], int(inp.split()[1]), int(inp.split()[2]), int(inp.split()[3])
                processes.append([proc_id, proc_arrival, proc_duration, priority])
            else:
                proc_id, proc_arrival, proc_duration = inp.split()[0], int(inp.split()[1]), int(inp.split()[2])
                processes.append([proc_id, proc_arrival, proc_duration])
        switching_time = int(input("Enter Switching Time: "))
        deep_copied_processes = copy.deepcopy(processes)
        deep_copied_processes2 = copy.deepcopy(processes)
        deep_copied_processes3 = copy.deepcopy(processes)
        deep_copied_processes4 = copy.deepcopy(processes)
        deep_copied_processes5 = copy.deepcopy(processes)
        deep_copied_processes6 = copy.deepcopy(processes)
        deep_copied_processes7 = copy.deepcopy(processes)
        final_results = None
        if order == 1:
            final_results = FIFO(processes, switching_time)
        elif order == 2:
            final_results = SJF(processes, switching_time)
        elif order == 3:
            final_results = SRT(processes, switching_time)
        elif order == 4:
            quantum_time = int(input("Enter Quantum Time: "))
            final_results = RR(processes, switching_time, quantum_time)
        elif order == 5:
            final_results = PRIORITY(processes, switching_time)

        if order != 6:
            calculations = calculate(final_results, deep_copied_processes)
            print("=" * 80)
            print("Given Processes:", deep_copied_processes)
            print("Gannt Chart:", final_results)
            print()
            print("Calculations:")
            print("CPU UTILIZATION (%):", calculations[0])
            print("THROUGHPUT (%):", calculations[1])
            print("Miangin Zaman Entezar:", calculations[2])
            print("Miangin Zaman Pasokh:", calculations[3])
            print("Miangin Zaman Bargasht:", calculations[4])
            print("Miangin Zaman Ejra:", calculations[5])
            print()
            print("=" * 80)
        else:
            # az unjai ke miangin zaman pasokh va zaman entezar bas kam bashan va bahrebari ziad, formuli
            # dorost kardam baraye moghayese ke ebteda miangin dotaye avalio migire va dar makhrej gharar mide
            # va bahrebari dar surat, ma mibinim ke harcheghadr surat bishtar va makhrej kamtar, algorithm behtar.
            FIFO_cal = calculate(FIFO(deep_copied_processes2, switching_time), deep_copied_processes3)
            FIFO_results = FIFO_cal[0] / ((FIFO_cal[3] + FIFO_cal[2]) / 2)
            SJF_cal = calculate(SJF(deep_copied_processes4, switching_time), deep_copied_processes5)
            SJF_results = SJF_cal[0] / ((SJF_cal[3] + SJF_cal[2]) / 2)
            SRT_cal = calculate(SRT(deep_copied_processes6, switching_time), deep_copied_processes7)
            SRT_results = SRT_cal[0] / ((SRT_cal[3] + SRT_cal[2]) / 2)
            comparison = [FIFO_results, SJF_results, SRT_results]
            print("Testing Results:", "FIFO", FIFO_results, "SJF", SJF_results, "SRT", SRT_results)
            if max(comparison) == comparison[0]:
                print("FIFO is the best algorithm to choose.")
            elif max(comparison) == comparison[1]:
                print("SJF is the best algorithm to choose.")
            elif max(comparison) == comparison[2]:
                print("SRT is the best algorithm to choose.")