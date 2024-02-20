from protkit.file_io.pdb_io import PDBIO
from protkit.file_io.fasta_io import (FastaIO)
# from src.io.OPFIO import OPFIO

from protkit.core.protein import Protein
from protkit.core.antibody import Antibody
from protkit.core.sequence import Sequence
from protkit.util.mutation import Mutation

from protkit.tools.haddock_adaptor import HaddockAdaptor
from protkit.tools.zdock_adaptor import ZDockAdaptor
from protkit.tools.alphafold_adaptor import AlphafoldAdaptor
from protkit.tools.foldx_adaptor import FoldxAdaptor

# protein1 = Protein()
# protein2 = Protein()
#
# haddock = HaddockAdaptor(use_waters=True)
# haddock.blind_dock(protein1, protein2)
#
# haddock2 = HaddockAdaptor(use_waters=False)
# haddock2.blind_dock(protein1, protein2)
#
# zdock = ZDockAdaptor()
# zdock.blind_dock(protein1, protein2)
#
# use_haddock: bool = True
# use_waters: bool = False
# if use_haddock:
#     dock_engine = HaddockAdaptor(use_waters=use_waters)
# else:
#     dock_engine = ZDockAdaptor()
#
# alphafold = AlphafoldAdaptor()
#
# sequence = Sequence()
# protein = alphafold.fold_monomer(sequence)
# protein = dock_engine.blind_dock(protein1, protein)
# mutation = Mutation()
# foldx = FoldxAdaptor()
# protein = foldx.mutate(protein, mutation)
#
# from src.pipelines.fold_and_dock import FoldAndDock, FoldAndDock2
#
# fad = FoldAndDock(dock_engine, alphafold)
# fad.fold_and_dock(protein, sequence)
#
# fad2 = FoldAndDock2(dock_engine, alphafold)
# fad2.fit(protein, sequence)

# from src.core.atom import Atom
#
# atom = Atom()
# print(vars(atom))
#
# atom.set_a(77)
# print(vars(atom))
#
# atom.x(20)
# print(vars(atom))
#
# atom.x(10)
# print(vars(atom))
#
# atom.y(20)
# print(vars(atom))
#
# setattr(atom, "_z", 40)
# print(vars(atom))

names = ["A", "B", "C", "D", "E"]
a = [4, 10, 5, 9, 1]
print(a)

b = sorted(a)
print(b)
print(a)

a.sort()
print(a)

i = 1
j = 2

i = i + j
i += j
