# DataChef Interview Assignment Solution

See [assignment document](https://www.notion.so/Data-Engineers-Mini-Assignment-72092166008c4b4d94f48a4e7a9acd9c) for requirements.

## Management:

#### To start:

```Bash
make start
```

Make sure to put the hostname/IP address of the server in the `ALLOWED_HOSTS` settings key in the [settings file](webapp/webapp/settings.py).

#### To test:

```Bash
make test
```

#### To import csvs:

```Bash
make importdata
```

#### To stop:
```Bash
make stop
```

## Design:

Given the relational nature of the data, an RDBMS is used to store and query the data.
During initial development, SQLite was used. Later, after making the code stable and functional,
PostgreSQL was used to decrease query latency and allow multiple backend processes to run simultaneously, easily.

Django was chosen as backend framework, as I had some exposure to it in the past and it made a lot of the work simpler.
The django application is run by gunicorn workers and is reverse proxied by nginx, which also serves the static content (i.e., banner images).

The results of the database queries are cached to speed up the process. I chose Memcached for this purpose, as it can also be shared between multiple backend processes.
This change increased the request per second rate from ~70 to ~230 on my computer.

All of these are dockerized to allow easy and predictable setup and running of the backend server.

The ingestion/loading of the data is done through django's ORM and is written as a django management command.
See [importdata](webapp/campaigns/management/commands/importdata.py).



## Each request goes through this pipeline:

- Current period is determined based on the current time. (Server-timezone dependent.)
- The requested campaign ID is extracted from the URL.
- The ID of the last banner served to that client is extracted from request cookies.
- An SQL query is run against the database to determine candidate banners to show for that period and campaign.
The result of the query is cached, and a cache lookup is done before querying the database.
- One of the candidate banners except the last banner served to that client for that campaign is chosen at random.
- A simple HTML page is rendered and served, showing the chosen banner.

## Benchmark:

### On my desktop:

<details>
<summary>5K requests</summary>

```Bash
❯ ab -n 5000 -c 32 http://localhost/campaigns/1/
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 500 requests
Completed 1000 requests
Completed 1500 requests
Completed 2000 requests
Completed 2500 requests
Completed 3000 requests
Completed 3500 requests
Completed 4000 requests
Completed 4500 requests
Completed 5000 requests
Finished 5000 requests


Server Software:        nginx/1.17.10
Server Hostname:        localhost
Server Port:            80

Document Path:          /campaigns/1/
Document Length:        189 bytes

Concurrency Level:      32
Time taken for tests:   20.633 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      2675000 bytes
HTML transferred:       945000 bytes
Requests per second:    242.33 [#/sec] (mean)
Time per request:       132.051 [ms] (mean)
Time per request:       4.127 [ms] (mean, across all concurrent requests)
Transfer rate:          126.61 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       3
Processing:    17  131  18.6    130     198
Waiting:       16  131  18.6    130     198
Total:         18  132  18.6    130     199

Percentage of the requests served within a certain time (ms)
  50%    130
  66%    138
  75%    143
  80%    147
  90%    156
  95%    164
  98%    172
  99%    178
 100%    199 (longest request)

```

</details>

<details>

<summary>50K requests</summary>

```Bash
❯ ab -n 50000 -c 32 http://localhost/campaigns/1/
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        nginx/1.17.10
Server Hostname:        localhost
Server Port:            80

Document Path:          /campaigns/1/
Document Length:        189 bytes

Concurrency Level:      32
Time taken for tests:   215.099 seconds
Complete requests:      50000
Failed requests:        0
Total transferred:      26750000 bytes
HTML transferred:       9450000 bytes
Requests per second:    232.45 [#/sec] (mean)  -> 3m 35s
Time per request:       137.664 [ms] (mean)
Time per request:       4.302 [ms] (mean, across all concurrent requests)
Transfer rate:          121.45 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   7.4      0    1163
Processing:    11  137  43.6    132     657
Waiting:       11  137  43.5    131     657
Total:         12  137  44.1    132    1296

Percentage of the requests served within a certain time (ms)
  50%    132
  66%    142
  75%    150
  80%    156
  90%    180
  95%    218
  98%    263
  99%    293
 100%   1296 (longest request)

```

</details>

* An Apple iMac, with 16 GB 2400 MHz DDR4 memory, and a 3.5 GHz Quad-Core Intel Core i5 CPU. 

### On my server:

<details>
<summary>5K requests</summary>

```Bash
$ ab -n 5000 -c 32 http://localhost/campaigns/1/
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 500 requests
Completed 1000 requests
Completed 1500 requests
Completed 2000 requests
Completed 2500 requests
Completed 3000 requests
Completed 3500 requests
Completed 4000 requests
Completed 4500 requests
Completed 5000 requests
Finished 5000 requests


Server Software:        nginx/1.17.10
Server Hostname:        localhost
Server Port:            80

Document Path:          /campaigns/1/
Document Length:        189 bytes

Concurrency Level:      32
Time taken for tests:   51.952 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      2675000 bytes
HTML transferred:       945000 bytes
Requests per second:    96.24 [#/sec] (mean)
Time per request:       332.491 [ms] (mean)
Time per request:       10.390 [ms] (mean, across all concurrent requests)
Transfer rate:          50.28 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   1.3      0      22
Processing:   239  331  83.2    319    1783
Waiting:      238  331  83.1    318    1781
Total:        239  331  83.9    319    1803

Percentage of the requests served within a certain time (ms)
  50%    319
  66%    331
  75%    340
  80%    347
  90%    369
  95%    390
  98%    514
  99%    722
 100%   1803 (longest request)

```

</details>

* A QEMU managed Linux VM, With 1 GB memory, and one 2GHz VCore CPU.

#### Notes:

* The benchmark was done using the ApacheBench tool and is done on only one campaign.
This can make the results different from real-world data about requests hitting various campaigns.
Yet, this won't make the performance go lower than 5000 RPM, as there are at ~50 campaigns in the provided data,
and it takes the cache about 2 seconds to warm up for every one of them.
(Assuming ~25 rps when they all miss the cache.)

* Results will vary based on hardware and configurations and tunings.
For example, if the program is run on a powerful server, increasing the number of gunicorn workers will help.


---

### Future work:

- Add bulk data import.
- Add cache warmup sequence.
