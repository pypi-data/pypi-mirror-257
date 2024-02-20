import pandas as pd

from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import AllChem, Descriptors

def mol_normalizer(smile, mode='inchi'):
    RDLogger.DisableLog('rdApp.*')
    m = Chem.MolFromSmiles(smile)
    Chem.SanitizeMol(m)
    inchi = Chem.MolToInchi(m)
    if mode == 'smile':
        m = Chem.MolFromInchi(inchi)
        smile = Chem.CanonSmiles(Chem.MolToSmiles(m))
        return smile
    return inchi

def mol_similarity(m1, m2, mode='inchi'):
    RDLogger.DisableLog('rdApp.*')
    fpgen = AllChem.GetRDKitFPGenerator()
    if mode == 'smile':
        m1 = Chem.MolFromSmiles(m1)
        m2 = Chem.MolFromSmiles(m2)
        inchi1 = Chem.MolToInchi(m1)
        inchi2 = Chem.MolToInchi(m2)
    elif mode == 'inchi':
        m1 = Chem.MolFromInchi(m1)
        m2 = Chem.MolFromInchi(m2)
        inchi1 = Chem.MolToInchi(m1)
        inchi2 = Chem.MolToInchi(m2)
    inchi1 = inchi1.split('/')
    inchi2 = inchi2.split('/')
    c_in1 = ''
    c_in2 = ''
    length = 4
    if len(inchi1) < length or len(inchi2) < length:
        length = min(len(inchi1), len(inchi2))
    for i in range(length):
        c_in1 += inchi1[i]
        c_in2 += inchi2[i]
    if c_in1 == c_in2:
        return 1
    m1_wt = Descriptors.MolWt(Chem.RemoveHs(m1))
    m2_wt = Descriptors.MolWt(Chem.RemoveHs(m2))
    score = DataStructs.cDataStructs.TanimotoSimilarity(fpgen.GetFingerprint(m1), fpgen.GetFingerprint(m2))
    if score == 1:
        score = score - abs(m1_wt-m2_wt)/(m1_wt+m2_wt)
    return score

def smile_in_sink(smile, sink):
    fpgen = AllChem.GetRDKitFPGenerator()
    f_sink = []
    for i in sink:
        m = Chem.MolFromSmiles(i)
        f_sink.append(fpgen.GetFingerprint(m))
    m = Chem.MolFromSmiles(smile)
    f_smile = fpgen.GetFingerprint(m)
    for f in f_sink:
        if DataStructs.cDataStructs.TanimotoSimilarity(f_smile, f) == 1:
            return True
    return False

def list_smile_in_sink(smiles, sink):
    RDLogger.DisableLog('rdApp.*')
    fpgen = AllChem.GetRDKitFPGenerator()
    f_sink = []
    for i in sink:
        try:
            m = Chem.MolFromSmiles(i)
            f_sink.append(fpgen.GetFingerprint(m))
        except:
            continue
    f_smiles = []
    for i in smiles:
        try:
            m = Chem.MolFromSmiles(i)
            f_smiles.append(fpgen.GetFingerprint(m))
        except:
            continue
    in_sink = [0]*len(smiles)
    for i in range(len(f_smiles)):
        for f in f_sink:
            if DataStructs.cDataStructs.TanimotoSimilarity(f_smiles[i], f) == 1:
                in_sink[i] = 1
                break
    return in_sink