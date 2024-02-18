import numpy as np
import numpy.typing as npt
from typing import Annotated, Literal, TypeVar

DType = TypeVar("DType", bound=np.generic)
Array3 = Annotated[npt.NDArray[DType], Literal[3]]
Array3x3 = Annotated[npt.NDArray[DType], Literal[3, 3]]

# set some constants (migrate these to separate file)
AUTOA    = 0.529177249
RYTOEV   = 13.605826
HARTREE  = 27.211386024367243
CLIGHT   = 137.037          # speed of light in a.u.
EVTOJ    = 1.60217733E-19
AMTOKG   = 1.6605402E-27
BOLKEV   = 8.6173857E-5
BOLK     = BOLKEV * EVTOJ
EVTOKCAL = 23.06

PI     = 3.141592653589793238
TPI    = 2 * PI
CITPI  = 1j * TPI
FELECT = 2 * AUTOA * RYTOEV
EDEPS  = 4 * PI * 2 * RYTOEV * AUTOA
HSQDTM = RYTOEV * AUTOA * AUTOA