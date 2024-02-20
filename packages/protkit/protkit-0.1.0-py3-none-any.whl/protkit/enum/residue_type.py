from enum import Enum


class ResidueType(Enum):
    ALA = 1,
    ARG = 2,
    ASN = 3,
    ASP = 4,
    CYS = 5,
    GLN = 6,
    GLU = 7,
    GLY = 8,
    HIS = 9,
    ILE = 10,
    LEU = 11,
    LYS = 12,
    MET = 13,
    PHE = 14,
    PRO = 15,
    SER = 16,
    THR = 17,
    TRP = 18,
    TYR = 19,
    VAL = 20,
    # ASX = 21,
    # GLX = 22,
    # UNK = 23,
    # ACE = 24,
    # NH2 = 25,
    # HIE = 26,
    # HID = 27,
    # HIP = 28,
    # CYX = 29,
    # CAS = 30,
    # PCA = 31,
    # HYP = 32,
    # TPO = 33,


class ResidueLookup:
    # Peptide bond length and standard deviation in Angstroms.
    PEPTIDE_BOND_LENGTH = (1.336, 0.23)

    # Peptide bond length cutoff in Angstroms. If the expected
    # bond length of 1.336 Angstroms is off by more than this
    # cutoff, then the bond is considered to be broken.
    PEPTIDE_BOND_LENGTH_CUTOFF = 0.2

    HEAVY_ATOMS = {
        "ALA": {"N", "CA", "C", "O", "CB"},
        "ARG": {"N", "CA", "C", "O", "CB", "CG", "CD", "NE", "CZ", "NH1", "NH2"},
        "ASN": {"N", "CA", "C", "O", "CB", "CG", "OD1", "ND2"},
        "ASP": {"N", "CA", "C", "O", "CB", "CG", "OD1", "OD2"},
        "CYS": {"N", "CA", "C", "O", "CB", "SG"},
        "GLU": {"N", "CA", "C", "O", "CB", "CG", "CD", "OE1", "OE2"},
        "GLN": {"N", "CA", "C", "O", "CB", "CG", "CD", "OE1", "NE2"},
        "GLY": {"N", "CA", "C", "O"},
        "HIS": {"N", "CA", "C", "O", "CB", "CG", "ND1", "CD2", "CE1", "NE2"},
        "ILE": {"N", "CA", "C", "O", "CB", "CG1", "CG2", "CD1"},
        "LEU": {"N", "CA", "C", "O", "CB", "CG", "CD1", "CD2"},
        "LYS": {"N", "CA", "C", "O", "CB", "CG", "CD", "CE", "NZ"},
        "MET": {"N", "CA", "C", "O", "CB", "CG", "SD", "CE"},
        "PHE": {"N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "CE1", "CE2", "CZ"},
        "PRO": {"N", "CA", "C", "O", "CB", "CG", "CD"},
        "SER": {"N", "CA", "C", "O", "CB", "OG"},
        "THR": {"N", "CA", "C", "O", "CB", "OG1", "CG2"},
        "TRP": {"N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "NE1", "CE2", "CE3", "CZ2", "CZ3", "CH2"},
        "TYR": {"N", "CA", "C", "O", "CB", "CG", "CD1", "CD2", "CE1", "CE2", "CZ", "OH"},
        "VAL": {"N", "CA", "C", "O", "CB", "CG1", "CG2"}
    }

    HYDROGEN_ATOMS = {
        "ALA": {"H", "HA", "HB1", "HB2", "HB3"},
        "ARG": {"H", "HA", "HB2", "HB3", "HG2", "HG3", "HD2", "HD3", "HE", "HH11", "HH12", "HH21", "HH22"},
        "ASN": {"H", "HA", "HB2", "HB3", "HD21", "HD22"},
        "ASP": {"H", "HA", "HB2", "HB3", "HD2"},
        "CYS": {"H", "HA", "HB2", "HB3", "HG"},
        "GLU": {"H", "HA", "HB2", "HB3", "HG2", "HG3", "HE2"},
        "GLN": {"H", "HA", "HB2", "HB3", "HG2", "HG3", "HE21", "HE22"},
        "GLY": {"H", "HA", "HA2", "HA3"},
        "HIS": {"H", "HA", "HB2", "HB3", "HD1", "HD2", "HE1", "HE2"},
        "ILE": {"H", "HA", "HB", "HG12", "HG13", "HG21", "HG22", "HG23", "HD11", "HD12", "HD13"},
        "LEU": {"H", "HA", "HB2", "HB3", "HG", "HD11", "HD12", "HD13", "HD21", "HD22", "HD23"},
        "LYS": {"H", "HA", "HB2", "HB3", "HG2", "HG3", "HD2", "HD3", "HE2", "HE3", "HZ1", "HZ2", "HZ3"},
        "MET": {"H", "HA", "HB2", "HB3", "HG2", "HG3", "HE1", "HE2", "HE3"},
        "PHE": {"H", "HA", "HB2", "HB3", "HD1", "HD2", "HE1", "HE2", "HZ"},
        "PRO": {"H", "HA", "HB2", "HB3", "HG2", "HG3", "HD2", "HD3"},
        "SER": {"H", "HA", "HB2", "HB3", "HG"},
        "THR": {"H", "HA", "HB", "HG1", "HG21", "HG22", "HG23"},
        "TRP": {"H", "HA", "HB2", "HB3", "HD1", "HE1", "HE3", "HZ2", "HZ3", "HH2"},
        "TYR": {"H", "HA", "HB2", "HB3", "HD1", "HD2", "HE1", "HE2", "HH"},
        "VAL": {"H", "HA", "HB", "HG11", "HG12", "HG13", "HG21", "HG22", "HG23"}
    }

    SHORT_CODE = {
        "ALA": "A",
        "CYS": "C",
        "ASP": "D",
        "GLU": "E",
        "PHE": "F",
        "GLY": "G",
        "HIS": "H",
        "ILE": "I",
        "LYS": "K",
        "LEU": "L",
        "MET": "M",
        "ASN": "N",
        "PRO": "P",
        "GLN": "Q",
        "ARG": "R",
        "SER": "S",
        "THR": "T",
        "VAL": "V",
        "TRP": "W",
        "TYR": "Y"
    }
