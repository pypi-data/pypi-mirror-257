F$MTBF (Mean time between failures) Test
===========

Mean Time Between Failure (MTBF) is a measure of the reliability of a hardware product, component or system.
(http://en.wikipedia.org/wiki/Mean_time_between_failures)

JIO OS leverages this measurement to perform stability testing to identify issues resulting in system failure, crash or hang after running for a long period of time.

# Environment
1. Linux-like operating system. Ubuntu 18+ LTS is recommended.
2. Python 3
3. virtualenv & pip

# MTBF Mode
JIO OS MTBF platform supports three mode:
1. dynamic mode:
```
Define a test set containing test cases and the weight of each case. It will randomly choose a test case with the given weight to run MTBF.
```
2. replay mode
```
Replay a test list.
```
3. sequential mode
```
A list define the running sequence of all test cases and the loop times of each case. It will run each case with the defined loop times and then go to the next case.
```

# MTBF Formula

### Radisys fomula
Based on these numbers and test device amount, we can calculate our final MTBF time.
```
MTBF time = sum(MTBF TIME of each device) / [sum(MTBF Crash Times of each device) + test device amount]
```
For example, we have 2 devices and have below output. We can get final MTBF time is '16603.470' sec.
```
Device A:
  MTBF TIME=49513.217 sec
  MTBF Crash Times=3
Device B:
  MTBF TIME=99918.010 sec
  MTBF Crash Times=4

  MTBF time = (49513.217+99918.010) / [(3+4) + 2] = 16603.470
```

### Industrial fomula
This could be a reference data on specific branch for better communication between partners.

MTBF = (sum(Test time of each device) / (0.5*CHIINV(1-CONFIDENCE LEVEL, 2*(CRASH+FREEZE+1))))

CONFIDENCE LEVEL = 0.95

Consider probability distribution by leveraging "chi-square distribution".

# Installation
1. Please clone the whole 'test-frameworks' repository.
2. Install virtualenv and activate it.
```
$ virtualenv .mtbf
$ . .mtbf/bin/activate
```
3. Run 'python setup.py develop' to install all 3rd party dependencies, sonar and gaia-ui-tests.
```
(.mtbf)$ python setup.py develop
```
4. Then, you have 'mtbftest' command in this virtual environment.

# Configurations
MTBF needs two configuration files. Please update them accordingly.
```
1. mtbf_template.json: to config what whole MTBF run needs. e.g. how many testing devices are used.
2. testvars_device-serial.json: to config required data for a target device. Each device should have a corresponding testvars.
   Its file name is like 'testvars_abcde642.json' which 'abcde642' is the serial number of target device.
```

Settings in mtbf_template.json
```
{
  "workspace": "/tmp/workspace",
  "mode": {
    "value": "dynamic",
    "dynamic": {
      "file": "/Users/hermesc/workspace-kai/test-frameworks/mtbf-tests/mtbftests/conf/list/common_usercases.list",
      "duration": "1h10m"
    },
    "replay": "/Users/hermesc/workspace-kai/test-frameworks/mtbf-tests/mtbftests/replay_template.txt",
    "sequential_loop": "/Users/hermesc/workspace-kai/test-frameworks/mtbf-tests/mtbftests/sequential_loop_template.txt"
  },
  "devices": [
    {
      "serial": "",
      "port": "",
      "logcat": false,
      "top": false,
      "procrank": false,
      "rootdir": "gaiatest",
      "archive_folder": "output",
      "test_log": "file"
    }
  ]
}
```

- workspace: where we put running data and collecting reports for each device.
- mode:
  - value: define what mode you want to test. Accepted value: "dynamic", "replay", and "sequential_loop".
  - dynamic: if your mode is 'dynamic', you need to specify this section.
```
    * file : define all tests to be performed. Use absolute path
      * Default test list is defined in 'conf/list/*.list'. Create a new list for different cases combination. You can put the same case multiple times, and it would be run with higher weight.
        Please see current case propotion design for each list in MTBF_test_case_propotion.xlsx
        (https://git.kaiostech.com/QA/case/blob/master/MTBF/MTBF_test_case_propotion.xlsx)
    * duration: duration of test. e.g., 1d = 1 days, 20h = 20 hours, 30S = 30 seconds, 120m = 120 minutes. Can be mixed.
```
  - replay : if your mode is 'replay', you need to specify a replay file which contains a test case list with a specific sequence.
  - sequential_loop : if your mode is 'sequential_loop', you need to specify a sequential file which contains a test case list with a specific sequence and repeated times.
```
{"sequential":
 [["/Users/hermesc/workspace-kai/test-frameworks/mtbf-tests/mtbftests/gaiatest/tests/mtbf/clock/test_mtbf_timer_set.py", "20"],
  ["/Users/hermesc/workspace-kai/test-frameworks/mtbf-tests/mtbftests/gaiatest/tests/mtbf/clock/test_mtbf_stopwatch_reset.py", "30"]
]}
```

- devices: an array which contains all target devices info.
  - serial: device serial number, which can be retrieved by the command 'adb devices'. This value must be unique.
  - port: the communication port used for this device. The value must be unique.
  - logcat: enable logcat during test run.
  - top: enable top log collection during test run. Its cost is high, so don't enable it unless for debugging.
  - procrank: enable procrank log collection during test run. Default is disable unless specific debugging case required.
  - rootdir: indicate search path of test case bank. For now, only accept 'gaiatest'.
  - archive_folder: output & archive folder under workspace.
  - test_log: file descriptor of output. The value can be 'file' or 'stdout'. Default is 'stdout'. If set to 'file', the output file path is $workspace/$archive_folder/test_log.txt.

# Execution
Please enter your virtualenv and then perform command like this.
```
(.mtbf)$ mtbftest --conf mtbftests/conf/mtbf_template.json
```


# MTBF Result Review Process
__This is only for dynamic mode.__

### Analyze result

Open test_log.txt under workspace set in mtbf.json. Result can be two types:
* Normal case
 * Time's up based on duration setting in mtbf.json
 * All test case failed in one test run
* Exceptional case
 * Device reboot, power off causing adb drop unexpectedly

#### Normal case
At the bottom of of test_log.txt, it will have summary of total running time. Check if it's finished because of reach duration or all case failed in last cycle, e.g.
```
SUMMARY
-------
2017-08-28 16:26:57.264929: passed: sing0
2017-08-28 16:26:57.265042: failed: 48
2017-08-28 16:26:57.265132: todo: 0
2017-08-28 16:26:57.265311: SUITE-END | took 2130s
```

#### Exceptional case
* Debug fail reason from last passed case to the end of test_log.txt
* Find if any 'PowerOff' word in logcat log of final days.
```
grep -w PowerOff logcat20180502*
If power off event triggered, similar result will be outputed:
05-02 15:05:12.799   302   302 I PowerManagerService: Call to virtual nsresult mozilla::dom::power::PowerManagerService::PowerOff().
```
* Check if device is enter dload mode or stuck

#### Count crash/b2g nubmers
No matter normal or exceptional cases, always check crash or b2g restart bug for MTBF result calculation.
* B2g restart
 * Check how many time b2g PID changes each day
```
grep -w b2g b2ginfo20180502*

From outpu, colum 3 and 5 means PID and CPU time, device is restarted
b2ginfo201805082320:            b2g   301    1 54112.1    0 169.6 174.3 191.4 55.7 553.4   0         0 root
b2ginfo201805082325:            b2g   301    1 54251.1    0 178.7 183.2 199.9 55.7 555.5   0         0 root
b2ginfo201805082330:            b2g   301    1 54410.3    0 179.3 184.0 199.6 58.2 562.7   0         0 root
b2ginfo201805082335:            b2g   301    1 54608.3    0 175.1 179.6 196.4 57.9 555.6   0         0 root
b2ginfo201805082340:            b2g   301    1 54777.5    0 183.3 187.6 204.1 56.6 557.3   0         0 root
b2ginfo201805082350:            b2g  302    1   60.9    0 82.1 90.2 114.7  0.0 282.6   0         0 root

```
* Crash
 * A crash folder will be found in output folder means crash occurs. Each folder inside it means one crash
 * adb shell and ls to check all dmp files are generated within test duration /data/b2g/mozilla/Crash\ Reports/pending/
 * When crash happens, b2g PID might change as well. So when sum restart and crash numbers, need to minus duplicated one
 
#### tombstones
When device encounters unexpected crash or hang issues, there might be tombstones files generated and saved in device. Capture it and attach to bug can provide more information to developer.
```
adb shell
cd /data/tombstones

If ther are files named "tombstones0x", adb pull all of them for related bugs.
```

### Calculate result
With mtbf_calculator.sh, you can get first and last test case pass time and total hours information.
```
script can be found under /mtbf-tests/mtbftests/utils

./mtbf_calculator.sh <path>/test_log.txt
```
For internal dashboard result update, please run parsing_mtbf_data.py in QA/handytools repository


# MTBF Script Pass Rate Review
Script might need to be updated over time as build changes. By using mtbf_count_pass_and_failed_case.sh, it can display all cases pass and fail number. Tester can review cases with highest failure rate.
```
script can be found under /mtbf-tests/mtbftests/utils

./mtbf_count_pass_and_failed_case.sh test_log.txt ./test-frameworks/mtbf-tests/mtbftests/conf/list/<common_usercases.list used for test> <path>/test_log.txt
```
