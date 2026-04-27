import os
import sys
from subprocess import Popen, STDOUT, PIPE, call
import logging


logging.basicConfig(filename='mdhistory.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

logger.info("##################################### New Folder #########################################")

path = os.getcwd()
protein = os.path.join(path, '1M17_rec.pdb')
md_output = "md_1M17.tpr"
protein_name = protein.strip('\.pdb') or protein.strip('\.PDB')

def system_preparation():
    #Generating TOPOLOGY files
    logger.info("Generating TOPOLOGY files")
    logger.info("Running pdb2gmx...")
    global pdb2gmx
    protein_file = os.path.join(path, protein)
    if os.path.isfile(protein_file):
        try:
            cmd = "echo '1'|gmx pdb2gmx -f "+protein_file+" -o proc.pdb -water tip3p -ignh"
            proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = proc.communicate()
            #logger.info(output[0].decode('utf_8'))
            logger.info("Topology files generated.")
            pdb2gmx =True
        except:
            logger.error(output[0].decode('utf-8'))

    #SOLVATION
    global solvation
    if topol == True:
        logger.info("Running Solvation...")
        complex_file = os.path.join(path, 'complex.pdb')
        global newbox
        if os.path.isfile(complex_file):
            try:
                cmd ="gmx editconf -f "+complex_file+" -o newbox.pdb -bt cubic -d 1.0"
                proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                output = proc.communicate()
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
                    proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                    output = proc.communicate()
                    logger.info(output[0].decode('utf_8'))
                    logger.info("Solvation completed.")
                    solvation =True
                except :
                    logger.error(output[0].decode('utf-8'))


    #ADD IONS
    if solvation == True:
        logger.info("Add ions step ...")
        ions_mdp = os.path.join(path, 'ions.mdp')
        solv_file = os.path.join(path, 'solv.pdb')
        topology = os.path.join(path, 'topol.top')
        global ions
        if os.path.isfile(ions_mdp) and os.path.isfile(solv_file):
            try:
                cmd = "gmx grompp -f "+ions_mdp+" -c "+solv_file+" -p "+topology+" -o ions.tpr -maxwarn -1"
                proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                output = proc.communicate()
                logger.info(output[0].decode('utf_8'))
                logger.info(" Ions tpr file created.")
                ions =True
            except :
                logger.error(output[0].decode('utf-8'))

        if ions == True:
            ions_tpr = os.path.join(path, 'ions.tpr')
            topology = os.path.join(path, 'topol.top')
            if os.path.isfile(ions_tpr):
                try:
                    cmd = "echo '15'|gmx genion -s "+ions_tpr+" -o solv_ions.pdb -p "+topology+" -pname NA -nname CL -neutral"
                    proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                    output = proc.communicate()
                    logger.info(output[0].decode('utf_8'))
                    logger.info(" Protein neutralization is done.")
                except :
                    logger.error(output[0].decode('utf-8'))



#Energy Minimization
def energy_minimization():
    global equil
    logger.info("Energy Minimization step...")
    em_mdp = os.path.join(path, 'em.mdp')
    topology = os.path.join(path, 'topol.top')
    solv_ions = os.path.join(path, 'solv_ions.pdb')
    if os.path.isfile(em_mdp):
        global e_md
        try:
            cmd = "gmx grompp -f "+em_mdp+" -c "+solv_ions+" -p "+topology+" -o em.tpr -maxwarn -1"
            proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = proc.communicate()
            logger.info(output[0].decode('utf_8'))
            logger.info(" Em tpr file created.")
            e_md =True
        except :
            logger.error(output[0].decode('utf-8'))

        if e_md ==True:
            em_tpr = os.path.join(path, 'em.tpr')
            if os.path.isfile(em_tpr):
                try:
                    cmd ="gmx mdrun -v -deffnm em -nb gpu"
                    proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                    output = proc.communicate()
                    logger.info(output[0].decode('utf_8'))
                    logger.info(" Energy Minimization is done.")
                    equil =True
                except :
                    logger.error(output[0].decode('utf-8'))

    equil = True
    
#NVT Equilibration

def equilibration():
    global nvt_md
    logger.info("NVT Equilibration step...")
    topology = os.path.join(path, 'topol.top')
    em_gro = os.path.join(path, 'em.gro')
    nvt_mdp = os.path.join(path, 'nvt.mdp')
    global nvt
        try:
            cmd = "gmx grompp -f "+nvt_mdp+" -c "+em_gro+" -r "+em_gro+" -p "+topology+" -o nvt.tpr -maxwarn -1"
            proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = proc.communicate()
            # logger.info(output[0].decode('utf_8'))
            logger.info("NVT.tpr file created.")
            nvt =True
        except :
            logger.error(output[0].decode('utf-8'))
    if nvt == True:
        nvt_tpr = os.path.join(path, 'nvt.tpr')
        if os.path.isfile(nvt_tpr):
            try:
                cmd = "gmx mdrun -deffnm nvt -nb gpu"
                proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                output = proc.communicate()
                # logger.info(output[0].decode('utf_8'))
                nvt_md =True
                logger.info("NVT Equilibration step is done.")
            except :
                logger.error(output[0].decode('utf-8'))



    #NPT Equilibration
    if nvt_md == True:
        logger.info("NPT Equilibration Step")
        topology = os.path.join(path, 'topol.top')
        nvt_gro = os.path.join(path, 'nvt.gro')
        nvt_cpt = os.path.join(path, 'nvt.cpt')
        npt_mdp = os.path.join(path, 'npt.mdp')
        if os.path.isfile(npt_mdp) and os.path.isfile(nvt_gro) and os.path.isfile(nvt_cpt):
            global npt
            try:
                cmd = "gmx grompp -f "+npt_mdp+" -c "+nvt_gro+" -t "+nvt_cpt+" -r "+nvt_gro+" -p "+topology+" -o npt.tpr -maxwarn -1"
                proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                output = proc.communicate()
                logger.info(output[0].decode('utf_8'))
                logger.info("NPT.tpr file created.")
                npt =True
            except :
                logger.error(output[0].decode('utf-8'))

            if npt == True:
                npt_tpr =os.path.join(path, 'npt.tpr')
                if os.path.isfile(os.path.join(path, 'npt.tpr')):
                    try:
                        cmd = "gmx mdrun -deffnm npt -nb gpu"
                        proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                        output = proc.communicate()
                        logger.info("NPT Equilibration step is done.")
                    except :
                        logger.error(output[0].decode('utf-8'))


#MD Simulation
def md_simulation():
    logger.info("MD Simulation Step")
    topology = os.path.join(path, 'topol.top')
    npt_gro = os.path.join(path, 'npt.gro')
    npt_cpt = os.path.join(path, 'npt.cpt')
    md_mdp = os.path.join(path, 'md.mdp')
    if os.path.isfile(md_mdp) and os.path.isfile(npt_gro) and os.path.isfile(npt_cpt):
        global md
        try:
            cmd = "gmx grompp -f "+md_mdp+" -c "+npt_gro+" -t "+npt_cpt+" -p "+topology+" -o "+md_output+" -maxwarn -1"
            proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            output = proc.communicate()
            logger.info(output[0].decode('utf_8'))
            md = True
            logger.info("md.tpr file created.")
        except :
            logger.error(output[0].decode('utf-8'))
        if md ==True:
            try:
                md_out = md_output.strip('\.tpr')
                cmd = "gmx mdrun -deffnm "+md_out+" -nb gpu"
                proc = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
                output = proc.communicate()
                logger.info(output[0].decode('utf_8'))
                logger.info("MD Simulation is done.")
            except :
                logger.error(output[0].decode('utf-8'))

logger.info("###############################  End Project ####################################")


if __name__ == '__main__':
    system_preparation()
    energy_minimization()
    equilibration()
    md_simulation()

# logger.info("### MD Simulation ###")

# logger.info(" MD Simulation steps: \n\ 1 : System preparation,\n 2 : Energy Minimization,\n 3 : Equilibration,\n 4 : MD simulation\n")

# user_input = [int(i) for i in input("Select the options which step you need to run in MD simulation: ").split()]
# logger.info(user_input)
# for i in user_input:
#     if i == 1:
#         system_preparation()
#     elif i == 2:
#         energy_minimization()
#     elif i ==3:
#         equilibration()
#     elif i == 4:
#         md_simulation()
