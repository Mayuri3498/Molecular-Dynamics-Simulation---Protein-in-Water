import os
import sys
from subprocess import Popen, STDOUT, PIPE, call


path = os.getcwd()

tpr_file = input("Enter the md tpr file: ")
xtc_file = input("Enter the xtc file: ")
tpr_em = input("Enter the energy minimisation tpr file: ")
outfile = input("Enter the outfile name (name only...don't add file extension.): ")


#RMSD Graph (Root Mean Square Deviation)
md_tpr = os.path.join(path, tpr_file)
md_xtc = os.path.join(path, xtc_file)
em_tpr = os.path.join(path, tpr_em)
if os.path.isfile(md_tpr) and os.path.isfile(md_xtc):
    sd = False
    center_xtc_file = os.path.join(path, "md_"+outfile+"_center.xtc")
    try:
        print("protein center xtc file")
        cmd = "gmx trjconv -s "+md_tpr+" -f "+md_xtc+" -o "+center_xtc_file+" -center -pbc mol -ur compact"
        center = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        center.stdin.write(b"1 \n\n 0")
        center.stdin.flush()
        output = center.communicate()
        print("Protein center xtc file created.")
    except:
        print(output[0].decode('utf-8'))

    if os.path.isfile(center_xtc_file):
        try:
            print("Protein RMSD Graph:")
            cmd = "gmx rms -s "+md_tpr+" -f "+center_xtc_file+" -o protein_rmsd_"+outfile+".xvg -tu ns"
            rmsd = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            rmsd.stdin.write(b"4 \n\n 4")
            rmsd.stdin.flush()
            output = rmsd.communicate()
            print("Protein RMSD xvg file created.")
        except:
            print(output[0].decode('utf-8'))
     
#RoG Graph (Radius of gyration)
        try:
            print("Gyration Graph")
            cmd = "gmx gyrate -s "+md_tpr+" -f "+center_xtc_file+" -o gyrate_"+outfile+".xvg -tu ns"
            gyrate = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            gyrate.stdin.write(b"1")
            gyrate.stdin.flush()
            output = gyrate.communicate()
            print("Gyration xvg file created!")
        except:
            print(output[0].decode('utf-8'))

#RMSF (Root Mean Square Fluctuation)
        try:
            print("RMSF Graph")
            cmd = "gmx rmsf -s "+md_tpr+" -f "+center_xtc_file+" -o rmsf_"+outfile+".xvg -res"
            rmsf = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            rmsf.stdin.write(b"1")
            rmsf.stdin.flush()
            output = rmsf.communicate()
            print("RMSF xvg file created!")
        except:
            print(output[0].decode('utf-8'))

        try:
            #hbond_outfile = inut("output filename for hbond graph: ")
            cmd = "gmx hbond -s "+md_tpr+" -f "+center_xtc_file+" -num hbond_"+outfile+".xvg"
            hbond = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            hbond.stdin.write(b"1 \n\n 13")
            hbond.stdin.flush()
            output = hbond.communicate()
            print('Hbond xvg file created.')
        except:
            print(output[0].decode('utf-8'))

#SASA (Solvent Accessible Surface Area)
        try:
            print("SASA graph")
            cmd = "gmx sasa -s "+md_tpr+" -f "+center_xtc_file+" -o sasa"+outfile+".xvg -tu ns"
            sasa = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
            sasa.stdin.write(b"1")
            sasa.stdin.flush()
            output = sasa.communicate()
            print('SASA xvg file created')
        except:
            print(output[0].decode('utf-8'))

else:
    print("File not found error")
