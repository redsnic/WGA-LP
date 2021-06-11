import PySimpleGUI as sg
import traceback
import os
import subprocess
from mini_programs.decontamination_workflow import run_decontaminationPE
from mini_programs.decontamination_workflow import run_decontamination

if __name__ == "__main__":
    # Very basic window.  Return values using auto numbered keys

    layout = [
        [sg.Text('Press START to initiate the decontamination process')],
        [sg.Text('--- Non paired end mode ---')], 
        
        [sg.Text('Path to .fastq file:')],
        [sg.Input(key='_FASTQ_'), sg.FileBrowse()],

        [sg.Text('--- Paired end mode ---')],

        [sg.Text('Path to forward reads file (.fastq):')],
        [sg.Input(key='_FASTQ_FWD_'), sg.FileBrowse()],
        [sg.Text('Path to forward reads file (.fastq):')],
        [sg.Input(key='_FASTQ_REV_'), sg.FileBrowse()],

        [sg.Text('--- Common input ---')], 

        [sg.Text('Path to the reference(s) of the sequencing target(s) (.fasta, bwa indexed):')],
        [sg.Input(key='_REFS_'), sg.FilesBrowse()],
        [sg.Text('Path to the reference(s) of the contaminant(s) (.fasta, bwa indexed):')],
        [sg.Input(key='_CONTS_'), sg.FilesBrowse()],
        [sg.Text('Output folder:')],
        [sg.Input(key="_OUT_"), sg.FolderBrowse()],
        [sg.Text('Note: to index a reference genome run the command: ')],
        [sg.Text('bwa index path/to/the/reference.fasta')],
        [sg.Button("START"), sg.Button("QUIT")]
    ]


    window = sg.Window('Decontaminate FASTQ files', layout)
    while True:
        try:
            event, values = window.Read()

            print(values)

            if event in ("QUIT", None):
                break

            values["_FASTQ_"] = values["_FASTQ_"].strip()
            values["_FASTQ_FWD_"] = values["_FASTQ_FWD_"].strip()
            values["_FASTQ_REV_"] = values["_FASTQ_REV_"].strip()
            values["_OUT_"] = values["_OUT_"].strip()

            references = [ x.strip() for x in values["_REFS_"].split(";") ]
            contaminants = [ x.strip() for x in values["_CONTS_"].split(";") ]

            if not os.path.isdir(values["_OUT_"]):
                os.mkdir(values["_OUT_"])

            subprocess.Popen(["xdg-open", values["_OUT_"]])

            if values["_FASTQ_"] != '' and values["_FASTQ_FWD_"] == '' and values["_FASTQ_REV_"] == '':
                # non PE mode
                run_decontamination(values["_FASTQ_"], references, contaminants, values["_OUT_"])
            elif values["_FASTQ_"] == '' and values["_FASTQ_FWD_"] != '' and values["_FASTQ_REV_"] != '':
                
                run_decontaminationPE(values["_FASTQ_FWD_"], values["_FASTQ_REV_"], references, contaminants, values["_OUT_"])
            else:
                raise Exception("Error in .fastq input files. Please select either PE or non PE modes, do not provide both inputs")

            sg.Popup('Decontamination was completed sucessfully', keep_on_top=True)

        except Exception as e:
            tb = traceback.format_exc()
            sg.popup_error('An error happened:', e, tb)
