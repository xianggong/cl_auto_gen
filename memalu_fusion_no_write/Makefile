include ../env.conf

MIN_MEM_COUNT=1
MAX_MEM_COUNT=10
MIN_ALU_COUNT=1
MAX_ALU_COUNT=20
MIN_MEM_DIST=0
MAX_MEM_DIST=$(MAX_ALU_COUNT)
MIN_GLB_SIZE=1024
MAX_GLB_SIZE=65536
MIN_LCL_SIZE=64
MAX_LCL_SIZE=256

SI_CONF=$(M2S_ROOT)/samples/southern-islands/7970/si-config
MEM_CONF=$(M2S_ROOT)/samples/southern-islands/7970/mem-config

MEM_SEQ=$(shell seq $(MIN_MEM_COUNT) $(MAX_MEM_COUNT))
ALU_SEQ=$(shell seq $(MIN_ALU_COUNT) $(MAX_ALU_COUNT))
DST_SEQ=$(shell seq $(MIN_MEM_DIST) $(MAX_MEM_DIST))

all: microbench.c microbench kernels

microbench.c: microbench_kernel.conf
	$(PWD)/hostgen.py $^ > microbench.c

microbench: microbench.c
	$(CC) $(CFLAGS) $^ -o $@ -lm -lrt -pthread -l:libm2s-opencl.a -ldl

kernels:
	for mem_count in $(MEM_SEQ); do \
		for alu_count in $(ALU_SEQ); do \
			for mem_dist in $(DST_SEQ); do \
				$(PWD)/kernelgen.py --output memalu $$mem_count $$alu_count $$mem_dist; \
			done \
		done \
	done
	$(M2S_BIN)/m2c --si2bin *.s

condor:
	echo "Executable = $(M2S_BIN)/m2s" > submit
	$(PWD)/condorgen.py \
	$(MIN_GLB_SIZE) $(MAX_GLB_SIZE) $(MIN_LCL_SIZE) $(MAX_LCL_SIZE) \
	$(MIN_MEM_COUNT) $(MAX_MEM_COUNT) $(MIN_ALU_COUNT) $(MAX_ALU_COUNT) \
	$(MIN_MEM_DIST) $(MAX_MEM_DIST) \
	$(SI_CONF) $(MEM_CONF) >> submit

tidy:
	mkdir -p kernel
	mv *.s *.bin kernel

clean:
	rm -rf microbench microbench.c *.s *.bin *.gz *.rpt kernel trace
