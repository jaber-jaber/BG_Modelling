#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _myions_reg();
extern void _Otsuka_STN_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," myions.mod");
fprintf(stderr," Otsuka_STN.mod");
fprintf(stderr, "\n");
    }
_myions_reg();
_Otsuka_STN_reg();
}
