#!/usr/bin/python
""" OpenCL device microbench kernel generator """
import argparse
import os


def get_snippet(path):
    """Get snippet source string"""
    current_file_dir = os.path.dirname(__file__)
    absolute_path = os.path.join(current_file_dir, path)
    with open(absolute_path) as src:
        return src.read()


class TestMix(object):
    """TestMix generates kernels to test mem and alu"""

    def __init__(self, kernel_name, mem_count, alu_count, mem_dist):
        self.__kernel_name = kernel_name
        self.__mem_count = mem_count
        self.__alu_count = alu_count
        self.__mem_dist = mem_dist

    def get_asm(self):
        """Get assembly """
        src = get_snippet("snippet/kernel_main.txt")
        src = src.replace("KERNEL_NAME", self.__kernel_name)
        alu = get_snippet("snippet/kernel_alu_inst.txt")
        mem = get_snippet("snippet/kernel_mem_inst.txt")
        alu_inst_list = []
        mem_inst_list = []
        for mem_count in xrange(self.__mem_count):
            reg = str(mem_count + 1)
            mem_inst_list.append(mem.replace("REG", reg))
            for alu_count in xrange(self.__alu_count):
                alu_inst_list.append(alu.replace("REG", reg))
        # Insert MEM instructions based on distant
        mix_src = ''
        # mem_dist_count = 0
        mem_inst_index = 0
        alu_inst_index = 0
        while alu_inst_index < len(alu_inst_list) and mem_inst_index < len(mem_inst_list):
            mix_src += mem_inst_list[mem_inst_index]
            mem_inst_index += 1
            count = 0
            while count < self.__mem_dist:
                mix_src += alu_inst_list[alu_inst_index]
                alu_inst_index += 1
                count += 1
        while alu_inst_index < len(alu_inst_list):
            mix_src += alu_inst_list[alu_inst_index]
            alu_inst_index += 1
        src = src.replace('MIX_INSTS', mix_src)
        return src


def main():
    """OpenCL device microbench kernel generator"""
    parser = argparse.ArgumentParser(
        description='OpenCL device microbench kernel generator')
    parser.add_argument('name', metavar='name', nargs=1,
                        help='Name of kernel')
    parser.add_argument('mem', metavar='mem', nargs=1, type=int,
                        help='MEM instruction count')
    parser.add_argument('alu', metavar='alu', nargs=1, type=int,
                        help='ALU instruction count')
    parser.add_argument('memdist', metavar='memdist', nargs=1, type=int,
                        help='MEM instruction distant')
    parser.add_argument('--output', '-o', action='store_true',
                        help='Output to file')
    args = parser.parse_args()

    kernel_name = args.name[0]
    mem_count = args.mem[0]
    alu_count = args.alu[0]
    mem_dist = args.memdist[0]
    if mem_dist > alu_count:
        return
    file_name = kernel_name + 'm' + \
        str(mem_count) + 'c' + str(alu_count) + 'd' + str(mem_dist) + '.s'
    asm = TestMix(kernel_name, mem_count, alu_count, mem_dist).get_asm()
    if args.output:
        output = open(file_name, "w+")
        output.write(asm)
        output.close()

    else:
        print asm


if __name__ == '__main__':
    main()
