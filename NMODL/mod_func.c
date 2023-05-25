#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _Destexhe_AMPA_reg();
extern void _Destexhe_GABAa_reg();
extern void _myions_reg();
extern void _Otsuka_STN_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," Destexhe_AMPA.mod");
fprintf(stderr," Destexhe_GABAa.mod");
fprintf(stderr," myions.mod");
fprintf(stderr," Otsuka_STN.mod");
fprintf(stderr, "\n");
    }
_Destexhe_AMPA_reg();
_Destexhe_GABAa_reg();
_myions_reg();
_Otsuka_STN_reg();
}
