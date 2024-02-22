import sys
import os

SUPPORTED_CALLERS = {"aldy", "cyrius", "pypgx", "stargazer", "stellarpgx"}
BAD_GENOTYPES = {
    "None",
    "./.",
    "Indeterminate",
    "Indeterminate/Indeterminate",
    "",
    "No_call",
}
ALLELE_FXN_PATH = os.path.join(
    os.path.dirname(sys.modules[__name__].__file__), "allele_fxn.csv"
)
