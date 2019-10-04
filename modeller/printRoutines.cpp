
// Adapted partially from
// https://reverseengineering.stackexchange.com/questions/20289/how-to-get-per-function-memory-accesses-using-pin-toolrese.cpp
#include "pin.H"
#include <iostream>


VOID Routine(RTN rtn, VOID *v) {
    RTN_Open(rtn);

    std::cout << RTN_Name(rtn) << std::endl;

    RTN_Close(rtn);
}

INT32 Usage() {
    std::cerr << "This Pintool prints the routines being read" << std::endl;
    std::cerr << std::endl << KNOB_BASE::StringKnobSummary() << std::endl;
    return -1;
}

int main(int argc, char *argv[]) {

    std::cout << "Hello - are we compiling.";

    PIN_InitSymbols();

    if (PIN_Init(argc, argv))
        return Usage();

    RTN_AddInstrumentFunction(Routine, 0);

    PIN_StartProgram();

    return 0;
}