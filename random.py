"""Generate random numbers
random.py

Tool for generating random numbers.

Description:

  random.py <iterations> <output> [options]

Arguments:

-a, --alternate
  Experimental, use alternate algorithm. Defaults to a Linear Congruential Generator.

-c, --cursor-mode
  Use cursor movement as seed.

-i, --iterations
  Specify number of iterations. 100,000 by default.

-o, --output-file
  Specify an output file for generated random numbers. Outputs to stdout by default.

-x, --screen-mode
  Use desktop screenshot noise as seed.

TODO:
Implement arg parsing
Screen noise based / cursor movement based seed as base for new algorithm

"""

import os, sys, subprocess;
from datetime import timedelta, datetime

def usage():
  print "Usage: %s <iterations> <output>" % os.path.basename(sys.argv[0])

def get_seed():
  # Get system uptime to use as the seed
  if sys.platform.startswith('win'):
    process = subprocess.Popen('net statistics server', stdout=subprocess.PIPE)
    output, err = process.communicate()
    output = output.splitlines()

    for line in output:
      if "Statistics since" in line:
        uptime = line

    uptime = uptime.split(" ")

    ## Sadly, the fact that Python's DateTime doesn't understand non zero-padded minutes ruined this oneliner for me :/
    # date = datetime.strptime(" ".join(uptime[2:]), "%m/%d/%y %H:%M:%S %p")

    date, ptime, meridian = uptime[2:]

    time = []

    for unit in ptime.split(':'):
      time.append(unit.zfill(2))

    time = ":".join(time)

    date = datetime.strptime(" ".join([date, time, meridian]), "%m/%d/%Y %H:%M:%S %p")

    uptime = datetime.now() - date

    return uptime.total_seconds()

  else:
    with open('/proc/uptime', 'r') as f:
      uptime_seconds = float(f.readline().split()[0])
      uptime_seconds = timedelta(seconds = uptime_seconds)
      uptime = datetime.now() - uptime_seconds

      return uptime.total_seconds()

def lcg(seed):
  # Preset numbers obtained from a TRUE random number generator. 
  # https://www.random.org/integers/?num=1&min=-999999&max=999999&col=1&base=10&format=html&rnd=new
  return (229633 * seed + -556694) % 77598

def main():
  # First, a proven but cryptographically insecure algorithm. (Linear congruential generator)
  # Fast, but not necessarily very random.

  args = sys.argv[1:]
  if "-h" in args or "--help" in args:
    usage()
    sys.exit(2)

  iterations = int(args[0]) if len(args) > 0 else 100000

  for i in xrange(iterations):
    seed = get_seed()
    print lcg(seed)

if __name__ == '__main__':
  main()