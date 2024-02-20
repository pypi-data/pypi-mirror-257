"""
# Roadmap

Below are the main features for Protkit and their current status.

| MVP | Target date | Description |
| --- | ----------- | ----------- |
| 1   | Feb 2024    | Core structure and sequence representations, core file support, core download support, basic anomaly detection, property and metadata management, chemical identity properties, physiochemical properties, pharmacophore properties, structural properties, interface properties, structural alignment, RMSD, sequence alignment metrics, initial task specification via abstract base classes, pairwise alignment, antibody numbering |
| 2   | Apr 2024    | Additional download data sources, expand file support, anomaly fixing, reporting, expand physiochemical properties, expand phamacophore properties, expand structural properties, expand interface properties, geometric manupulations, additional model evaluation metrics, initial task specifications for docker, web services, heuristic and multiple sequence alignment, structure prediction tools, docking tools, binding affinity, humanisation, feature preprocessing and generation |
| 3   | Jun 2024    | Expand file support, derived representations as needed, expand structural properties, expand interface properties, classification metrics, regression metrics, utility metricsm, structure alignment, PPI prediction tools, dynamics simulation, de novo tools, antibody-specific tasks, data storage and loading for ML models |
| 4   | Aug 2024    | Self-hosted and cloud-hosted capabilities, microservice architectures, automation engines |
| 5   | Oct 2024    | Large-scale dataset generation, hosting of ML datasets and models |
| 6   | Dec 2024    | Prepare for major version release (v1.0) |

Temporarily added as a module to generate documentation.

---

## Downloading Data (```protkit.download```)

Provide capabilities to download biological data from various sources.  Downloaded
data is stored to disk.

- **<font color="green">Download File</font>**:  Generic capability to download a file from a URL.
- **<font color="green">Parallel Download</font>**:  Generic capability to download multiple files in parallel.
- **<font color="green">(Parallel) Download PDB File(s) from RCSB</font>**:  Download a PDB file from RCSB (https://www.rcsb.org/).
- **<font color="green">(Parallel) Download CIF File(s) from RCSB</font>**:  Download a PDB file from RCSB (https://www.rcsb.org/).
- **<font color="green">(Parallel) Download Binary CIF File(s) from RCSB</font>**:  Download a PDB file from RCSB (https://www.rcsb.org/).
- **<font color="green">(Parallel) Download PDB File(s) from SabDab</font>**:  Downloads a SabDab file from opig (https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabdab).
- **<font color="green">(Parallel) Download Fasta File(s) from RCSB</font>**:  Downloads a Fasta file from RCSB (https://www.rcsb.org/).
- **<font color="green">(Parallel) Download Fasta File(s) from Uniprot</font>**:  Downloads a Fasta file from UnitProt (https://www.uniprot.org/).
- **<font color="black">Download PDB Master List</font>**:  Downloads the master list of PDB files from RCSB.

| MVP | Description |
| --- | ----------- |
| <font color="green">1</font>   | <font color="green">READY. Able to download PDB and Fasta files from RCSB, Uniprot and Sabdab.</font> |
| 2   | Able to download files from additional sources. The ability to download files is fairly easy to implement, but the challenge is to identify the sources of reliable data. The data usually also has associated metadata, so it is important to be able to handle the metadata sooner rather than later.  |

---

## Reading and Writing Data (```protkit.file_io```)

Provide capabilities to read and write biological data from various file formats.
Support both structural and sequence based file formats. Expand to support
other types of file formats, such as alignment data or simulation data.

### Structure File Formats

Read and write structure data from various file formats. Structure-based representation
of a protein is constructed as a ```Protein```.  Where available, sequence-based data
is read and stored as part of a ```Protein``` in a ```Sequence``` object.

- **<font color="green">Read Prot File</font>**:  Read a Prot file.  Returns a list of Proteins.
- **<font color="green">Write Prot File</font>**:  Write a Prot file.
- **<font color="green">Read PDB File</font>**:  Read a PDB file. Returns a list of Proteins.  <font color="red">Only supports reading of structural and sequence based fields like ATOM, HETATM, SEQRES, etc.</font>
- **<font color="green">Write PDB File</font>**:  Write a PDB file.
- **<font color="green">Convert PDB to Prot File</font>**:  Convert a PDB file to a Prot file.
- **<font color="green">Read PQR File</font>**:  Read a PQR file. Returns a list of Proteins.
- **<font color="green">Write PQR File</font>**:  Write a PQR file. <font color="red">An update is needed in PDBIO to properly save PQR files. Currently stored in PDB format</font>
- **<font color="green">Convert PQR to Prot File</font>**:  Convert a PQR file to a Prot file.
- **<font color="green">Read MMTF File</font>**:  Read a MMTF file <font color="red">Currently, conversion to PDB and then read. Some properties may be lost</font>.
- **<font color="black">Write MMTF File</font>**:  Write a MMTF file.
- **<font color="green">Convert MMTF File to Prot File</font>**:  Convert an MMTF file to a Prot file. <font color="red">Currently, conversion to PDB and then read. Some properties may be lost</font>.
- **<font color="green">Read mmCIF File</font>**:  Read a mmCIF file <font color="red">Currently, conversion to PDB and then read. Some properties may be lost</font>.
- **<font color="black">Write mmCIF File</font>**:  Write a mmCIF file.
- **<font color="green">Convert mmCIF File to Prot file</font>**:  Convert a mmCIF file to a Prot file. <font color="red">Currently, conversion to PDB and then read. Some properties may be lost</font>.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">READY. Able to work with PDB, PRQ and Prot files. This forms the core of 3D data sources.</font> |
| 2   | Additional support for mmCIF and MMTF formats |

### Sequence File Formats

Read and write sequence data from various file formats. Sequence-based representation
is constructed as a ```Sequence```.

- **<font color="green">Read Fasta File</font>**:  Read a Fasta file. Returns a list of Sequences.
- **<font color="green">Write Fasta File</font>**:  Write a Fasta file.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">READY. Support for Fasta files.</font> |

### Alignment File Formats

Read alignment data from various file formats. <font color="red">Alignment-based representation
to be decided upon</font>.

- **<font color="black">Read Clustal File</font>**:  Read a Clustal file. Returns a list of alignments / Sequences.
- **<font color="black">Write Clustal File</font>**:  Write a Clustal file.

| MVP | Description |
| --- | ----------- |
| 2   | Support for Clustal files |

### Simulation File Formats

Read simulation data from various file formats. <font color="red">Simulation-based representation
to be decided upon</font>.

- **<font color="black">Reading MD simulation files (trajectories)</font>**: Read data from MD simulation files (trajectories).

| MVP | Description |
| --- | ----------- |
| 3+   | Support for handling simulations does not immediately contribute to the success of the project. |

---

## Core Data Representations (```protkit.core```)

### Structural Representations

Maintain structural data of a protein. A ```Protein``` consists of a list of ```Chain``` objects.
Each ```Chain``` consists of a list of ```Residue``` objects. Each ```Residue``` consists
of a list of ```Atom``` objects.  Entities can also maintain a reference to their parent, i.e.
an ```Atom``` maintains a reference to its parent ```Residue```, a ```Residue``` maintains a
reference to its parent ```Chain``` and a ```Chain``` maintains a reference to its parent
```Protein```.

Each object also maintains a set of core properties that
describe the object.  Extended properties are those that can be added to an object.

This is a **hierarchical representation** of a protein structure.  **Linear representation**
of an entity can be achieved by filters that query for specific properties at levels below
the entity.

### Proteins

A ```Protein``` represents a protein structure. A ```Protein``` maintains a set of properties
that describe the protein.  Core properties provide the minimum set of properties required
to describe a protein.  Extended properties are those that can be added to a protein.
A protein contains a list of ```Chain``` objects.

- **<font color="green">Core properties</font>** (with getters and setters):
    - PDB ID
- **<font color="green">Extended properties</font>**
- **<font color="green">Construction</font>**
    - Constructor
    - Copy Protein
    - Chains Management (add, remove, keep)
    - Residues Management (add, remove)
    - Atom management (add, remove, keep, keep backbone)
    - Renaming chains
    - Renumber residues
- **<font color="green">Statistics and Queries</font>**
    - Number of chains
    - Number of residues
    - Number of disordered residues
    - Number of hetero residues
    - Number of water residues
    - Number of residues by type
    - Number of atoms
    - Number of heavy atoms
    - Number of hydrogen atoms
    - Number of disordered atoms
    - Number of hetero atoms
- **<font color="green">Fixes and checks</font>**
    - Remove hetero residues
    - Remove water residues
    - Missing heavy atoms types
    - Extra heavy atom types
    - Missing Hydrogen atom types
    - Extra hydrogen atom types
    - Fix disordered atoms
    - Remove hydgroen atoms
- **<font color="green">Filter chains</font>**: Filter chains based on specified chain criteria.
- **<font color="green">Filter residues</font>**: Filter residues based on specified residue criteria.
- **<font color="green">Filter atoms</font>**: Filter atoms based on specified atom criteria.

### Chains

A ```Chain``` represents a chain in a protein structure. A ```Chain``` maintains a set of properties
that describe the chain.  Core properties provide the minimum set of properties required
to describe a chain.  Extended properties are those that can be added to a chain.
A chain can maintain a reference to its associated ```Protein```. A chain contains
a list of ```Residue``` objects.

- **<font color="green">Core properties</font>** (with getters and setters):
    - Chain ID
    - Sequence
- **<font color="green">Extended properties</font>**
- **<font color="green">Construction</font>**
    - Constructor
    - Copy Chain
    - Protein Management (assign)
    - Residues Management (add, remove)
    - Atom management (add, remove, keep)
    - Renaming chain
    - Renumbering residues
- **<font color="green">Statistics and Queries</font>**
    - Number of residues
    - Number of hetero residues
    - Number of water residues
    - Number of disordered residues
    - Number of residues by type
    - Number of atoms
    - Number of heavy atoms
    - Number of hydrogen atoms
    - Number of disordered atoms
    - Number of hetero atoms
- **<font color="green">Fixes and checks</font>**
    - Remove hetero residues
    - Remove water residues
    - Missing heavey atom types
    - Extra heavy atom types
    - Missing Hydrogen atom types
    - Exra hydrogen atom types
    - Fix disordered atoms
    - Remove hydgroen atoms
- **<font color="green">Filter residues</font>**: Filter residues based on specified residue criteria.
- **<font color="green">Filter atoms</font>**: Filter atoms based on specified atom criteria.

### Residues (```protkit.core.residue```)

Represents a residue in a protein structure. A ```Residue``` maintains a set of properties
that describe the residue.  Core properties provide the minimum set of properties
required to describe a residue.  Extended properties are those that can be added to a residue.
A residue can maintain a reference to its associated ```Chain```. A residue contains
a list of ```Atom``` objects.

- **<font color="green">Core properties</font>** (with getters and setters):
    - Residue type
    - Sequence number
    - Insertion code
- **<font color="green">Extended properties</font>**
- **<font color="green">Construction</font>**
    - Constructor
    - Copy Residue
    - Chain Management (assign)
    - Atoms Management (add, remove, keep, keep backbone, etc)
- **<font color="green">Statistics and Queries</font>**
    - Number of atoms
    - Number of heavy atoms
    - Number of hydrogen atoms
    - Number of disordered atoms
    - Number of hetero atoms
- **<font color="green">Fixes and checks</font>**
    - Missing heavy atoms types
    - Extra heavy atoms types
    - Hydrogen atom types
    - Missing hydrogen atom types
    - Extra hydrogen atom types
    - Fix disordered atoms
- **<font color="green">Filter atoms</font>**: Filter atoms based on specified atom criteria.

### Atoms (```protkit.core.atom```)

Represent a single atom in a protein structure. An ``Atom`` maintains a set of properties
that describe the atom.  These properties are divided into two categories: core and extended.
Core properties are those that are required to describe the atom, typically those found
in PDB files.  Extended properties are those that can be added to an atom.
An atom can maintain a reference to its associated ```Residue```.

- **<font color="green">Core properties</font>** (with getters and setters):
    - Element
    - Atom type
    - x
    - y
    - z
    - is_hetero
    - is_disordered
    - alt_loc
    - occupancy
    - temp_factor
    - assigned_charge
- **<font color="green">Extended properties</font>**
- **<font color="green">Construction</font>**
    - Constructor
    - Residue (assign)
- **<font color="green">Merge Disordered Atom</font>**
- **<font color="green">Fix Disordered Atom</font>**

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">READY. Support for Protein, Chain, Residue and Atom structures is core to the project and should be released as soon as possible.</font> |

### Sequence Representations

Data structures for managing sequence data. The ```Sequence``` class is the base class
for all sequence-based representations.  ```ProteinSequence``` and ```NucleotideSequence```
are derived from ```Sequence```.  ```AntibodySequence``` is derived from ```ProteinSequence```.

### Sequences (```protkit.core.sequence```)

Represents a sequence with associated metadata. Elementary alignment functionality.

<font color="red">To add attribute extension functionality</font>

### Protein Sequence (```protkit.core.protein_sequence```)

Represents a protein sequence.

### Nucleotide Sequence (```protkit.core.nucleotide_sequence```)

Represents a nucleotide sequence.

### Antibody Sequence (```protkit.core.antibody_sequence```)

Represents an antibody sequence.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">READY. Support for Sequence and derived structures is core the project.</font> |

### Derived Representations

Data structures not directly representing protein structure or sequence data, but
derived from them.

### Surfaces

<font color="red">To be decided upon</font>

### Epitope / Paratope

<font color="red">To be decided upon</font>

### Protein dynamics

<font color="red">To be decided upon</font>

| MVP | Description |
| --- | ----------- |
| 2+   | Derived representations as needed by tasks. |

---

## Quality Checks, Anomaly Detection and Fixes (```protkit.core```)

Methods to detect and fix common problems in protein structures. These methods
can be applied at the level of a ```Protein```, ```Chain```, ```Residue``` or ```Atom```
and are generally build into the entities themselves.

Distinction between detection and fixing methods.  Detection detects that there
is a problem, while fixing methods attempt to correct the issue (typically a harder
problem).

### Chain-level

- **<font color="green">Rename chain</font>**:  Rename a chain.
- **<font color="green">Remove chain chain</font>**:  Remove a chain.
- **<font color="black">Detect and remove non-protein chains</font>**:  Removes non-protein (eg. nucleotide-based chains) from an entity.

### Residue-level

- **<font color="green">Renumber residues</font>**:  Renumber residues.
- **<font color="green">Remove residues</font>**:  Removes residues from an entity.
- **<font color="black">Remove carbohydrate-based residues</font>**:  Removes carbohydrate-based residues from an entity.
- **<font color="black">Remove ligand-based residues</font>**:  Removes ligand-based residues from an entity.
- **<font color="green">Remove Hetero Residues/Atoms [Protein, Chain]</font>**:  Removes hetero residues from an entity.
- **<font color="green">Remove Water Residues [Protein, Chain]</font>**:  Removes water residues from an entity.
- **<font color="black">Remove non-standard residues</font>**:  Removes non-standard residues from an entity.
- **<font color="black">Rename non-standard residues</font>**:  Renames non-standard residues to standard names in an entity.
- **<font color="orange">Detect Missing Residues</font>**:  Detects missing residues in chain. This is accomplished by comparing the residue structure information to sequence data (from SEQRES records in PDB file or from FASTA file).
- **<font color="black">Add Missing Residues</font>**:  Add missing residues in chain by modelling them.

### Atom-level

- **<font color="orange">Detect Missing Atoms [Protein, Chain]</font>**:  Detects missing atoms in a residue.
- **<font color="orange">Detect Extra Atoms [Protein, Chain]</font>**:  Detects extra atoms in a residue.
- **<font color="orange">Detect Missing Heavy Atoms</font>**:  Detects missing heavy atoms in a residue.
- **<font color="orange">Detect Extra Heavy Atoms</font>**:  Detects extra heavy atoms in a residue.
- **<font color="orange">Detect Missing Hydrogen Atoms</font>**:  Detects missing hydrogen atoms in a residue.
- **<font color="orange">Detect Extra Hydrogen Atoms</font>**:  Detects extra hydrogen atoms in a residue.
- **<font color="black">Detect missing terminal (OXT) atoms in residues</font>**
- **<font color="black">Add missing terminal (OXT) atoms in residues</font>**
- **<font color="black">Add Missing Atoms [Protein, Chain]</font>**:  Adds missing atoms to an entity.
- **<font color="green">Fix Disordered Atoms [Protein, Chain]</font>**:  Removes alternate conformations from an entity.
- **<font color="green">Remove Hydrogen Atoms (deprotonate)</font>**:  Removes hydrogen atoms
- **<font color="black">Add Hydrogen Atoms (protonate)</font>**:  Adds hydrogen atoms

### Structure Checks

- **<font color="black">Detect breaks in segments of residues in chains</font>**:  Detects breaks in segments of residues in chains based on distance between backbone atoms.
- **<font color="black">Assign segments to continues residues</font>**:  Assigns segments to continues residues based on distance between backbone atoms.
- **<font color="black">Detect anomalies in bond lengths</font>**:  Detects anomalies in covalent bond lengths.
- **<font color="black">Detect anomalies in bond angles</font>**:  Detects anomalies in covalent bond angles.
- **<font color="black">Rotamer evaluation / Detect anomalies in dihedral angles</font>**:  Detects anomalies in dihedral angles.
- **<font color="black">Detect clashes</font>**:  Detects atomic clashes in a protein.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="orange">IN PROGRESS. Detection of anomalies across Protein, Chain, Residue and Atom. Fixes not immediately required.</font> |
| 2   | Fixing anomalies that require modelling. Achieved through external tools integrations. |
| 2   | Reporting mechanisms |

---

## Properties (```protkit.properties```)

Properties are measurable characteristics of a protein, chain, residue or atom.
Properties can be core properties, which are part of the core representation of
an entity, or extended properties, which are added to an entity.

The properties in this module generally relates to extended properties, organized
by category, such as chemical identity, physiochemical properties, pharmacophore
properties, structural properties and interface properties.

These properties are calculated using modules in the ```protkit.properties``` package.
Calculated properties can be added to entities.

### Property and Metadata Management

Management of properties and metadata for entities.

<font color="green">Needs to be applied against sequence-bases objects as well. Perhaps move into interface definition that all entities inherit from.</font>

- **<font color="green">Setting Properties [Atom, Residue, Chain, Protein]</font>**:  Sets properties for entities.
- **<font color="green">Checking Properties [Atom, Residue, Chain, Protein]</font>**:  Checks properties for entities.
- **<font color="green">Removing Properties [Atom, Residue, Chain, Protein]</font>**:  Removes properties for entities.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">READY. Management of properties and metadata for entities critial as part of first release.</font> |

### Chemical Identity

Properties related to the chemical identity of atoms or residues.

- **<font color="green">Element Type [Atom]</font>**:  Element associated with an atom (part of core representation).
- **<font color="green">Atom Type [Atom]</font>**:  Atom name within a residue (part of core representation).
- **<font color="green">Residue Type [Residue]</font>**:  Residue type (part of core representation).
- **<font color="green">Chemical Class [Residue]</font>**:  Chemical classes associated with a residue.
- **<font color="black">Amino Acid Composition [Chain, Protein]</font>**:  Distribution of amino acids in a chain or protein.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">READY (to finalise amino acid composition). Chemical identity properties. |
| 2   | Amino acid composition. |

### Physiochemical Properties

Measurable properties of molecules related to the physical and chemical characteristics.

- **<font color="green">Mass [Atom, Residue, Chain, Protein]</font>**:  Calculates the mass based on individual atoms (eg. from periodic table).
- **<font color="green">Molecular Weight [Residue, Chain, Protein]</font>**:  Calculates the molecular weight of residues, chains and proteins, based on exected masses of residues (in case of missing atoms).
- **<font color="green">Hydrophobicity [Residue, Chain, Protein, Sequence]</font>**:  Calculates the hydrophobicity using Kyte-Doolittle scale.
- **<font color="green">Hydrophobicity Class [Residue, Chain, Protein, Sequence]</font>**:  Calculates the hydrophobicity class of a structure.
- **<font color="green">Polarity [Residue] </font>**:  Polarity of a residue.
- **<font color="green">Charge [Residue] </font>**:  Charge of a residue.
- **<font color="black">Charge [Atom]</font>**:  Charges / partial charges of an atom (requires quantum chemistry packages)
- **<font color="black">Isoelectric Point [Residue, Chain, Protein]</font>**:  Isoelectric point (pH of no net electrical charge) of an entity.
- **<font color="black">Electrostatics [Surface]</font>**:  Electrostatics of a protein surface.
- **<font color="black">Evolutionary Conservation [Residue]</font>**:  Evolutionary conservation of a residue.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">READY (To review code) Mass, molecular weight, hydrophobicity, hydrophobicity class, polarity (residue), charge (residue)</font> |
| 2   | Charge (atom), isoelectric point, electrostatics, evolutionary conservation |

### Pharmacophore Properties

Properties that relate to the recognition and binding of a molecule to its biological target.

- **<font color="green">H-bond Donor/Acceptors Residues [Residue]</font>**:  Donor/acceptor residues for hydrogen bonds on a protein surface.
- **<font color="green">H-bond Donor/Acceptors Atoms [Atom]</font>**:  Donor/acceptor atoms for hydrogen bonds on a protein surface.
- **<font color="black">Aromaticity [Residue]</font>**:  Aromaticity of a residue.
- **<font color="black">Hydrophobic Regions/Patches [Residue]</font>**:  Hydrophobicity patches of a residue.
- **<font color="black">Aliphatic Centers [Residue]</font>**:  Aliphatic centers of a residue.
- **<font color="black">Positive or Negative Charge Centers [Residue]</font>**:  Positive or negative charge centers of a residue.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">DONE. H-bond Donor/Acceptor Atoms</font> <font color="red">Needs test cases.</font> |
| 2   | Aromaticity, hydrophobic regions/patches, aliphatic centers, positive or negative charge centers |

### Structural Properties

Properties related to the three-dimensional structure of a molecule.

- **<font color="green">Atom Coordinates [Atom]</font>**:  Coordinates of an entity (derived form core representation).
- **<font color="green">Residue Coordinates [Residue]</font>**:  Calculated based on atoms present in a residue, eg. CA atom, or other averaging mechanism.
- **<font color="green">Entity Bounds [Residue, Chain, Protein]</font>**:  Calculated from atomic coordinates.
- **<font color="green">Entity Center [Residue, Chain, Protein]</font>**:  Calculated from atomic coordinates.
- **<font color="orange">Solvent Accessibility [Atom, Residue, Chain, Protein]</font>**:  Solvent accessibility of a structure (entities exposed to surface of protein) [DSSP, NACCESS, FreeSASA
- **<font color="orange">Accessible Surface Area [Atom, Residue, Chain, Protein]</font>**:  Surface area of a structure, calculated form surface accessibilty.
- **<font color="orange">Relative accessible surface area [Atom, Residue, Chain, Protein]</font>**:  Relative surface area of a structure, calculated form surface accessibilty and changes in bound and unbound state.
- **<font color="orange">Structural Region [Residue]</font>**:  Structural region of a residue (core, rim, support, surfacem, interior).
- **<font color="orange">Circular Variance [Atom, Residue]</font>**: Circular variance
- **<font color="green">Volume [Residue, Chain, Protein, Sequence]</font>**:  Volume of a structure.
- **<font color="green">Volume Class [Residue, Chain, Protein, Sequence]</font>**:  Volume class of a structure.
- **<font color="green">Covalent Bond Lengths</font>**:  Bond lengths of covalent bonds in structure.
- **<font color="green">Covalent Bond Angles</font>**:  Bond angles of covalent bonds in structure.
- **<font color="green">Dihedral / Torsional Angles [Residue]</font>**:  Calculates the dihedral angles with a residue and between consequtive residues in a chain. [GROMACS, CHARMM, ProDy]
- **<font color="black">Van der Waals radii [Atom]</font>**:  Van der Waals radii of an atom.
- **<font color="black">Secondary Structure [Residue]</font>**:  Calculates the secondary structure in a chain [DSSP, STRIDE].
- **<font color="black">Concavity []</font>**:  Concavity
- **<font color="black">Residue Burial Depth [Residue]</font>**: Residue burial depth (distance to protein surface).
- **<font color="black">Flexibility [Atom, Residue]</font>**: Flexibility as provided by B-factors from crystallography.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="orange">IN PROGRESS. Atom coordinates, residue coordinates, entity bounds, entity center, covalent bond lengths, covalent bond angles, dihedral angles, volume, solvent accessibility, accessible surface area, relative accessible surface area, structural region, circular variance</font> |
| 2   | Van der Waals radii, secondary structure, concavity, residue burial depth, flexibility |

### Interface Properties

Properties related to the interface between chains.

- **<font color="green">Interface Atoms [Atom]</font>**:  Atoms at the interface, within a cutoff-distance from another chain.
- **<font color="green">Interface Residues [Residue]</font>**:  Residues at the interface, within a cutoff-distance from another chain.
- **<font color="green">Interface Residues by Alpha Carbon [Residue]</font>**:  Residues at the interface, within a cutoff-distance from another chain.
- **<font color="black">Interface Area [Residue]</font>**:  Area associated with the interface between two chains.
- **<font color="black">Hydrogen Bond Identification [Atom]</font>**: Identification of Hydrogen bonding calculations. [DSSP, HBPLUS]
- **<font color="black">Disulfide Bonds</font>**:  Calculates the disulfide bonds of a protein.
- **<font color="black">Other Bonds</font>**: Calculates other bonds of a protein (van der Waals, salt bridges, halogens, etc.)

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">DONE. Interface atoms, interface residues</font> |
| 2   | Interface area, Hydrogen bond identification, disulfide bonds, other bonds |

---

## Geometric Manupulations (```protkit.geometry```)

Mathematical computation on coordinates and vectors.

- **<font color="green">Magnitude</font>**:  Vector magnitude.
- **<font color="green">Distance</font>**:  Euclidean distance between two vectors.
- **<font color="green">Dot Product</font>**:  Dot product between two vectors.
- **<font color="green">Cross Product</font>**:  Cross product between two vectors.
- **<font color="green">Angle</font>**:  Angle between two vectors.
- **<font color="green">Dihedral Angle</font>**:  Dihedral angle between three vectors.

| MVP | Description |
| --- | ----------- |
| 1    | <font color="green">READY. Magnitude, distance, dot product, cross product, angle, dihedral angle. These are essential to other computations.</font> |

Geometric manipulations of protein structures.

- **<font color="black">Rotate Structure</font>**:  Rotates a structure.
- **<font color="black">Translate Structure</font>**:  Translates a structure.
- **<font color="black">Align Structures</font>**:  Aligns two structures.
- **<font color="black">Transform Coordinates</font>**: Transforms coordinates of a structure relative to a orthogonal coordinate system.

| MVP | Description |
| --- | ----------- |
| 2    | Structure alignment as example of geometric manipulations. |
| 2+   | Other geometric manipulations of protein structures. |

---

## Metrics

Metrics applicable to protein structures and sequences for evaluating properties.

### Model Evaluation Metrics

- **<font color="green">RMSD</font>**:  Root Mean Square Deviation (RMSD) measures the average distance between corresponding atoms in two structures.
    - CA atoms
    - Backbone atoms (N, CA, C, O)
    - All atoms
- **<font color="orange">TM-Score</font>**:  TM (Template Modelling) score measures the structural similarity between two structures.
- **<font color="orange">GDT</font>**:  GDT (Global Distance Test) evaluates precision of a model by measuring the percentage of residues in a predicted structures that are within a specified distance of the native structure.
- **<font color="orange">Fnat</font>**:  Fnat (Fraction of Native Contacts) measures the fraction of contacts in the predicted models that are also present in the native structure.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">READY (stubs created for other metrics as well). RMSD</font> |
| 2   | TM-Score, GDT, Fnat |

### Sequence Alignment Metrics

- **<font color="green">Sequence Identity</font>**:  Sequence identity measures the percentage of identical residues between two aligned sequences.
- **<font color="green">Sequence Similarity</font>**:  Sequence similarity measures the percentage of similar residues between two aligned sequences.
- **<font color="green">Alignment Coverage</font>**:  Sequence coverage measures the percentage of residues in a sequence that are aligned to another sequence.
- **<font color="green">Edit Distance</font>**:  Minimum number of edits required to transform one sequence into another.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">DONE. Sequence identity, sequence similarity, alignment coverage, edit distance</font> |

### Classification Metrics

- **<font color="black">Accuracy</font>**:  Accuracy measures the percentage of correctly classified samples.
- **<font color="black">Precision</font>**:  Precision measures the percentage of correctly classified positive samples among all positive predictions
- **<font color="black">Recall</font>**:  Recall measures the percentage of correctly classified positive samples among all actual positive instances.
- **<font color="black">F1 Score</font>**:  F1 score is the harmonic mean of precision and recall.
- **<font color="black">ROC AUC</font>**:  ROC AUC (Area Under the Curve) measures the area under the ROC curve.
- **<font color="black">Confusion Matrix</font>**:  Confusion matrix measures the number of true positives, false positives, true negatives and false negatives.

| MVP | Description |
| --- | ----------- |
| 2+  | Accuracy, precision, recall, F1 score, ROC AUC, confusion matrix. Care should be taken not to duplicate measures available in other frameworks, such as Scikit-learn or PyTorch. Rather, these should be customised for use across in ML tasks related to structural biology. |

### Regression Metrics

- **<font color="black">Mean Absolute Error</font>**:  Mean Absolute Error (MAE) measures the average absolute difference between predicted and actual values.
- **<font color="black">Mean Squared Error</font>**:  Mean Squared Error (MSE) measures the average squared difference between predicted and actual values.
- **<font color="black">Root Mean Squared Error</font>**:  Root Mean Squared Error (RMSE) measures the square root of the average squared difference between predicted and actual values.
- **<font color="black">R2 Score</font>**:  R2 Score measures the proportion of variance in the dependent variable that is predictable from the independent variable.
- **<font color="black">Pearson Correlation Coefficient</font>**:  Pearson Correlation Coefficient measures the linear correlation between two variables.
- **<font color="black">Spearman's Rank Correlation Coefficient</font>**:  Spearmans Rank Correlation Coefficient measures the monotonic relationship between two variables.

| MVP | Description |
| --- | ----------- |
| 2+  | Mean Absolute Error, Mean Squared Error, Root Mean Squared Error, R2 Score, Pearson Correlation Coefficient, Spearman's Rank Correlation Coefficient. Care should be taken not to duplicate measures available in other frameworks, such as Scikit-learn or PyTorch. Rather, these should be customised for use across in ML tasks related to structural biology. |

### Utility Metrics

- **<font color="black">Execution Time</font>**:  Execution time measures the time taken to execute a task.
- **<font color="black">Memory Usage</font>**:  Memory usage measures the memory used by a task.
- **<font color="black">Disk Usage</font>**:  Disk usage measures the disk space used by a task.
- **<font color="black">Network Usage</font>**:  Network usage measures the network bandwidth used by a task.

| MVP | Description |
| --- | ----------- |
| 3+  | Metrics become important as a scalable solution is required. |

---

## Tasks, Tools and Pipelines (```protkit.tasks```, ```protkit.tools``` and ```protkit.pipelines```)

Tasks are a collection of steps that perform a specific function.  Pipelines are
a sequence of tasks that are executed in a specific order and automates the
execution of a series of tasks. Tools implement the functionality of tasks.

To establish pipelines, tasks need to have a well-defined interface.  These interface
are be defined in the ```protkit.tasks``` module. A task can be considered as
an abstract base class and tools should honour the interface defined by the task.

Pipelines are implemented in the
```protkit.pipelines``` module and provide the functionality to feed the output
of one task into the input of another task.

Tools are implemented in the ```protkit.tools``` module and provide the
functionality for tasks.  Some of the tools are "adaptors" that implements
the task interface on the one hand and calls the tool on the other hand.

### Tools Integration / Pipeline Mechanisms

- **<font color="green">Integrating Internal Tools - Tool Architecture: Abstract Base Classes</font>**:  Integrating internal tools exposed via Python.
- **<font color="orange">Integrating External Tools - Tool Architecture: PyPI</font>**:  Integrating external tools exposed via PyPI.
- **<font color="black">Integrating External Tools - Tool Architecture: Docker</font>**:  Integrating external tools exposed via Docker.
- **<font color="black">Integrating External Tools - Tool Architecture: Web Services</font>**:  Integrating external tools exposed via web services.

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">DONE. Specify architecture required for Abstract Base Classes.</font> |
| 1   | <font color="orange">IN PROGRESS. Specify architecture required for PyPi + integrate 3 examples (eg. FreeSASA, ANARCI)</font>  |
| 2   | Specify architecture required for Docker and Web Services. |


### Sequence and Structure Alignment

- **<font color="black">Task: Pairwise Sequence Alignment</font>**:  Aligns two sequences.
    - **<font color="green">Task: Global Sequence Alignment (Needleman-Wunsch)</font>**:
    - **<font color="green">Task: Local Sequence Alignment (Smith-Waterman)</font>**:
    - **<font color="black">Tool: Emboss</font>**: Adaptor for Emboss (https://www.ebi.ac.uk/Tools/psa/emboss_needle/)
- **<font color="black">Task: Heuristic Sequence Alignment</font>**:  Aligns two sequences.
    - **<font color="black">Tool: BLAST</font>**: Adaptor for BLAST (https://blast.ncbi.nlm.nih.gov/Blast.cgi)
- **<font color="black">Task: Multiple Sequence Alignment</font>**:  Aligns multiple sequences.
    - **<font color="black">Tool: Clustal Omega</font>**: Adaptor for Clustal Omega (https://www.ebi.ac.uk/Tools/msa/clustalo/)
    - **<font color="black">Tool: MUSCLE</font>**: Adaptor for MUSCLE (https://www.ebi.ac.uk/Tools/msa/muscle/)
    - **<font color="black">Tool: MAFFT</font>**: Adaptor for MAFFT (https://mafft.cbrc.jp/alignment/software/)
    - **<font color="black">Tool: T-Coffee</font>**: Adaptor for T-Coffee (http://tcoffee.crg.cat/apps/tcoffee/index.html)
- **<font color="black">Task: Structure Alignment</font>**:  Aligns two structures.
    - **<font color="black">Tool: DALI</font>**: Adaptor for DALI (http://ekhidna2.biocenter.helsinki.fi/dali/)
    - **<font color="black">Tool: FATCAT</font>**: Adaptor for FATCAT (https://fatcat.godziklab.org/)
- **<font color="black">Task: Canonical Form Prediction</font>**:  Predicts the canonical form of a protein structure.
    - **<font color="black">Tool: SCALOP</font>**: Adaptor for SCALOP (https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/scalop/)

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">DONE. Basic Global and Local Pairwise Alignment (build in)</font>  <font color="red">Comprehensive test cases needed</font> |
| 2   | Integrations for Heuristic and Multiple Sequence Alignment with external tools |
| 3+   | Structure alignements, canonical forms, etc. |

### Structure Prediction
- **<font color="black">Task: Protein Structure Prediction from Sequence</font>**:  Predicts protein structures from sequences.
    - **<font color="black">Tool: AlphaFold</font>**: Adaptor for AlphaFold (https://alphafold.ebi.ac.uk/)
    - **<font color="black">Tool: RoseTTAFold</font>**: Adaptor for RoseTTAFold (https://rostlab.org/services/rosetta/)
    - **<font color="black">Tool: ESMFold</font>**: Adaptor for ESMFold ()
    - **<font color="black">Tool: OmegaFold</font>**: Adaptor for OmegaFold ()
- **<font color="black">Task: Antibody/Nanobody Structure Prediction from Sequence</font>**:  Predicts antibody/nanobody structures from sequences.
    - **<font color="black">Tool: ImmuneBuilder</font>**: Adaptor for ImmuneBuilder (https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/immune_builder)
- **<font color="black">Task: Structure Repair</font>**:  Repairs protein structures by modelling missing residues.
- **<font color="black">Task: Side Chain Prediction</font>**:  Predicts side chains for a protein structure.
- **<font color="black">Task: Structure Change Upon Mutation</font>**:  Predicts structural changes upon mutation of a residue(s).
    - **<font color="black">Tool: FoldX</font>**: Adaptor for FoldX (http://foldxsuite.crg.eu/)
- **<font color="black">Task: Protonation / Deprotonation</font>**:  Protonates / deprotonates a protein structure.
    - **<font color="red">Tool: Reduce</font>**: Adaptor for Reduce (http://kinemage.biochem.duke.edu/software/reduce.php)
    - **<font color="black">Tool: Propka</font>**: Adaptor for Propka ()
    - **<font color="black">Tool: PDB2PQR</font>**: Adaptor for PDB2PQR ()

| MVP | Description |
| --- | ----------- |
| 1   | <font color="red">NOT STARTED. Integrate one protonation tool</font> |
| 1   | <font color="red">NOT STARTED. Integrate one structure prediction tool</font> |
| 2   | Integrate structure repair, side chain prediction, structure change upon mutation |
| 2+   | Integrate other structure prediction tools |

### Protein-Protein Interactions
- **<font color="black">Task: Protein-Protein Interaction Prediction</font>**:  Predicts protein-protein interactions.
    - **<font color="black">Tool: EveBind</font>**: Adaptor for EveBind
- **<font color="black">Task: Paratope Prediction</font>**:  Predicts paratopes.
- **<font color="black">Task: Epitope Prediction (both antibody-agnostic and antibody-aware)</font>**:  Predicts epitopes.
- **<font color="black">Task: Protein Interface Prediction from Sequence</font>**:  Predicts protein interfaces from sequences.
- **<font color="black">Task: Epitope/Residue Binning</font>**:  Bins residues into epitope, paratope, interface and non-interface.

| MVP | Description |
| --- | ----------- |
| 2   | Integration one protein-protein interaction prediction tool |
| 3+  | Integration of other PPI tools |

### Docking and Simulation / Protein Dynamics

- **<font color="black">Task: Molecular Docking</font>**:  Performs molecular docking.
    - **<font color="black">Tool: HADDOCK3</font>**: Adaptor for HADDOCK3 (https://wenmr.science.uu.nl/haddock/)
- **<font color="black">Task: Molecular Dynamics Simulation</font>**:  Performs molecular dynamics simulation.
    - **<font color="black">Tool: GROMACS</font>**: Adaptor for GROMACS (https://www.gromacs.org/)
    - **<font color="black">Tool: NAMD</font>**: Adaptor for NAMD (https://www.ks.uiuc.edu/Research/namd/)
    - **<font color="black">Tool: AMBER</font>**: Adaptor for AMBER (https://ambermd.org/)
    - **<font color="black">Tool: CHARMM</font>**: Adaptor for CHARMM (https://www.charmm.org/)
    - **<font color="black">Tool: OpenMM</font>**: Adaptor for OpenMM (https://openmm.org/)
- **<font color="black">Task: Structure Relaxation / Refinement</font>**:  Refines a protein structure.
    - **<font color="black">Tool: Rosetta</font>**: Adaptor for Rosetta (https://www.rosettacommons.org/)
    - **<font color="black">Tool: Modeller</font>**: Adaptor for Modeller (https://salilab.org/modeller/)
- **<font color="black">Task: Charge / Electrostatic Calculation</font>**:  Calculates charges and electrostatics.
    - **<font color="black">Tool: APBS</font>**: Adaptor for APBS (https://www.poissonboltzmann.org/)

| MVP | Description |
| --- | ----------- |
| 2   | Integration of one molecular docking tool |
| 2   | Integration of one structure relaxation tool |
| 3+   | Integration of one dynamics simulation tool |

### Property Prediction

- **<font color="black">Task: Binding Affinity Prediction</font>**:  Predicts binding affinity.
- **<font color="black">Task: Binding Affinity Under Mutation Prediction</font>**:  Predicts binding affinity under single or multiple mutations.
- **<font color="black">Task: Aggregation Prediction</font>**:  Predicts aggregation propensity.
     - **<font color="black">Tool: Aggrescan3D</font>**: Adaptor for Aggrescan3D (http://biocomp.chem.uw.edu.pl/Aggrescan3D/)
     - **<font color="black">Tool: AgMata</font>**: Adaptor for AgMata
- **<font color="black">Task: PTM Prediction</font>**:  Predicts post-translational modifications.
- **<font color="black">Task: Immunogenicity Prediction</font>**:  Predicts immunogenicity.
- **<font color="black">Task: Toxicity Prediction</font>**:  Predicts toxicity.
- **<font color="black">Task: Solubility Prediction</font>**:  Predicts solubility.
- **<font color="black">Task: Stability Prediction</font>**:  Predicts stability.
- **<font color="green">Task: Surface Prediction</font>**:  Predicts surface properties.
    - **<font color="green">Tool: FreeSASA</font>**: Adaptor for FreeSASA (https://freesasa.github.io/)

| MVP | Description |
| --- | ----------- |
| 1   | <font color="green">Surface prediction with FreeSASA</font> |
| 2   | Integration of one binding affinity prediction tool |
| 3+  | Integration of other property prediction tools |

### De Novo Design

- **<font color="black">Task: Scaffold to Sequence (Inverse Folding)</font>**:  Converts a scaffold to a sequence.
    - **<font color="black">Tool: ProteinMPNN</font>**: Adaptor for ProteinMPNN ()
- **<font color="black">Task: Antibody Library Design</font>**:  Designs antibody libraries.
    - **<font color="black">Tool: AB-Gen</font>**: Adaptor for AB-Gen
- **<font color="black">Task: Binder Design</font>**:  Designs binders.
    - **<font color="black">Tool: RFDiffusion</font>**: Adaptor for RFDiffusion
- **<font color="black">Task: Antibody CDR Generation</font>**:  Generates CDRs for antibodies.
    - **<font color="black">Tool: DiffAb</font>**: Adaptor for DiffAb
- **<font color="black">Task: Full-atom Antibody Generation</font>**:  Generates full-atom antibodies.
    - **<font color="black">Tool: AbDiffuser</font>**: Adaptor for AbDiffuser
    - **<font color="black">Tool: dyMEAN</font>**: Adaptor for dyMEAN

| MVP | Description |
| --- | ----------- |
| 2   | Integration of one scaffold to sequence tool |
| 3+  | Integration of other de novo design tools |

### Antibody-specific Tasks

- **<font color="red">Task: Antibody Numbering</font>**:  Support for numbering antibodies across various naming conventions:
    - Chothia
    - IGMT
    - Kabat
    - Martin
    - AHo
    - **<font color="black">Tool: ANARCI</font>**: Adaptor for ANARCI (https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/anarci/)
- **<font color="black">Task: Identify CDR regions, Venier regions, FR regions</font>**:  Identifies CDR regions, Venier regions, FR regions.
- **<font color="black">Task: Antibody Annotation</font>**:  Annotates an antibody structure.
- **<font color="black">Task: Humanisation</font>**:  Humanisation of antibodies.
    - **<font color="black">Tool: BioPhi</font>**: Adaptor for BioPhi (https://biophi.dichlab.org/)
    - **<font color="black">Tool: AbNativ</font>**: Adaptor for AbNativ (https://gitlab.developers.cam.ac.uk/ch/sormanni/abnativ)
- **<font color="black">Task: Antibody Nativeness / Naturalness Evaluation</font>**:  Evaluating the degree to which an antibody sequence resembles natural antibodies and assessing potential immunogenicity.
- **<font color="black">Task: Antibody Humanness Evaluation</font>**:  Assessing the sequence for potential immunogenicity and determining the degree of similarity to human antibodies.
- **<font color="black">Task: Antibody Therapeutic Profiling</font>**:  Analyzing the therapeutic potential of antibodies based on their sequence, structure, and known functions.
    - **<font color="black">Tool: TAP</font>**: Adaptor for TAP (https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/tap)

| MVP | Description |
| --- | ----------- |
| 1   | <font color="RED">NOT STARTED. ANARCI numbering</font> |
| 2   | Humanisation, nativeness, humanness, therapeutic profiling |
| 3+  | Other antibody-specific tasks |

---

## Features and Machine Learning

Utilities to generate features from protein structures, sequences and properties and
to train machine learning models.

### Preprocessing and Feature Generation

- **<font color="black">Feature Generation</font>**:  Pipelines for generating features from protein structures, sequences and properties.
- **<font color="black">Feature Selection</font>**:  Selecting features from protein structures, sequences and properties.
- **<font color="black">Feature Normalisation and Scaling</font>**:  Normalising features from protein structures, sequences and properties.
- **<font color="black">Feature Encoding</font>**:  Encoding features from protein structures, sequences and properties.

- **<font color="black">Exporting Features as Tabular Data (eg. Numpy Tensors)</font>**: Exporting features as tabular data.
- **<font color="black">Exporting Features as Pandas Dataframe</font>**: Exporting features as Pandas Dataframe.
- **<font color="black">Exporting Features as Graph Data</font>**: Exporting features as graph data (2D) suitable for training with Geometric Deep Learning Models.
- **<font color="black">Exporting Features as Volumetric Data</font>**: Exporting features as volumetric data (3D) suitable for training with 3D Convolutional Neural Networks.
- **<font color="black">Exporting Features as Large Language Model Data</font>**: Exporting features as data (1D) suitable for training with Large Language Models.

### Data Storage and Loading

- **<font color="black">Data Storage</font>**:  Storage of feature data in ML file formats (Parquet, HDF5, Avro, etc.)
- **<font color="black">Data Loaders</font>**:  Loading of feature data via Data Loaders

### Machine Learning Models

- **<font color="black">Train Models</font>**:  Architecture to ease the development of machine learning models for structural biology.
- **<font color="black">Evaluate Models</font>**:  Evaluation of machine learning models applied in structural biology.

### Dataset Generation

- **<font color="black">Dataset Generation</font>**:  Generation of datasets ready for training with machine learning models.

| MVP | Description |
| --- | ----------- |
| 2   | Preprocessing and Feature Generation |
| 3   | Data Storage and Loading, Machine Learning Models |
| 4   | Dataset Generation |

---

## Reporting and Visualisation

- **<font color="black">Reporting</font>**:  Reporting of results from tasks and pipelines - TBD
- **<font color="black">Ramachandran Plot Analysis</font>**

"""