#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _Otsuka_STN_reg(void);
extern void _myions_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"Otsuka_STN.mod\"");
    fprintf(stderr, " \"myions.mod\"");
    fprintf(stderr, "\n");
  }
  _Otsuka_STN_reg();
  _myions_reg();
}

#if defined(__cplusplus)
}
#endif
