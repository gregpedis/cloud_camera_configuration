import os
import time
import sys


def parse_args():
    assert len(sys.argv)>=3, "Pass Sleep Interval and Flushing as parameters"
    assert float(sys.argv[1])>=0.2, "Sleep Interval must be at least 0.2"

    interval = float(sys.argv[1])
    flush = int(sys.argv[2]) == 1
    return interval, flush


def show_temperature(interval, flush):
    while True:
        result = os.popen("vcgencmd measure_temp").readline()
        result = str(result[5:-1])

        if (flush):
            sys.stdout.write("\r" + result)
            sys.stdout.flush()
        else:
            print(f"Temperature is {result}")
            sys.stdout.flush()

        time.sleep(interval)


def main():
    interval, flush = parse_args()
    show_temperature(interval, flush)


if __name__ == "__main__":
    main()

