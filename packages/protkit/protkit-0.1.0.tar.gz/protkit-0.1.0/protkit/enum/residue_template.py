class ResidueTemplate:
    VALID_RESIDUES = {
        "ARG",
        "ALA",
        "ASN",
        "ASP",
        "CYS",
        "GLN",
        "GLU",
        "GLY",
        "PHE",
        "HIS",
        "ILE",
        "LEU",
        "LYS",
        "MET",
        "PRO",
        "SER",
        "THR",
        "TRP",
        "TYR",
        "VAL"
    }

    VALID_DNA_RESIDUES = {
        "DA",
        "DC",
        "DG",
        "DT"
    }

    ENCODING_MAP = {
        0: ["ALA", "A"],
        1: ["CYS", "C"],
        2: ["ASP", "D"],
        3: ["GLU", "E"],
        4: ["PHE", "F"],
        5: ["GLY", "G"],
        6: ["HIS", "H"],
        7: ["ILE", "I"],
        8: ["LYS", "K"],
        9: ["LEU", "L"],
        10: ["MET", "M"],
        11: ["ASN", "N"],
        12: ["PRO", "P"],
        13: ["GLN", "Q"],
        14: ["ARG", "R"],
        15: ["SER", "S"],
        16: ["THR", "T"],
        17: ["VAL", "V"],
        18: ["TRP", "W"],
        19: ["TYR", "Y"],
    }

    STANDARD_RESIDUES = {
        "ALA": {
            "name": "Alanine",
            "short_code": "A",
            "long_code": "ALA",
            "int": 0,
            "charge": 0.0,
            "hydrophobicity": 1.8
        },
        "ARG": {
            "name": "Arginine",
            "short_code": "R",
            "long_code": "ARG",
            "int": 14,
            "charge": 1.0,
            "hydrophobicity": -4.5
        },
        "ASN": {
            "name": "Asparagine",
            "short_code": "N",
            "long_code": "ASP",
            "int": 11,
            "charge": 0.0,
            "hydrophobicity": -3.5
        },
        "ASP": {
            "name": "Aspartic Acid",
            "short_code": "D",
            "long_code": "ASP",
            "int": 2,
            "charge": -1.0,
            "hydrophobicity": -3.5
        },
        "CYS": {
            "name": "Cysteine",
            "short_code": "C",
            "long_code": "CYS",
            "int": 1,
            "charge": 0.0,
            "hydrophobicity": 2.5
        },
        "GLN": {
            "name": "Glutamine",
            "short_code": "Q",
            "long_code": "GLN",
            "int": 13,
            "charge": 0.0,
            "hydrophobicity": -3.5
        },
        "GLU": {
            "name": "Glutamic Acid",
            "short_code": "E",
            "long_code": "GLU",
            "int": 3,
            "charge": -1.0,
            "hydrophobicity": -3.5
        },
        "GLY": {
            "name": "Glycine",
            "short_code": "G",
            "long_code": "GLY",
            "int": 5,
            "charge": 0.0,
            "hydrophobicity": -0.4
        },
        "HIS": {
            "name": "Histidine",
            "short_code": "H",
            "long_code": "HIS",
            "int": 6,
            "charge": 0.1,
            "hydrophobicity": -3.2
        },
        "ILE": {
            "name": "Isoleucine",
            "short_code": "I",
            "long_code": "ILE",
            "int": 7,
            "charge": 0.0,
            "hydrophobicity": 4.5
        },
        "LEU": {
            "name": "Leucine",
            "short_code": "L",
            "long_code": "LEU",
            "int": 9,
            "charge": 0.0,
            "hydrophobicity": 3.8
        },
        "LYS": {
            "name": "Lysine",
            "short_code": "K",
            "long_code": "LYS",
            "int": 8,
            "charge": 1.0,
            "hydrophobicity": -3.9
        },
        "MET": {
            "name": "Methionine",
            "short_code": "M",
            "long_code": "MET",
            "int": 10,
            "charge": 0.0,
            "hydrophobicity": 1.9
        },
        "PHE": {
            "name": "Phenylalanine",
            "short_code": "F",
            "long_code": "PHE",
            "int": 4,
            "charge": 0.0,
            "hydrophobicity": 2.8
        },
        "PRO": {
            "name": "Proline",
            "short_code": "P",
            "long_code": "PRO",
            "int": 12,
            "charge": 0.0,
            "hydrophobicity": -1.6
        },
        "SER": {
            "name": "Serine",
            "short_code": "S",
            "long_code": "SER",
            "int": 15,
            "charge": 0.0,
            "hydrophobicity": -0.8
        },
        "THR": {
            "name": "Threonine",
            "short_code": "T",
            "long_code": "THR",
            "int": 16,
            "charge": 0.0,
            "hydrophobicity": -0.7
        },
        "TRP": {
            "name": "Tryptophan",
            "short_code": "W",
            "long_code": "TRP",
            "int": 18,
            "charge": 0.0,
            "hydrophobicity": -0.9
        },
        "TYR": {
            "name": "Tyrosine",
            "short_code": "Y",
            "long_code": "TYR",
            "int": 19,
            "charge": 0.0,
            "hydrophobicity": -1.3
        },
        "VAL": {
            "name": "Valine",
            "short_code": "V",
            "long_code": "VAL",
            "int": 17,
            "charge": 0.0,
            "hydrophobicity": 4.2
        }
    }

    EXTENDED_RESIDUES = {
        "SEC": {
            "name": "Selenocysteine",
            "short_code": "U",
            "long_code": "SEC",
            "int": 20,
            "charge": 0.0
        }
    }