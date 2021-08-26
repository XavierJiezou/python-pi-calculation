[简体中文](README.zh.md) | English
# Introduction
Implementation for calculating the value of π based on Python.
# Method
## Monte Carlo
![](monte_carlo.png)
There is an inscribed circle in the square of 1 × 1. Randomly scatter points into the square area (the total number of scattered points is recorded as `S`). For each point, the probability of falling in the circle is: $\frac {\pi \cdot 0.5^2}{1×1}=0.25\pi$，After the scatter ends, count the number of points it falls in the circle, and write it down as N.

In general, with the increase in the number of experiments, the frequency will be close to the probability. 
When the number of experiments tends to be infinite, the limit of frequency is probability.

Therefore, when `S` is large enough, we can simply think: $0.25\pi=\frac{N}{S}$，namely $\pi=\frac{4N}{S}$.

**Tips:** How to judge the point is inside the circle? Calculate the Euclidean distance from the point to the center of the circle. The smaller the radius is inside the circle, and the larger the radius is outside the circle.
```python
S = 1e6
N = 0
for i in range(int(S)):
    x = random.random()
    y = random.random()
    d = (x-0.5)**2+(y-0.5)**2
    if d <= 0.5**2:
        N += 1
    else:
        pass
PI = 4*N/S
print(PI)
```
## Formula
$$
\pi = \sum_{n=0}^\infty [\frac{1}{16^n}(\frac{4}{8n+1}-\frac{2}{8n+4}-\frac{1}{8n+5}-\frac{1}{8n+6})]
$$
```python
PI = 0
N = 1000
for n in range(int(N)):
    PI += 1/pow(16,n) * (4/(8*n+1) - 2/(8*n+4) - 1/(8*n+5) - 1/(8*n+6))
print(PI)
```
# Multi-Process
| max_workers of ProcessPool | Time (Evaluate 10 times, unit: second) | 
|:--:|:--:|
| 1 | 53.55±1.98 |
| 2 | 42.17±1.49 |
| 4 | 28.01±0.77 |
| 8 | 21.73±0.51 |
| 16 | **19.93±0.48** |
| 32 | 20.51±0.37 |
| 61 | 22.65±0.84 |

**Tips:** The maximum number of processes in the process pool must be less than or equal to 61, otherwise an exception will be raised.
```python
import concurrent.futures as cf
from tqdm import tqdm
import os


class CalculatePI(object):
    """Calculate the value of π by multi process

    Args:
        num_iterations (int): Number of iterations. Default: 100000
        max_workers (int): Maximum number of processes. Default: the number of processors on the machine.
    """

    def __init__(self, num_iterations: int = 100000, max_workers: int = os.cpu_count()) -> None:
        """Initialization

        Args:
            num_iterations (int): Number of iterations. Default: 100000
            max_workers (int): Maximum number of processes. Default: the number of processors on the machine.
        """
        self.num_iterations = num_iterations
        self.max_workers = max_workers

    def __calc__(self, start: int, end: int) -> float:
        """Calculate the value of π according to formula

        Args:
            start (int): Starting value for the iterations
            end (int): Ending value for the iterations

        Returns:
            float: Value of π
        """
        PI = 0
        for n in tqdm(range(start, end)):
            PI += 1/pow(16, n) * (4/(8*n+1) - 2 / (8*n+4) - 1/(8*n+5) - 1/(8*n+6))
        return PI

    def __main__(self) -> float:
        """Calulate the value of π by multi process

        Returns:
            float: Value of π
        """
        PI = 0
        with cf.ProcessPoolExecutor(self.max_workers) as p:
            futures = []
            for i in range(self.max_workers):
                start = i*self.num_iterations//self.max_workers
                end = (i+1)*self.num_iterations//self.max_workers
                futures.append(p.submit(self.__calc__, start, end))
            for future in cf.as_completed(futures):
                PI += future.result()
        return PI


if __name__ == '__main__':
    print(CalculatePI().__main__())
```
# Reference
> [https://baike.baidu.com/item/圆周率/139930](https://baike.baidu.com/item/%E5%9C%86%E5%91%A8%E7%8E%87/139930)