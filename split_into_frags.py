#define the function SPLITINTOFRAGS to split a long sequence into fragments for Golden Gate Assembly
#sequence (a str)= the input DNA sequence 
#import Bio so that we can load and parse fasta/genbank files
#import xlsxwriter so that we can output the fragment sequences to a excel file
from Bio import SeqIO
import xlsxwriter
def splitIntoFrags(sequence):
    #calculate and output the length of the total input sequence in both bp and kb 
    seq_length = len(sequence)
    print('The length of the input sequence is %(length)i bp, or %(length_kb).3f kb'% {'length':seq_length,'length_kb':seq_length/1000})
   
    #convert the user input str max_num into int
    #set 2 as the default minimum # of fragments
    max_num = int(input('Please enter the maximum number of fragments:'))
    min_num = 2
    
    #create two lists for displaying the options for # of fragments & corresponding fragment lengths
    num_options = []
    length_options = []
    for i in range(max_num - min_num + 1):
        num_options.append(min_num + i)
        length_options.append(int(seq_length / num_options[i]))
     
    #output options
    print('You have the following options: number of fragments: ',num_options,'corresponding mean length per fragment',length_options)

    #let user choose the # of fragments and set it to target_num
    #output the sequences of split fragments according to user input
    target_num = int(input('Select the number of fragments you want: '))
    target_length = length_options[num_options.index(target_num)]
    frag_list = []
    for i in range(target_num):
        if i == target_num - 1:
            frag = sequence[int(target_length * i):]
        else: 
            frag = sequence[int(target_length * i):int(target_length * (i+1))]
        frag_list.append(frag)
        print('fragment sequence',i+1,frag)
    return target_num,frag_list

#define a function PARSESEQUENCE to read and validate sequences from fasta/genbank files
#file_name (a str) = the name of the input file (e.g.'test.fa')
#file_type (a str) = the type of the input file (e.g. 'fasta')
def parseSequence(file_name,file_type):
    #read a list of SequenceRecord Objects from the file
    seq_list = list(SeqIO.parse(file_name, file_type))

    #extract the actual sequences, turn them into strings and place them into a list called target_seq_list
    target_seq_list = []
    for i in range(len(seq_list)):
        length = int(len(seq_list[i].seq))
        seq = str(seq_list[i].seq[0:length])
        target_seq_list.append(seq)
    
    #iterate through each sequence in the list and check for invalid base
    for i in range(len(target_seq_list)):
        for j in range(len(target_seq_list[i])):
            if target_seq_list[i][j]!= 'a' and target_seq_list[i][j]!= 'A'and target_seq_list[i][j]!= 't'and target_seq_list[i][j]!= 'T'and target_seq_list[i][j]!= 'c'and target_seq_list[i][j]!= 'C'and target_seq_list[i][j]!= 'g'and target_seq_list[i][j]!= 'G':
                print('The sequence you put contains invalid base, please check your file')
    return  target_seq_list      
    
#create an excel file for storing the output
workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()
target_seq_list = parseSequence('test2.fa','fasta')

#iterate through and split each sequence in the list, write the output fragment sequences in the excel file
for i in range(len(target_seq_list)):
    num,frag_list = splitIntoFrags(target_seq_list[i])
for k in range(num):
    worksheet.write(k,i,frag_list[k])
workbook.close()
