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

    def __init__(self, kernel_name, mem_count, alu_count):
        self.__kernel_name = kernel_name
        self.__mem_count = mem_count
        self.__alu_count = alu_count

    def get_asm(self):
        """Get assembly """
        src = get_snippet("snippet/kernel_main.txt")
        src = src.replace("KERNEL_NAME", self.__kernel_name)
        alu = get_snippet("snippet/kernel_alu_inst.txt")
        mem = get_snippet("snippet/kernel_mem_inst.txt")
        mix_src = ''
        for mem_count in xrange(self.__mem_count):
            mix_src += mem
            if mem_count != self.__mem_count:
                mix_src += '\n'
            for alu_count in range(self.__alu_count):
                mix_src += alu + ' // alu count = ' + str(alu_count)
                if alu_count != (self.__alu_count - 1) or \
                        mem_count != (self.__mem_count - 1):
                    mix_src += '\n'
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
    parser.add_argument('--output', '-o', action='store_true',
                        help='Output to file')
    args = parser.parse_args()

    kernel_name = args.name[0]
    mem_count = args.mem[0]
    alu_count = args.alu[0]
    file_name = kernel_name + 'm' + \
        str(mem_count) + 'c' + str(alu_count) + '.s'
    asm = TestMix(kernel_name, mem_count, alu_count).get_asm()
    if args.output:
        output = open(file_name, "w+")
        output.write(asm)
        output.close()

    else:
        print asm


if __name__ == '__main__':
    main()
