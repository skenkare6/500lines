
// https://reverseengineering.stackexchange.com/questions/20289/how-to-get-per-function-memory-accesses-using-pin-tool
// rese.cpp
#include "pin.H"
#include <iostream>
// #include <map>

// typedef long long LL;
// typedef pair<int, int> pii;

// #define forup(i, a, b) for (int i = (a); i < (b); ++i)
// #define fordn(i, a, b) for (int i = (a); i > (b); --i)
// #define rep(i, a) for (int i = 0; i < (a); ++i)

// #define fs first
// #define sc second

// #define pb push_back
// #define mp make_pair

// map<string, vector<pair<UINT64, UINT64>>> RtnToRead;

// VOID RecordMemRead(ADDRINT address, UINT64 memOp, string rname) {
//     RtnToRead[rname].pb(mp(address, memOp));
// }

VOID Routine(RTN rtn, VOID *v) {

    RTN_Open(rtn);

    std::cout << RTN_Name(rtn) << std::endl;

    // for (INS ins = RTN_InsHead(rtn); INS_Valid(ins); ins = INS_Next(ins)) {

    //     UINT32 memOperands = INS_MemoryOperandCount(ins);
    //     for (UINT32 memOp = 0; memOp < memOperands; memOp++) {
    //         if (INS_MemoryOperandIsRead(ins, memOp)) {
    //             INS_InsertPredicatedCall(ins, IPOINT_BEFORE,
    //                                      (AFUNPTR)RecordMemRead, IARG_INST_PTR,
    //                                      IARG_MEMORYOP_EA, memOp, IARG_PTR,
    //                                      new string(name), IARG_END);
    //         }
    //     }
    // }

    RTN_Close(rtn);
}

// VOID Fini(INT32 code, VOID *v) {
//     for (auto &rtn : RtnToRead) {
//         cout << rtn.fs << " :" << endl;
//         for (auto &e : rtn.second) {
//             cout << "\t" << hex << e.fs << " : " << e.sc << endl;
//         }
//     }
// }

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

    // PIN_AddFiniFunction(Fini, 0);

    PIN_StartProgram();

    return 0;
}