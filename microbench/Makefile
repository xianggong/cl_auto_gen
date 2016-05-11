AMDAPPSDKROOT=/opt/AMDAPP
M2S_ROOT=/home/xgong/multi2sim-4.2

MIX_MEM_COUNT=1
MAX_MEM_COUNT=10
MIX_ALU_COUNT=1
MAX_ALU_COUNT=20
MIN_GLB_SIZE=1024
MAX_GLB_SIZE=65536
MIN_LCL_SIZE=64
MAX_LCL_SIZE=256

SI_CONF=$(M2S_ROOT)/samples/southern-islands/7970/si-config
MEM_CONF=$(M2S_ROOT)/samples/southern-islands/7970/mem-config

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

run_trace:
	m2s --si-sim detailed --si-config $(SI_CONF) --mem-config \
	$(MEM_CONF) --trace $(GLB_SZ)_$(LCL_SZ)_$(MEM_LEN)_$(ALU_LEN).gz \
	--mem-report mem_$(GLB_SZ)_$(LCL_SZ)_$(MEM_LEN)_$(ALU_LEN).rpt \
	--si-report si_$(GLB_SZ)_$(LCL_SZ)_$(MEM_LEN)_$(ALU_LEN).rpt \
	microbench memalum$(MEM_LEN)c$(ALU_LEN).bin $(GLB_SZ) $(LCL_SZ) --output

#$(GLOBAL_SZ) $(LOCAL_SZ)

run:
	global_size=$(MIN_GLB_SIZE); while [[ $$global_size -le $(MAX_GLB_SIZE) ]]; do \
		local_size=$(MIN_LCL_SIZE); while [[ $$local_size -le $(MAX_LCL_SIZE) ]]; do \
			for mem_count in $(MEM_SEQ); do \
				for alu_count in $(ALU_SEQ); do \
				$(MAKE) run_trace MEM_LEN=$$mem_count ALU_LEN=$$alu_count GLB_SZ=$$global_size LCL_SZ=$$local_size ; \
				done; \
			done; \
			((local_size = local_size * 2)); \
		done; \
	((global_size = global_size * 2)); \
	done

clean:
	rm -rf microbench microbench.c *.s *.bin *.gz *.rpt
