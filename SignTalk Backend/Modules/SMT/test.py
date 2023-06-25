# Test the SMT
from smt import SMT

smt = SMT()

aslg = smt.forward_translate('the girl is in france')
print(aslg)

en = smt.backward_translate(aslg)
print(en)

aslg = smt.forward_translate('the girl in france')
print(aslg)

en = smt.backward_translate(aslg)
print(en)