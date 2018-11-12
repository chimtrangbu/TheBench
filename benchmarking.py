#!/usr/bin/env python3
import subprocess
import argparse
import resource
import cProfile
import pstats


def take_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", nargs='+', help="src_file")
    parser.add_argument("-t", '--time', action='store_true')
    parser.add_argument("-m", '--memory', action='store_true')
    parser.add_argument("-n", '--numfunc', action='store_true')
    args = parser.parse_args()
    return args


# join allfile to run like : ./a ./b (instead of running a, running a & b)
def launch_file(src_file):
    file = ' '.join(args.src)
    run_file = subprocess.run([file], shell=True)


def option_of_file():
    #  export resource of target file used
    resource_consumed_child = resource.getrusage(resource.RUSAGE_CHILDREN)
    if args.memory:
        # export memory
        memory_child = resource_consumed_child.ru_maxrss
        # print('Memory usage: ' + str(memory_child) + ' KB' )
        print('Memory usage: %0.0f' % memory_child + ' KB')
    if args.numfunc:
        src = args.src[0]
        compile_target_file = compile(open(src, "rb").read(), src, 'exec')
        pr = cProfile.Profile()
        pr.enable()
        pr.run(compile_target_file)
        pr.disable()
        # sort_stats to sort ncalls
        ps = pstats.Stats(pr).sort_stats('calls')
        # src[2:] if my program = ./smart_db.py , it'll get smart_db.py
        # find in field "filename:lineno(function)" to get func of smart_db.py
        ps.print_stats(src[2:])
    else:
        # export time of user
        # export time of system
        # total time
        run_time_child = resource_consumed_child.ru_utime
        run_sys_time = resource_consumed_child.ru_stime
        total_time = run_time_child + run_sys_time
        print('run-time:', run_time_child)


if __name__ == '__main__':
    args = take_args()
    launch_file(args.src)
    option_of_file()
