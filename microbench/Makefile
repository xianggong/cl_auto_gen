AMDAPPSDKROOT=/home/xgong/Develop/amdappsdk291/AMDAPPSDK-2.9-1
M2S_ROOT=/home/xgong/Develop/multi2sim

MIX_MEM_COUNT=1
MAX_MEM_COUNT=10
MIX_ALU_COUNT=1
MAX_ALU_COUNT=20

MEM_SEQ=$(shell seq $(MIN_MEM_COUNT) $(MAX_MEM_COUNT))
ALU_SEQ=$(shell seq $(MIN_ALU_COUNT) $(MAX_ALU_COUNT))

M2S_BIN=$(M2S_ROOT)/bin
M2S_LIB=$(M2S_ROOT)/lib/.libs/
CC=gcc
CFLAGS = -std=c99 -m32 -L $(M2S_LIB) -I $(AMDAPPSDKROOT)/include/

all: microbench.c microbench kernels

microbench.c: microbench_kernel.conf
	hostgen.py $^ > microbench.c

microbench: microbench.c
	$(CC) $(CFLAGS) $^ -o $@ -lm -lrt -pthread -l:libm2s-opencl.a -ldl

kernels:
	for mem_count in $(MEM_SEQ); do \
		for alu_count in $(ALU_SEQ); do \
			kernelgen.py --output memalu $$mem_count $$alu_count; \
		done \
	done
	m2c --si2bin *.s

clean:
	rm -rf microbench microbench.c *.s *.bin
