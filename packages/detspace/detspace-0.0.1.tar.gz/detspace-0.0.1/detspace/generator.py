import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import Descriptors
from Filtro.standardizer import Standardizer

from utils import mol_normalizer

def generator(smile, r, filename, ec_num, leg_id):
    RDLogger.DisableLog('rdApp.*')
    a=Standardizer()
    m=Chem.MolFromSmiles(smile)
    Chem.SanitizeMol(m)
    mol1 = a.sequence_rr_legacy(m)
    mol2 = Chem.AddHs(m)
    mol = [mol1, mol2]
    
    prod = []
    res = []
    for mm in mol:
        for i in range(len(r)):
            try:
                pr = r[i].RunReactants((mm,))
                if len(pr) > 0:
                    m = pr[0][0]
                    p = mol_normalizer(Chem.MolToSmiles(m), mode='smile')
                    for j in p.split('.'):
                        m = Chem.MolFromSmiles(j)
                        if Descriptors.MolWt(m) <= 1000:
                            prod.append(j)
                            res.append(j+'$'+smile+'$'+leg_id[i]+'$'+ec_num[i])
            except:
                continue
    res = list(dict.fromkeys(res))
    res = pd.DataFrame(res, columns=['Resultado'])
    res.to_csv(filename, mode='a')
    return prod
