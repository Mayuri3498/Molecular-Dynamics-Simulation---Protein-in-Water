import os
import sys
from subprocess import Popen, STDOUT, PIPE, call
import logging


logging.basicConfig(filename='mdhistory.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

logger.info("##################################### New Folder #########################################")

path = os.getcwd()
protein = os.path.join(path, 'CA_1HEA_prep.pdb')
md_output = "md_1HEA.tpr"
protein_name = os.path.splitext(protein)[0]

def system_preparation():
    #Generating TOPOLOGY files
    logger.info("Generating TOPOLOGY files")
    logger.info("Running pdb2gmx...")
    global pdb2gmx
    protein_file = os.path.join(path, protein)
    if os.path.isfile(protein_file):
        try:
            cmd = "echo '1'|gmx pdb2gmx -f "+protein_file+" -o prep.pdb -water tip3p -ignh"
            protein_fix = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = protein_fix.communicate()
            #logger.info(output[0].decode('utf_8'))
            logger.info("Topology files generated.")
            pdb2gmx =True
        except:
            logger.error(output[0].decode('utf-8'))
            
    global topol
    if pdb2gmx == True:
        logger.info("Generating topology files")
        topology = os.path.join(path, 'topol.top')
        topol = True

#SOLVATION
    global solvation
    solvation = False
    if topol == True:
        logger.info("Running Solvation...")
        protein_fix = os.path.join(path, 'prep.pdb')
        global newbox
        if os.path.isfile(protein_fix):
            try:
                cmd ="gmx editconf -f "+protein_fix+" -o newbox.pdb -bt cubic -d 1.0"
                protein_fix = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                output = protein_fix.communicate()
                logger.info(output[0].decode('utf_8'))
                logger.info("The Box type and box dimension step completed.")
                newbox =True
            except :
                logger.error(output[0].decode('utf-8'))
            
        if newbox == True:
            newbox = os.path.join(path, 'newbox.pdb')
            topology = os.path.join(path, 'topol.top')
            if os.path.isfile(newbox):
                try:
                    cmd = "gmx solvate -cp "+newbox+" -cs spc216.gro -p "+topology+" -o solv.pdb"
                    protein_fix = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                    output = protein_fix.communicate()
                    logger.info(output[0].decode('utf_8'))
                    logger.info("Solvation completed.")
                    solvation =True
                    topology = os.path.join(path, 'topol.top')
                    if os.path.isfile(topology):
                        try:
                            with open(topology, 'r') as f:
                                for line in f:
                                    if line.strip().startswith("SOL"):
                                        sol_count = line.split()[1]
                                        logger.info(f"Number of water molecules (SOL) added: {sol_count}")
                                        print("Number of water molecules (SOL) added to system:", sol_count)
                        except Exception as e:
                            logger.error(f"Error reading topology file: {e}")
                except :
                    logger.error(output[0].decode('utf-8'))


# ADD IONS
    if solvation:
        logger.info("Add ions step...")
        ions_mdp = os.path.join(path, 'ions.mdp')
        solv_file = os.path.join(path, 'solv.pdb')
        topology = os.path.join(path, 'topol.top')
        global ions
        ions = False

        # Step 1: Create ions.tpr using grompp
        if os.path.isfile(ions_mdp) and os.path.isfile(solv_file):

            cmd = "gmx grompp -f " + ions_mdp + " -c " + solv_file + " -p " + topology + " -o ions.tpr -maxwarn 1"
            logger.info("Running grompp to generate ions.tpr")
            protein_fix = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            output = protein_fix.communicate()[0].decode()

            logger.info(output)

            # Check if ions.tpr was created
            if os.path.isfile("ions.tpr"):
                logger.info("ions.tpr successfully created.")
                ions = True
            else:
                logger.error("ions.tpr was NOT created. Check grompp errors above.")

        else:
            logger.error("ions.mdp or solv.pdb file missing.")

        # Step 2: Add ions using genion
        if ions:

            ions_tpr = os.path.join(path, "ions.tpr")
            logger.info("Running genion to add ions")
            cmd = "echo SOL | gmx genion -s " + ions_tpr + " -o solv_ions.pdb -p " + topology + " -pname NA -nname CL -neutral"
            process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            output = process.communicate()[0].decode()
            logger.info(output)
            if os.path.isfile("solv_ions.pdb"):
                logger.info("Ions added successfully. System neutralized.")
            else:
                logger.error("genion failed. solv_ions.pdb not created.")
                
# Energy Minimization
def energy_minimization():
    logger.info("Energy Minimization step...")
    em_mdp = os.path.join(path, 'em.mdp')
    topology = os.path.join(path, 'topol.top')
    solv_ions = os.path.join(path, 'solv_ions.pdb')

    global e_md
    e_md = False
    if not os.path.isfile(em_mdp):
        logger.error("em.mdp file not found.")
        return
    if not os.path.isfile(solv_ions):
        logger.error("solv_ions.pdb file not found. Ion addition step failed.")
        return
    try:
        cmd = "gmx grompp -f " + em_mdp + " -c " + solv_ions + " -p " + topology + " -o em.tpr -maxwarn 1"
        logger.info("Running grompp to generate em.tpr")
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        output = process.communicate()[0].decode()
        logger.info(output)

        if os.path.isfile("em.tpr"):
            logger.info("em.tpr file successfully created.")
            e_md = True
        else:
            logger.error("em.tpr was NOT created. Check grompp errors.")

    except Exception as e:
        logger.error(str(e))

    if e_md:
        logger.info("Running mdrun for Energy Minimization")
        try:
            cmd = "gmx mdrun -v -deffnm em"
            process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            output = process.communicate()[0].decode()
            logger.info(output)
            if os.path.isfile("em.gro"):
                logger.info("Energy Minimization completed successfully.")
            else:
                logger.error("Energy Minimization failed. em.gro not generated.")
        except Exception as e:
            logger.error(str(e))

#equil = True
    
# NVT Equilibration
def equilibration():
    logger.info("Starting NVT Equilibration")
    topology = os.path.join(path, "topol.top")
    em_gro = os.path.join(path, "em.gro")
    nvt_mdp = os.path.join(path, "nvt.mdp")
    global nvt
    global nvt_md
    nvt = False
    nvt_md = False

    if not os.path.isfile(nvt_mdp):
        logger.error("nvt.mdp file not found")
        return
    if not os.path.isfile(em_gro):
        logger.error("em.gro not found. Energy minimization failed.")
        return
    if not os.path.isfile(topology):
        logger.error("topol.top not found")
        return

    try:
        cmd = "gmx grompp -f " + nvt_mdp + " -c " + em_gro + " -r " + em_gro + " -p " + topology + " -o nvt.tpr -maxwarn 1"
        logger.info("Running grompp to create nvt.tpr")
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        output = process.communicate()[0].decode()
        logger.info(output)
        if os.path.isfile("nvt.tpr"):
            logger.info("nvt.tpr successfully created")
            nvt = True
        else:
            logger.error("nvt.tpr not created. Check grompp errors.")

    except Exception as e:
        logger.error(str(e))

    if nvt:
        logger.info("Running NVT simulation")
        try:
            cmd = "gmx mdrun -deffnm nvt"
            process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            output = process.communicate()[0].decode()
            logger.info(output)
            if os.path.isfile("nvt.gro"):
                logger.info("NVT equilibration completed")
                nvt_md = True
            else:
                logger.error("NVT run failed. nvt.gro not generated")
        except Exception as e:
            logger.error(str(e))

# NPT Equilibration
    if nvt_md:
        logger.info("NPT Equilibration Step")
        topology = os.path.join(path, 'topol.top')
        nvt_gro = os.path.join(path, 'nvt.gro')
        nvt_cpt = os.path.join(path, 'nvt.cpt')
        npt_mdp = os.path.join(path, 'npt.mdp')
        global npt
        global npt_md
        npt = False
        npt_md = False
        if not os.path.isfile(npt_mdp):
            logger.error("npt.mdp file not found")
            return
        if not os.path.isfile(nvt_gro):
            logger.error("nvt.gro not found")
            return
        if not os.path.isfile(topology):
            logger.error("topol.top not found")
            return
        try:
            cmd = "gmx grompp -f " + npt_mdp + " -c " + nvt_gro + " -t " + nvt_cpt + " -r " + nvt_gro + " -p " + topology + " -o npt.tpr -maxwarn 1"
            process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            output = process.communicate()[0].decode()
            logger.info(output)
            if os.path.isfile("npt.tpr"):
                logger.info("npt.tpr successfully created")
                npt = True
            else:
                logger.error("npt.tpr not created. Check grompp errors.")

        except Exception as e:
            logger.error(str(e))

        if npt:
            logger.info("Running NPT Equilibration")
            try:
                cmd = "gmx mdrun -deffnm npt"
                process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
                output = process.communicate()[0].decode()
                logger.info(output)
                if os.path.isfile("npt.gro"):
                    logger.info("NPT equilibration completed")
                    npt_md = True
                else:
                    logger.error("NPT run failed. npt.gro not generated")

            except Exception as e:
                logger.error(str(e))
# MD Simulation
def md_simulation():
    logger.info("MD Simulation Step")
    topology = os.path.join(path, 'topol.top')
    npt_gro = os.path.join(path, 'npt.gro')
    npt_cpt = os.path.join(path, 'npt.cpt')
    md_mdp = os.path.join(path, 'md.mdp')
    global md
    md = False
    if not os.path.isfile(md_mdp):
        logger.error("md.mdp file not found")
        return
    if not os.path.isfile(npt_gro):
        logger.error("npt.gro not found. NPT step failed.")
        return
    if not os.path.isfile(npt_cpt):
        logger.error("npt.cpt not found.")
        return
    if not os.path.isfile(topology):
        logger.error("topol.top not found.")
        return
    try:
        cmd = "gmx grompp -f " + md_mdp + " -c " + npt_gro + " -t " + npt_cpt + " -p " + topology + " -o " + md_output + " -maxwarn 1"
        logger.info("Running grompp to generate MD tpr file")
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        output = process.communicate()[0].decode()
        logger.info(output)
        if os.path.isfile(md_output):
            logger.info("MD tpr file created successfully.")
            md = True
        else:
            logger.error("MD tpr file was NOT created. Check grompp errors.")

    except Exception as e:
        logger.error(str(e))

    if md:
        logger.info("Running MD simulation")
        try:
            md_out = os.path.splitext(md_output)[0]
            cmd = "gmx mdrun -deffnm " + md_out
            process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            output = process.communicate()[0].decode()
            logger.info(output)
            if os.path.isfile(md_out + ".gro"):
                logger.info("MD Simulation completed successfully.")
            else:
                logger.error("MD run finished but output .gro file not found.")

        except Exception as e:
            logger.error(str(e))
if __name__ == '__main__':
    system_preparation()
    energy_minimization()
    equilibration()
    md_simulation()
