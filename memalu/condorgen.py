#!/usr/bin/python
""" Condor submit script generator """
import argparse


def main():
    """ Condor submit script generator """
    parser = argparse.ArgumentParser(
        description='Condor submit script generator')
    parser.add_argument('min_glb', metavar='min_glb', nargs=1,
                        help='Min Global Size')
    parser.add_argument('max_glb', metavar='max_glb', nargs=1,
                        help='Max Global Size')
    parser.add_argument('min_lcl', metavar='min_lcl', nargs=1,
                        help='Min Local Size')
    parser.add_argument('max_lcl', metavar='max_lcl', nargs=1,
                        help='Max Local Size')
    parser.add_argument('min_mem', metavar='min_mem', nargs=1,
                        help='Min MEM instructions')
    parser.add_argument('max_mem', metavar='max_mem', nargs=1,
                        help='Max ALU instructions')
    parser.add_argument('min_alu', metavar='min_alu', nargs=1,
                        help='Min ALU instructions')
    parser.add_argument('max_alu', metavar='max_alu', nargs=1,
                        help='Max ALU instructions')
    parser.add_argument('si_conf', metavar='si_conf', nargs=1,
                        help='SI configuration file')
    parser.add_argument('mem_conf', metavar='mem_conf', nargs=1,
                        help='Mem configuration file')
    args = parser.parse_args()

    min_glb = args.min_glb[0]
    max_glb = args.max_glb[0]
    min_lcl = args.min_lcl[0]
    max_lcl = args.max_lcl[0]
    min_alu = args.min_alu[0]
    max_alu = args.max_alu[0]
    min_mem = args.min_mem[0]
    max_mem = args.max_mem[0]
    si_conf = args.si_conf[0]
    mem_conf = args.mem_conf[0]

    arg = ''
    glb = int(min_glb)
    while glb <= int(max_glb):
        lcl = int(min_lcl)
        while lcl <= int(max_lcl):
            mem = int(min_mem)
            while mem <= int(max_mem):
                alu = int(min_alu)
                while alu <= int(max_alu):
                    name = '_'.join([str(glb), str(lcl), str(mem), str(alu)])
                    arg = "Arguments = --si-sim detailed --si-config "
                    arg += si_conf
                    arg += " --mem-config " + mem_conf
                    arg += " --trace " + name + ".gz"
                    arg += " --mem-report mem_" + name + ".rpt"
                    arg += " --si-report si_" + name + ".rpt"
                    arg += " microbench memalum" + \
                        str(mem) + "c" + str(alu) + ".bin "
                    arg += str(glb) + " " + str(lcl) + "--output"
                    arg += "\nQueue\n"
                    print arg
                    alu = alu + 1
                mem = mem + 1
            lcl = lcl * 2
        glb = glb * 2


if __name__ == '__main__':
    main()
