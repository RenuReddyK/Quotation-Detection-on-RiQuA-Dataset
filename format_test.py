# Convert files from brat annotated format to CoNLL format
from os import listdir, path
from collections import namedtuple
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input_dir",
    dest="input_dir",
    type=str,
    default='',
    help="Input directory where Brat annotations are stored",
)

parser.add_argument(
    "--output_file",
    dest="output_file",
    type=str,
    default='',
    help="Output file where CoNLL format annotations are saved",
)

class FormatConvertor:
    def __init__(self, input_dir: str, output_file: str):
        self.input_dir = input_dir
        self.output_file = output_file

    def read_input(self, annotation_file: str, text_file: str):
        """Read the input BRAT files into python data structures
        Parameters
            annotation_file:
                BRAT formatted annotation file
            text_file:
                Corresponding file containing the text as a string
        Returns
            input_annotations: list
                A list of dictionaries in which each entry corresponds to one line of the annotation file
            text_string: str
                Input text read from text file
        """
        with open(text_file, 'r') as f:
            text_string = f.read()
        input_annotations = []
        
        # Read each line of the annotation file to a dictionary
        with open(annotation_file, 'r') as fi:
            for line in fi:
                annotation_record = {}
                entry = line.split()
                if entry[0] == "R1":
                    break
                start = int(entry[2])
                end = int(entry[3])
                annotation_record["label"] = entry[1]
                annotation_record["start"] = start
                annotation_record["end"] = end
                annotation_record["text"] = ' '.join(entry[4:])
                input_annotations.append(annotation_record)
                
        # Annotation file need not be sorted by start position so sort explicitly. Can also be done using end position
        input_annotations = sorted(input_annotations, key=lambda x: x["start"])

        return input_annotations, text_string

    def parse_text(self):
        """Loop over all annotation files, and write tokens with their label to an output file"""
        file_pair_list = self.read_input_folder()

        with open(self.output_file, 'w') as fo:
            for file_count, file_pair in enumerate(file_pair_list):
                annotation_file, text_file = file_pair.ann, file_pair.text  

                input_annotations, text_string = self.read_input(annotation_file, text_file)
                fo.write("\n")
                fo.write("-DOCSTART- O\n")
                old_token = ""


                new_input_annotations = []
                old_start = -1
                old_end = -1
                temp_ann = []
                for i in range(len(input_annotations)):
                    curr_start = input_annotations[i]["start"]
                    curr_end = input_annotations[i]["end"]
                    if curr_start <= old_end and curr_end <= old_end:
                        continue
                    elif curr_start <= old_end and curr_end > old_end:
                        curr_start = old_end+1
                    annotation_record = {}
                    annotation_record["label"] = input_annotations[i]["label"]
                    annotation_record["start"] = curr_start
                    annotation_record["end"] = curr_end
                    annotation_record["text"] = input_annotations[i]["text"]
                    new_input_annotations.append(annotation_record) 

                    old_end = curr_end
                    old_start = curr_start  

                for i in range(len(new_input_annotations)):
                    curr_start = new_input_annotations[i]["start"]
                    curr_end = new_input_annotations[i]["end"]
                    if curr_start > 3500 or curr_start < 3000:
                        continue
                    temp_ann.append(new_input_annotations[i])

                curr_ann_index = 0
                curr_ann_start = new_input_annotations[curr_ann_index]["start"]
                curr_ann_end = new_input_annotations[curr_ann_index]["end"]
                curr_label = new_input_annotations[curr_ann_index]["label"]
                curr_token = ""
                i = 0
                while i<len(text_string):
     
                    if i==curr_ann_start:
                        # print("first")
                        if curr_token.strip("-") != "":
                            fo.write(f'{curr_token.strip("-")} O\n')
                            if (curr_token.strip("-"))[-1] == "." and  curr_token.strip("-") not in ['Mrs.','Mr.', 'Dr.']:
                                fo.write('\n')
                            curr_token = ""
                        j = i
                        first_token = 0
                        while j<=curr_ann_end:
                            # print(j)
                            # print(curr_token)
                            if text_string[j] == " ":
                                if curr_token.strip("-") != "":
                                    first_token+=1
                                    if first_token <= 1:
                                        label_to_write = "B-"+curr_label
                                    else:
                                        label_to_write = "I-"+curr_label  
                                    fo.write(f'{curr_token.strip("-")} {label_to_write}\n')
                                    if (curr_token.strip("-"))[-1] == "." and  curr_token.strip("-") not in ['Mrs.','Mr.', 'Dr.']:
                                        fo.write('\n')
                                    curr_token = ""
                            else:
                                curr_token +=  text_string[j]
                            j+=1
                        if curr_token.strip("-") != "":
                            if first_token <= 1:
                                label_to_write = "B-"+curr_label
                            else:
                                label_to_write = "I-"+curr_label 
                            fo.write(f'{curr_token.strip("-")} {label_to_write}\n')
                            if (curr_token.strip("-"))[-1] == "." and  curr_token.strip("-") not in ['Mrs.','Mr.', 'Dr.']:
                                fo.write('\n')
                            curr_token = ""
                        i = j
                        curr_ann_index += 1
                  
                        if curr_ann_index < len(new_input_annotations):
                            curr_ann_start = new_input_annotations[curr_ann_index]["start"]
                            curr_ann_end = new_input_annotations[curr_ann_index]["end"]
                            curr_label = new_input_annotations[curr_ann_index]["label"]
                    else:
                        if text_string[i] == " ":
                            if curr_token.strip("-") != "":
                                fo.write(f'{curr_token.strip("-")} O\n')
                                if (curr_token.strip("-"))[-1] == "." and  curr_token.strip("-") not in ['Mrs.','Mr.', 'Dr.']:
                                    fo.write('\n')
                                curr_token = ""
                        else:
                            curr_token +=  text_string[i]
                        i+=1   

                    
              
    
    def read_input_folder(self):
        """Read multiple annotation files from a given input folder"""
        file_list = listdir(self.input_dir)
        annotation_files = sorted([file for file in file_list if file.endswith('.ann')])
        # print(annotation_files)
        file_pair_list = []
        file_pair = namedtuple('file_pair', ['ann', 'text'])
        # The folder is assumed to contain *.ann and *.txt files with the 2 files of a pair having the same file name
        for file in annotation_files:
            if file.replace('.ann', '.txt') in file_list:
                file_pair_list.append(file_pair(path.join(self.input_dir, file), path.join(self.input_dir, file.replace('.ann', '.txt'))))
            else:
                raise(f"{file} does not have a corresponding text file")
        
        return file_pair_list
            
