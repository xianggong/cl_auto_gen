#!/usr/bin/python
""" OpenCL host program generator """
import argparse


def get_snippet(path):
    """Get snippet source string"""
    with open(path) as src:
        return src.read()


def get_host_cl_datatype(datatype):
    """Get corresponding OpenCL datatype: float -> cl_float"""
    return "cl_" + datatype


def get_host_src_prefix():
    """Get host code snippet: create program/context/device"""
    return get_snippet("snippet/clPrefix.txt")


def get_host_src_postfix():
    """Get host code snippet: release kernel/program/context/device"""
    return get_snippet("snippet/clPostfix.txt")


def get_host_buffer_create(arg_name, num_elem, host_data_type):
    """Get host code snippet: create host buffer"""
    src = get_snippet("snippet/clHostBufferCreate.txt")
    src = src.replace("ARG_NAME", arg_name)
    src = src.replace("NUM_ELEM", str(num_elem))
    src = src.replace("HOST_DATA_TYPE", host_data_type)
    return src


def get_host_buffer_init(arg_name, num_elem, host_data_type, host_init_val):
    """Get host code snippet: init host buffer"""
    src = get_snippet("snippet/clHostBufferInit.txt")
    src = src.replace("ARG_NAME", arg_name)
    src = src.replace("NUM_ELEM", str(num_elem))
    src = src.replace("HOST_DATA_TYPE", host_data_type)
    src = src.replace("HOST_INIT_VALUE", host_init_val)
    return src


def get_host_buffer_free(arg_name):
    """Get host code snippet: free host buffer"""
    src = get_snippet("snippet/clHostBufferFree.txt")
    src = src.replace("ARG_NAME", arg_name)
    return src


def get_device_buffer_create(arg_name, num_elem, host_data_type):
    """Get host code snippet: create device buffer"""
    src = get_snippet("snippet/clDeviceBufferCreate.txt")
    src = src.replace("ARG_NAME", arg_name)
    src = src.replace("NUM_ELEM", str(num_elem))
    src = src.replace("HOST_DATA_TYPE", host_data_type)
    return src


def get_device_buffer_init(arg_name, num_elem, host_data_type):
    """Get host code snippet: init/push device buffer"""
    src = get_snippet("snippet/clDeviceBufferInit.txt")
    src = src.replace("ARG_NAME", arg_name)
    src = src.replace("NUM_ELEM", str(num_elem))
    src = src.replace("HOST_DATA_TYPE", host_data_type)
    return src


def get_device_buffer_read(arg_name, num_elem, host_data_type):
    """Get host code snippet: read device buffer back to host buffer"""
    src = get_snippet("snippet/clDeviceBufferRead.txt")
    src = src.replace("ARG_NAME", arg_name)
    src = src.replace("NUM_ELEM", str(num_elem))
    src = src.replace("HOST_DATA_TYPE", host_data_type)
    return src


def get_print_host_buffer(arg_name, num_elem, host_data_type):
    """Get host code snippet: read device buffer back to host buffer"""
    src = get_snippet("snippet/clDeviceBufferRead.txt")
    src = src.replace("ARG_NAME", arg_name)
    src = src.replace("NUM_ELEM", str(num_elem))
    print_format = "f"
    if "float" in host_data_type:
        print_format = "f"
    elif "int" in host_data_type:
        print_format = "d"
    src = src.replace("PRINT_FORMAT", print_format)
    return src


def get_device_buffer_free(arg_name):
    """Get host code snippet: free device buffer"""
    src = get_snippet("snippet/clDeviceBufferFree.txt")
    src = src.replace("ARG_NAME", arg_name)
    return src


def get_program_create(kernel_file):
    """Get host code snippet: create program with source"""
    src = get_snippet("snippet/clProgramCreate.txt")
    src = src.replace("KERNEL_FILE", kernel_file)
    return src


def get_program_free():
    """Get host code snippet: create program with source"""
    src = get_snippet("snippet/clProgramFree.txt")
    return src


def get_kernel_create(kernel_name):
    """Get host code snippet: create kernel"""
    src = get_snippet("snippet/clKernelCreate.txt")
    src = src.replace("KERNEL_NAME", kernel_name)
    return src


def get_kernel_free(kernel_name):
    """Get host code snippet: free kernel"""
    src = get_snippet("snippet/clKernelFree.txt")
    src = src.replace("KERNEL_NAME", kernel_name)
    return src


def get_host_set_arg(kernel_name, arg_index, arg_size, arg_value):
    """Get host code snippet: set a single argument"""
    src = get_snippet("snippet/clSetKernelArg.txt")
    src = src.replace("KERNEL_NAME", kernel_name)
    src = src.replace("ARG_INDEX", str(arg_index))
    src = src.replace("ARG_SIZE", arg_size)
    src = src.replace("ARG_VALUE", arg_value)
    return src


def get_host_launch_kernel(kernel_name, global_work_size, local_work_size):
    """Get host code snippet: launch kernel"""
    src = get_snippet("snippet/clLaunchKernel.txt")
    src = src.replace("KERNEL_NAME", kernel_name)
    src = src.replace("GLOBAL_WORK_SIZE", global_work_size)
    src = src.replace("LOCAL_WORK_SIZE", local_work_size)
    return src


class Arg(object):
    """Arg contains information of a kernel arg"""

    def __init__(self, arg_desc):
        prop = arg_desc.split(' ')
        self.__kernel_name = prop[0]
        self.__index = prop[1]
        self.__name = prop[2]
        self.__addrspace = prop[3]
        self.__datatype = prop[4]
        self.__num_elem = prop[5]
        self.__init_val = prop[6]

    def get_create_buffers(self):
        """Create host and device buffers for this arg"""

        # If not a buffer
        if self.__addrspace == 'other':
            src = '  /* Declare variable */\n'
            src += '  ' + self.__datatype + ' device_' + self.__name
            if int(self.__num_elem) > 1:
                src += '[' + self.__num_elem + ']'
            src += ';\n\n'
            return src

        # Create host buffer
        src = get_host_buffer_create(self.__name,
                                     self.__num_elem,
                                     self.__datatype)
        # Create device buffer
        src += get_device_buffer_create(self.__name,
                                        self.__num_elem,
                                        self.__datatype)

        return src

    def get_init_buffers(self):
        """Init host and device buffers for this arg"""
        # If not a buffer
        if self.__addrspace == 'other':
            src = '  /* Init variable */\n'
            src += '  device_' + self.__name
            if int(self.__num_elem) == 1:
                src += ' = ' + self.__init_val
            src += ';\n\n'
            return src

        # Init host buffer
        src = get_host_buffer_init(self.__name,
                                   self.__num_elem,
                                   self.__datatype,
                                   self.__init_val)

        # Init device buffer
        src += get_device_buffer_init(self.__name,
                                      self.__num_elem,
                                      self.__datatype)
        return src

    def get_free_buffers(self):
        """Free host and device buffers for this arg"""

        if self.__addrspace == 'other':
            return ''

        # Free host buffer
        src = get_host_buffer_free(self.__name)

        # Free device buffer
        src += get_device_buffer_free(self.__name)

        return src

    def get_set_kernel_arg(self):
        """Set kernel arg for this arg"""
        kernel = self.__kernel_name
        arg_index = self.__index
        arg_size = None
        arg_value = None

        if self.__addrspace == 'global':
            arg_size = 'sizeof(cl_mem)'
            arg_value = '&' + self.__name + '_device_buffer'
        else:
            arg_size = 'sizeof(' + self.__datatype + ')' + \
                '*' + self.__num_elem
            if self.__addrspace == 'local':
                arg_value = 'NULL'
            else:
                arg_value = '&device_' + self.__name

        src = get_host_set_arg(kernel, arg_index, arg_size, arg_value)
        return src


class Kernel(object):
    """Kernel"""

    def __init__(self, name, global_work_size, local_work_size):
        self.__name = name
        self.__global_work_size = global_work_size
        self.__local_work_size = local_work_size
        self.__args = []

    def set_args(self, arg_prop_list):
        """Set list of argument"""
        for prop in arg_prop_list:
            self.__args.append(Arg(prop))

    def get_name(self):
        """Get name of kernel"""
        return self.__name

    def get_args(self):
        """Get list of argument object"""
        return self.__args

    def get_kernel_create(self):
        """Create this kernel"""
        return get_kernel_create(self.__name)

    def get_kernel_free(self):
        """Free this kernel"""
        return get_kernel_free(self.__name)

    def get_kernel_buffers_create(self):
        """Created host and device buffers for this kernel"""
        src = ''
        for arg in self.__args:
            src += arg.get_create_buffers()
        return src

    def get_kernel_buffers_init(self):
        """Init host and device buffers for this kernel"""
        src = ''
        for arg in self.__args:
            src += arg.get_init_buffers()
        return src

    def get_kernel_buffers_free(self):
        """Free host and device buffers for this kernel"""
        src = ''
        for arg in self.__args:
            src += arg.get_free_buffers()
        return src

    def get_kernel_set_args(self):
        """Set args for this kernel"""
        src = get_snippet('snippet/clSetKernelArgs.txt')
        src_set_kernel_args = ''
        for arg in self.__args:
            src_set_kernel_args += arg.get_set_kernel_arg()
        src = src.replace('SET_KERNEL_ARGS', src_set_kernel_args)
        return src

    def get_kernel_launch(self):
        """Launch this kernel"""
        # Set dim and launch
        src = get_host_launch_kernel(self.__name,
                                     str(self.__global_work_size),
                                     str(self.__local_work_size))
        return src


class OpenCLHostProgram(object):
    """OpenCL host program"""

    def __init__(self, conf_file):
        self.__kernel_file = None
        self.__kernels = []
        self.__parse_conf(conf_file)

    def __parse_conf(self, conf_file):
        conf_src = ''
        with open(conf_file) as conf:
            conf_src = conf.readlines()

        arg_prop_list = []
        arg_count = 0
        for line in conf_src:
            line = line.replace('\n', '')
            if '#' in line:
                continue
            elif 'KERNEL' in line:
                prop = line.replace('KERNEL ', '').split(' ')
                self.__kernel_file = prop[0]
                kernel_name = prop[1]
                global_work_size = prop[2]
                local_work_size = prop[3]
                kernel = Kernel(kernel_name, global_work_size, local_work_size)
                self.__kernels.append(kernel)
            elif 'ARG' in line:
                prop = line.replace('ARG ', '')
                kernel_name = self.__kernels[-1].get_name()
                arg_index = str(len(arg_prop_list))
                arg_prop = kernel_name + ' ' + arg_index + ' '
                arg_prop += prop
                arg_prop_list.append(arg_prop)
                arg_count += 1
            elif 'END' in line:
                self.__kernels[-1].set_args(arg_prop_list)
                arg_count = 0
                arg_prop_list[:] = []

    def get_src_code(self):
        """Get host program source code"""
        src = get_host_src_prefix()

        src += get_program_create(self.__kernel_file)

        for kernel in self.__kernels:
            src += kernel.get_kernel_create()
            src += kernel.get_kernel_buffers_create()
            src += kernel.get_kernel_buffers_init()

            src += kernel.get_kernel_set_args()
            src += kernel.get_kernel_launch()

            src += kernel.get_kernel_buffers_free()
            src += kernel.get_kernel_free()

        src += get_program_free()

        src += get_host_src_postfix()
        return src


def main():
    """OpenCL host program generator"""
    parser = argparse.ArgumentParser(
        description='OpenCL host program generator')
    parser.add_argument('progdesc', metavar='p', nargs=1,
                        help='program description file')
    args = parser.parse_args()

# arg = Arg('matmul 0 matA global float 10 1.0')
# print arg.get_create_buffers()
# print arg.get_init_buffers()
# print arg.get_set_kernel_arg()

# arg_prop_list = []
# arg_prop_list.append('matmul matA 0 global float 10 1.0')
# kernel = Kernel('matmul', 1024, 128, arg_prop_list)
# print kernel.get_kernel_create()

    program = OpenCLHostProgram(args.progdesc[0])
    print program.get_src_code()

if __name__ == '__main__':
    main()
