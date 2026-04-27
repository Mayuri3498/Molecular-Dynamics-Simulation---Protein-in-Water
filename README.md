# Molecular-Dynamics-Simulation: Protein-in-Water
Automated Python pipeline for performing Molecular Dynamics simulation using GROMACS for proteins in explicit water with ions. Structure preparation, solvation, ionisation, energy minimisation, NVT/NPT equilibration, and production MD and performing RMSD, RMSF, and energy analysis for efficient and scalable biomolecular simulations.

A protein binding pocket is a cavity or groove located on the surface or interior of a protein where small molecules, drugs, or ligands selectively bind. Accurately characterising these pockets is central to structure-based drug discovery (SBDD). However, since pharmacologically relevant pockets are inherently dynamic, static structural snapshots they are insufficient for effective Computer-Aided Drug Design (CADD).

Molecular Dynamics (MD) simulations play an important role in CADD for capturing the continuous conformational evolution of ligand binding pockets. The simulations apply complex quantum-mechanical forces governing atomic motion by modeling atoms and bonds as simple spheres connected by virtual springs striking a balance between physical accuracy and computational feasibility. This approach provides researchers with dynamic access to pharmacologically relevant conformational transitions, allosteric mechanisms, structural communication, and the opening and closing of transient druggable sub-pockets. By clustering diverse conformations sampled throughout an MD trajectory, researchers generate a representation of pocket geometries collectively termed a conformational ensemble which serves as a foundation for virtual screening, docking, and binding affinity studies.

The duration of an MD simulation directly governs the depth and diversity of conformational sampling. Short simulations primarily capture rapid molecular events such as local fluctuations, surface side-chain rotations, and fast loop reorientations. Whereas, longer simulations reveal how buried side-chain rotations, slow loop reorientations, and allosteric transitions reshape binding-pocket geometries, exposing druggable conformations that shorter simulations rarely sample. Hence, extended MD runs are particularly critical for identifying allosteric and cryptic binding sites of significant therapeutic relevance.

GROMACS is a versatile package which is used to perform molecular dynamics and simulation using the Newtonian equations of motions for the systems consisting of particles. The simulations were performed using GROMOS (version 23.5.0; www.gromos.net) and Gromacs software (version 2023.1) with the CHARMM36 force field and simple point charge (SPC) water. The entire MD simulation was performed with time step, constant pressure, and constant temperature of 2 fs, 1 atm 300 K, respectively. 

The protein was immerged into the cubic box with a minimum distance of 10 Å from the center to the box edge. The system was solvated using the transferable intermolecular potential with 3 points (TIP3P) water model. A required number of required Na+/Cl- ions were added to neutralize each of the systems. The steepest-descent algorithm was used to minimize each system for addressing the close contacts or overlaps between the atoms. To equally distribute the water molecules and ions around the system, each of the systems was equilibrated through NVT (constant number of particles, volume and temperature) followed by NPT (constant number of particles, pressure and temperature). On successful completion, the MD simulation trajectories were used to calculate several parameters including protein backbone RMSD, root-mean-square fluctuation (RMSF), radius of gyration (RoG), intramolecular H-bonds and solvent accessible surface area (SASA).


**REQUIREMENTS**
1. GROMACS v23.5.0
2. Prepared protein with fixed hydrogens, atoms, selected chain for running simulation.
3. CHARMM36 force field (https://mackerell.umaryland.edu/download.php?filename=CHARMM_ff_params_files/charmm36-jul2022.ff.tgz)
4. Download ions.mdp, minim.mdp, nvt.mdp, npt.mdp and md.mdp


**AUTOMATED PYTHON CODE**
1. Replace the protein input filename and enter the output filename in the Lysozyme_in_water.py python script.
2. Run the python code.
   
   _python3 Lysozyme_in_water.py_
   
4. All the files will be generated after the molecular dynamics simulation step.
5. Post-molecular dynamics simulation analysis are to be performed. Enter the md_tpr, md_xtc, em_tpr and output filename without extension. The protein center xtc file, protein rmsd, radius of gyration, rmsf, solvent accessible surface area and hydrogen bond .xvg files will be generated. Visualisation of these parameters can be analysed using graphs.
   
   _python3 Lysozyme_mda.py_

6. For visualisation of the plots rum visualisation.py code and input the .xvg files as input for generating the graph.

   _python3 visualisation.py_


**REFERENCES**
1. Kuzmanic A, Bowman GR, Juarez-Jimenez J, Michel J, Gervasio FL. Investigating Cryptic Binding Sites by Molecular Dynamics Simulations. Acc Chem Res. 2020 Mar 17;53(3):654-661. doi: 10.1021/acs.accounts.9b00613. Epub 2020 Mar 5. PMID: 32134250; PMCID: PMC7263906.
2. Ahmed M, Maldonado AM, Durrant JD. From byte to bench to bedside: molecular dynamics simulations and drug discovery. BMC Biol. 2023 Dec 29;21(1):299. doi: 10.1186/s12915-023-01791-z. PMID: 38155355; PMCID: PMC10755930.
3. Pronk S, Páll S, Schulz R, Larsson P, Bjelkmar P, Apostolov R, Shirts MR, Smith JC, Kasson PM, van der Spoel D, Hess B, Lindahl E. GROMACS 4.5: a high-throughput and highly parallel open source molecular simulation toolkit. Bioinformatics. 2013 Apr 1;29(7):845-54. doi: 10.1093/bioinformatics/btt055. Epub 2013 Feb 13. PMID: 23407358; PMCID: PMC3605599.
