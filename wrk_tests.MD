# Performance Test Comparison

| Metric          | Without Redis            | With Redis                |
|-----------------|--------------------------|---------------------------|
| Duration        | 30s                      | 30s                       |
| Threads         | 4                        | 4                         |
| Connections     | 100                      | 100                       |
| Avg Latency     | 108.71ms                 | 26.94ms                   |
| Latency Stdev   | 94.38ms                  | 10.90ms                   |
| Max Latency     | 1.02s                    | 352.78ms                  |
| Latency > Stdev | 90.35%                   | 93.09%                    |
| Avg Req/Sec     | 272.08                   | 940                       |
| Req/Sec Stdev   | 171.85                   | 121.89                    |
| Max Req/Sec     | 810                      | 1.22k                     |
| Req/Sec > Stdev | 68.96%                   | 72.08%                    |
| Total Requests  | 31,596                   | 113,138                   |
| Total Data Read | 7.05MB                   | 28.92MB                   |
| Requests/sec    | 1051.23                  | 3759.07                   |
| Transfer/sec    | 240.22KB                 | 960KB                     |