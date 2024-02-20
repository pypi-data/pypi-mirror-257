from multiprocessing import Process,cpu_count


def mp_iterator(function_array,arguments = []):
    processes = []

    for i in range(len(function_array)):
        if arguments[i]:
            args = arguments[i]
        else:
            args = ()
        process = Process(target=function_array[i],args = args)
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

