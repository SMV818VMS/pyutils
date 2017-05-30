#!/usr/bin/env python

import subprocess
import matplotlib.pyplot as plt
import collections
import numpy as np
from Bio import SeqIO

# Several easy scripts in order to perform simple processes

def indexes(lista, values):
    """
    Given a list and its values return a list with the indexes of the values
    in lista
    """

    indexes = []
    for element in values:
        indexes.append(lista.index(element))
    return indexes


def list_generator(filename, index=0):
    """
    Given a file, returns a set with all the values from the column[index]
    """
    results = []
    with open(filename, 'r') as fi:
        for line in fi:
            line = line.strip().split()
            results.append(line[index])
    return results


def ins2positions(filename):
    """
    Given a ins file extract all the positions and returns them in a set
    """

    with open(filename, 'rU') as fi:
        return set([int(line.split()[0]) for line in fi.readlines()])


def set_generator(filename, index):
    """
    Given a file, returns a set with all the values from the column[index]
    """
    results = set()
    with open(filename, 'r') as fi:
        for line in fi:
            line = line.strip().split()
            results.add(line[index])
    return results


def dic_generator(filename, key_index, value_index=None, header=False):
    """
    Given a file, returns a dictionary where {key_index:key_index+1}
    """
    results = {}
    with open(filename, 'r') as fi:
        for line in fi:
            if header:
                header=False
            else:
                line = line.strip().split()
                if not value_index:
                    results[int(line[key_index])] = float(line[key_index+1])
                else:
                    results[int(line[key_index])] = float(line[value_index])
    return results

def new_dic_generator(filename, key_index, value_index):
    """
    Given a file, returns a dictionary where {key_index:key_index+1}
    """
    results = {}
    with open(filename, 'r') as fi:
        results = {int(k):float(v) for k, v in [l.split()[0:2] for l in fi.readlines()]}
    return results

def str_dic_generator(filename, key_index, value_index=None, header=False, split_by=None):
    """
    Given a file, returns a dictionary where {key_index:key_index+1}
    """
    if header==True:
        header = 1

    results = {}
    with open(filename, 'r') as fi:
        for line in fi:
            if header != 0:
                header-=1
            else:
                if split_by:
                    line = line.strip().split(split_by)
                else:
                    line = line.strip().split()
                if value_index !=  key_index+1:
                    results[line[key_index]] = line[value_index]
                else:
                    results[line[key_index]] = line[key_index+1]
    return results


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


def double_set_generator(filename, index):
    """
    Given a file, returns two sets with all the values from the column[index]. The first set includes
    those positions appearing in both replicas and the thirs those appearing in only one
    """

    rep_results = set()
    nonrep_results = set()

    with open(filename, 'r') as fi:
        for line in fi:
            line = line.strip().split()
            try:
                if int(line[2]) == 2:
                    rep_results.add(line[0])
            except:
                nonrep_results.add(line[0])

    return (rep_results, nonrep_results)

def genes_coordinates(caps = True):
    """
    Given a three colums file returns a dictionary where the first column is the key and the other are the values
    in a list
    """

    results_dic = {}

    with open('/home/smiravet/crg/transpgrowth/datasets/essentials/gene_coordinates.txt', 'r') as fi:
        for line in fi:
            line = line.strip().split()
            if caps:
                results_dic[line[0].upper()] = [line[1], line[2]]
            else:
                results_dic[line[0]] = [line[1], line[2]]

    return results_dic

def return_ene_set(region_type):
    """
    Given E or NE return the genes with that feature
    """
    results_set = set()
    with open('/home/smiravet/crg/transpgrowth/datasets/essentials/goldsets.csv', 'r') as fi:
        for line in fi:
            line = line.strip().split()
            if line[1] == region_type:
                results_set.add(line[0].upper())
    return results_set


def process_ene_set(ENE_set, gene_coord_dic, percentage = 10):
    """
    Generate new dictionaries with the genes appearing in the NE E list and the 10% of the ORF removed (5% per side)
    """

    ENE_dic = {}

    # For the essential set
    for gene in ENE_set:
        # restore the start and end
        start = int(gene_coord_dic[gene][0])
        end = int(gene_coord_dic[gene][1])
        length = end - start
        bases_to_remove = int(round(length*(percentage/2)*0.01))
        new_start = start + bases_to_remove
        new_end = end - bases_to_remove

        ENE_dic[gene] = [new_start, new_end]

    return ENE_dic


def return_two_list(filename):
    """
    Given a file with position reads, returns two lists with those values in order to easy plot them
    """
    positions_list = []
    reads_list = []

    with open(filename, 'r') as fi:
        for line in fi:
            line = line.strip().split()
            position = int(line[0])
            reads = float(line[1])
            positions_list.append(position)
            try:
                if line[2] == '2':
                    reads_list.append(reads)
            except:
                reads_list.append(reads)

    return positions_list, reads_list


def mapping_figure(datasetA, datasetB, spanning = False):
    """
    Function to retrieve map reads per position for all the genome of pneumoniae
    """

    if spanning:
        gene_coord = gene_coordinates_dic()
        n += 1

        # Span ENE regions
        with open('/home/smiravet/crg/transpgrowth/datasets/essentials/goldsets.csv', 'r') as fi:
            for line in fi:
                line = line.strip().split()
                if line[-1] == 'E':
                    plt.axvspan(gene_coord[line[0].upper()][0], gene_coord[line[0].upper()][1], facecolor='b', alpha=0.1)
                else:
                    plt.axvspan(gene_coord[line[0].upper()][0], gene_coord[line[0].upper()][1], facecolor='g', alpha=0.1)

    # Set figure width to 24 and height to 9
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 40
    fig_size[1] = 9
    plt.rcParams["figure.figsize"] = fig_size

    # Extract the information from the nc and the rrn files
    dataA = return_two_list('/home/smiravet/crg/transpgrowth/datasets/'+datasetA)
    dataB = return_two_list('/home/smiravet/crg/transpgrowth/datasets/'+datasetB)

    plt.subplot(2, 1, 1)
    plt.title('mapping '+datasetA+' and '+datasetB)
    plt.xlim([0,816394])
    plt.bar(dataA[0], dataA[1], alpha = 0.6)
    plt.ylabel(datasetA.replace('.ins',''))

    plt.subplot(2, 1, 2)
    plt.xlim([0,816394])
    plt.bar(dataB[0], dataB[1], alpha = 0.6)
    plt.ylabel(datasetB.replace('.ins',''))

    plt.savefig('/home/smiravet/crg/transpgrowth/results/mapping/'+datasetA.replace('/','_').replace('.ins','')+datasetB.replace('/','_').replace('.ins','')+'.pdf')


def mapping_figure_from_dictionary(your_dictionary):
    # Extract the information from the nc and the rrn files

    listA= [int(k) for k,v in your_dictionary.iteritems()]
    listB= [int(v) for k,v in your_dictionary.iteritems()]

    plt.title('mapping')
    plt.xlim([0,816394])
    plt.bar(listA, listB, alpha = 0.6)
    plt.show()


def dict2file(dictionary, filename):
    """
    Writes a file where the first column is the key and the second the values
    """

    directorytosave = '/home/smiravet/crg/transpgrowth/datasets/'

    fo = open(directorytosave+filename+'.txt', 'w')

    od = collections.OrderedDict(sorted(dictionary.items()))
    for k, v in od.iteritems():
        fo.write(str(k)+'\t'+str(v)+'\n')

    fo.close()


def histogram(dataset, numBins = None, location = None):
    """ Plot a histogram for the dataset """

    if not numBins:
        numBins = len(dataset)/20

    fig = plt.figure()
    ax  = fig.add_subplot(111)

    ax.hist(dataset, numBins, color='green', alpha = 0.25)

    if location:
        plt.savefig(location)
    else:
        plt.show()


def load_multifasta(inFile):
    """ Return a dictionary wit the sequences from a multifasta file """
    your_sequences = {}
    handle = open(inFile, 'rU')
    for record in SeqIO.parse(handle, "fasta"):
        your_sequences[record.id]=str(record.seq)
    handle.close()
    return your_sequences


def load_multifasta_info(inFile):
    """ Return a dictionary wit the sequences from a multifasta file """
    your_sequences = {}
    handle = open(inFile, 'rU')
    for record in SeqIO.parse(handle, "fasta"):
        your_sequences[record.id+'//'+record.description]=str(record.seq)
    handle.close()
    return your_sequences


def load_genome(genome):
    # Determine the file type:
    if genome.endswith('gb'):
        tipo = 'genbank'
    else:
        tipo = 'fasta'
    handle = open(genome, 'rU')
    for record in SeqIO.parse(handle, tipo):
        return str(record.seq)
    handle.close()


def load_genome_DB(organism):
    """Uses load_genome function to return the sequence of the organism selected"""

    try:
        genome = load_genome('../smprots_DB/genomes/'+organism+'.fa')
    except:
        genome = load_genome('../smprots_DB/genomes/'+organism+'.gb')

    return genome


def load_annotation(inFile):
    annotation = {}
    with open(inFile) as fi:
        for line in fi:
            line = line.strip().split()
            ide  = line[0]
            if len(line[1:]) == 2:
                st, en = sorted([int(x) for x in line[1:]])
                l      = [st, en]
            else:
                st, en = sorted([int(x) for x in line[1:] if x not in ['+', '-']])
                strand = [str(x) for x in line[1:] if x in ['+', '-']]
                l      = [st, en] + strand
            annotation[ide] = l
    return annotation


def lists2dict(listA, listB):
    """ Given two lists of the same length, merge them in one dictionary """
    return dict(zip(listA, listB))


def remove_column(array, index):
    """ Remove the index column from a numpy array, index can be a list"""

    return np.delete(array, np.s_[index], axis=1)


##### FOR SEQUENCES

def reverse_complement(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join([complement[k] for k in seq][::-1])
