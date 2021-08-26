# 公式法
import time
t1 = time.time()
PI = 0
N = 1e5
for n in range(int(N)):
    PI += 1/pow(16,n) * (4/(8*n+1) - 2/(8*n+4) - 1/(8*n+5) - 1/(8*n+6))
print(PI)
print(round(time.time()-t1)) # 50s
