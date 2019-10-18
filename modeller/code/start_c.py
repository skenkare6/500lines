from cffi import FFI
ffibuilder = FFI()

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("""
    int* start_where_we_exist(void);
    int* stop_where_we_exist(void);
""")

# pin tool binding start stop or pin_ss
ffibuilder.set_source("_pin_ss",
"""
    int* start_where_we_exist(void) {
        int *p  = malloc(4);
        return p;
    }
    int* stop_where_we_exist(void) {
        int *p  = malloc(4);
        return p;
    }
""",
     libraries=[])   # library name, for the linker

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)