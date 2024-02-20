# LTPDrop

LTPDrop is a command line Python program designed to act as a filter bewteen two LTP Engines, it enables to filter/log specifics LTP Segments. LTPDrop can be used to:
1) Deterministically drop a given number of time one (or more) LTP segments based on his type or on some of its attributes
2) Randomically drop LTP segments with a given probability
3) Log LTP sessions <br>
The current version of this program (0.1.6) is compatible with [LTP RFC-5326](https://datatracker.ietf.org/doc/rfc5326/) and [Multicolor LTP](https://datatracker.ietf.org/doc/rfc5326/)


## Table of Contents

[Installation](#installation) <br>
[Setup](#setup) <br>
[Usage](#usage) <br>

<a name="installation"/>

## Installation

To install simply type in the command line 
```bash
$ git clone https://gitlab.com/unibo-dtn/ltpdrop
```
<a name="setup"/>

## Setup

There are 3 different setups depending on where LTPDrop is ran: it can be ran on the same machine of the session receiver, or on the machine of the session generator, or on a completely different machine. To describe the different setups it is used the terminology used by [ION](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/interplanetary-overlay-network/). In the following examples all the different possibles arguments to modify the network topology are used. The engine number of the session originator must be specified, all LTP segments that are not part of a session started by the generator will be discarded.

### Receiver Side
![alt-text](images/setup1.png "Receiver Side")<br>
__Session originator__: outduct 10.0.0.12:1114, induct 0.0.0.0:1113 <br>
__Session receiver__: outduct loopback:1114, induct loopback:1113 <br>
```bash
$ python3 LTPDrop.py -e 1
```
### Generator Side
![alt-text](images/setup2.png "Generator Side")<br>
__Session originator__: outduct loopback:1115, induct loopback:1113 <br>
__Session receiver__: outduct 10.0.0.11:1115, induct 0.0.0.0.1113 <br>
```bash
$ python3 LTPDrop.py -e 1 --ltpdrop_port 1115 --session_rcv 10.0.0.12:1113 
```

### Middle Ground
![alt-text](images/setup3.png "Middle Ground")<br>
__Session originator__: outduct 10.0.0.26:1115, induct 0.0.0.0:1115 <br>
__Session receiver__: outduct 10.0.0.26:1115, induct 0.0.0.0:1113 <br>
```bash
$ python3 LTPDrop.py -e 1 --ltpdrop_port 1115 --session_gen 10.0.0.11:1116 --session_rcv 10.0.0.12:1113 
```

<a name="usage"/>

## Usage

In the underlying examples it is used a "Receiver Side" setup. This application does not take into account different sessions.

### Drop specific segments
1) Drop of the two first segments containing a CP
```bash
$ python3 LTPDrop.py -e 1 --drop_CP 2
```
2) Drop of the first CP segment containing a Red EOB
```bash
$ python3 LTPDrop.py -e 1 --drop_RD_CP_EORP_EOB 1
```
3) Drop of one RS segment and two RA segments
```bash
$ python3 LTPDrop.py -e 1 --drop_RS 1 --drop_RA 2
```
For more option check the help command
```bash
$ python3 LTPDrop.py -h
```

### Drop random segments
To implement this function the Python [random](https://docs.python.org/3/library/random.html) module is used, which implements a mersenne twister.
1) Drop 15% of segments
```bash
$ python3 LTPDrop.py -e 1 --random 15
```
2) Drop 20% of segments, using a seed for the random number generator
```bash
$ python3 LTPDrop.py -e 1 --random 20 --seed 26032002
```

### LTP Sessions Logs
1) Disable logs to Stdout and write a copy to a file
```bash
$ python3 LTPDrop.py -e 1 -n --write-logs logs.txt
```
2) Print logs to csv file(this function logs all segment that arrive to LTPDrop, also those segment that get dropped)
```bash
$ python3 LTPDrop.py -e 1 --csv logs.csv
```


