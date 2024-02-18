import pysam
import pandas as pd
import argparse
import taxopy
import os
import numpy as np
from collections import Counter
import logging
import sys
from collections import defaultdict, OrderedDict
from taxopy.exceptions import TaxidError
import numpy as np
from scipy.stats import binned_statistic
import math

# Create a logger object
logger = logging.getLogger('my_logger')

# Create a formatter object with the desired log format
log_format = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# Create a handler and add the formatter to it
console_handler = logging.StreamHandler()  # Output logs to the console
console_handler.setFormatter(log_format)

# Add the handler to the logger object
logger.addHandler(console_handler)

# Customize logger.info function to include status
def custom_log(level, msg, *args, status=None):
    if status:
        msg = f'({status}) {msg}'  # Concatenate the message and status
    logger.log(level, msg, *args)

# Bind the custom_log function to the logger object for different log levels
logger.info = lambda msg, *args, status=None: custom_log(logging.INFO, msg, *args, status=status)
logger.warning = lambda msg, *args, status=None: custom_log(logging.WARNING, msg, *args, status=status)
logger.error = lambda msg, *args, status=None: custom_log(logging.ERROR, msg, *args, status=status)
logger.debug = lambda msg, *args, status=None: custom_log(logging.DEBUG, msg, *args, status=status)


def compute_entropy(seq):
    # Calculate the Shannon entropy of a sequence
    counter = Counter(seq)
    length = len(seq)
    return -sum(count/length * math.log2(count/length) for count in counter.values())

def compute_coverage(pysam_cov):
    """Computes average coverage of a reference
    Args:
        pysam_cov (np.array): Four dimensional array of coverage for each base
    Returns:
        np.array: 1D int array of coverage at each base
    """
    return np.sum(pysam_cov, axis=0)


def zscore(cov):
    """Compute zscore

    Args:
        cov (np.array): 1D numpy array of coverage (float)
    Returns:
        np.array: zscore(float) of coverage
    """
    mean = np.mean(cov)
    stdev = np.std(cov)
    if mean == stdev == 0:
        return cov
    else:
        return (cov - mean) / stdev

def calc_alignment_start(read):
    if not read.is_reverse:
        return read.query_alignment_start
    return read.infer_read_length() - read.query_alignment_end

def calc_alignment_end(read):
    if not read.is_reverse:
        return read.query_alignment_end
    return read.infer_read_length() - read.query_alignment_start

def flag_conserved_regions(cov_array, window_size=500, zscore_thresh=1.65):
    """Flag ultra-conserved regions by checking coverage with zscore

    Args:
        cov_array (np.array): 1D int array of coverage at each base
        window_size(int): size of sliding window
        zscore_thresh(float): zscore threshold
    Returns:
        list: list of start and end positions of windows flagged as
            conserved [[start, end],[start,end]]

    """
    nb_windows = int(cov_array.size / window_size)
    cov_bin_median = binned_statistic(
        np.arange(cov_array.size), cov_array, statistic="median", bins=nb_windows
    )
    cov_bin_zscore = zscore(cov_bin_median[0])
    is_conserved = cov_bin_zscore > zscore_thresh
    conserved_regions = cov_bin_median[1][:-1].astype(int)[is_conserved]
    cons_range = []
    for i in conserved_regions:
        cons_range.append((i, min(i + window_size, cov_array.size - 1)))

    return cons_range


def is_in_conserved(read, cons_ranges):
    """Check if read is in a conserved region

    Args:
        read (pysam read): Read class from PySam
        cons_ranges (list): list of start and end positions of windows flagged as
            conserved [[start, end],[start,end]]
    """
    for r in cons_ranges:
        if read.reference_start > r[1]:
            continue
        if read.reference_start > r[0] and read.reference_end < r[1]:
            return True
    return False

def get_conserved_regions(input_file, mode, ref):
    """Get regions with higher than expected coverage, with zscore method

    Args:
        ref (pysam reference): one of pysam.alignment.references
    Returns:
        dict: {reference: conserved_regions[(start,end)]}
    """

    al_file = pysam.AlignmentFile(input_file, mode)
    refcov = compute_coverage(al_file.count_coverage(ref))
    window_size = min(al_file.get_reference_length(ref), 500)
    conserved_regions = flag_conserved_regions(refcov, window_size=window_size)
    return {ref: conserved_regions}

def reassign_count_lineage(taxid_counts, read_taxid_dict_reassign, taxo_db):
    """Compute total counts of reads matching to taxons and their descendants

    Args:
        taxid_items (dict_item): (TAXID(int), read_count(int))
    """
    for taxid, read_count in taxid_counts.items():
        try:
            taxon = taxopy.Taxon(taxid, taxo_db)
            lineage = taxon.taxid_lineage
        except Exception:
            read_taxid_dict_reassign[taxid] = [read_count, read_count]
            return
        if taxid not in read_taxid_dict_reassign:
            read_taxid_dict_reassign[taxid] = [read_count, 0]
        else:
            read_taxid_dict_reassign[taxid][0] = read_count
        for t in lineage:
            if t not in read_taxid_dict_reassign:
                read_taxid_dict_reassign[t] = [0, read_count]
            else:
                read_taxid_dict_reassign[t][1] += read_count

    return read_taxid_dict_reassign

def taxids_to_majority_lca(taxids, weights, taxo_db,unclassified_taxid=12908):
    """Run LCA on list of TAXID

    Args:
        taxids (set): frozenset of taxids
    """
    # try:
    #     taxids.remove(0)
    # except KeyError:
    #     pass
    try:
        if len(taxids) == 1:
            ancestor = tuple(taxids)[0].taxid
        elif len(taxids) > 1:
            ancestor = taxopy.find_majority_vote(tuple(taxids), tuple(weights), taxo_db).taxid
        else:
            ancestor = taxopy.Taxon(unclassified_taxid, taxo_db)
    except (TaxidError, AttributeError) as e:
        logger.error(e)
        logger.error(taxids)
        ancestor = taxopy.Taxon(unclassified_taxid, taxo_db)
    
    return ancestor

ranks = OrderedDict(
    [
        ("strain", 0.95),
        ("subspecies", 0.8),
        ("species", 0.7),
        ("subgenus", 0.5),
        ("genus", 0.5),
        ("family", 0.5),
        ("order", 0.5),
        ("class", 0.5),
        ("phylum", 0.5),
        ("superkingdom", 0.5),
    ]
)

def alignment_vote(rank_dicts, contig_length, taxonomy):
    for rank, vote_percent_threshold in ranks.items():
        taxnode_bp_dict = rank_dicts.get(rank)
        if taxnode_bp_dict is None:
            continue
        vote_bp_threshold = vote_percent_threshold * contig_length
        # sort the dict by bp assigned
        taxnode, bp = max(taxnode_bp_dict.items(), key=lambda k: k[1])
        if bp > vote_bp_threshold:
            return taxnode
    # return root if all else fails
    return int(taxonomy.root.id)

#Main method
def main():
    #Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input SAM or BAM file', required=True)
    parser.add_argument('-s2t', '--seqid_taxid_tsv', help='Tab separated text file with each line containing a reference sequence identifier and associated taxonomy ID.')
    parser.add_argument('--nodes', help='Path for nodes.dmp file', required=True)
    parser.add_argument('--names', help='Path for names.dmp file', required=True)
    parser.add_argument('--verbose', action='store_true', help='Detailed print')
    parser.add_argument('--check_conserved', action='store_true', help='Check for conserved regions')
    parser.add_argument('--output_bam', help='Output bam file', required=True)
    parser.add_argument('--output_tsv', help='Output microbiome read tsv', required=True)
    parser.add_argument('--minlength', type=int, default=30, help='Minimum length of alignment to consider')
    parser.add_argument('--log_file', dest='log_file', required=True, help="File to write the log to")
    parser.add_argument('--process', type=int, default=1, help='Number of processes to use')
    args=parser.parse_args()
    
    process = args.process
    minlength = int(args.minlength)
    # Set log level based on command line arguments
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Create a file handler and add the formatter to it
    file_handler = logging.FileHandler(args.log_file)  # Output logs to the specified file
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Check if file exists
    if not os.path.exists(args.input):
        logger.error(f"Unable to find {args.input}")
        sys.exit()

    # Check bam file type
    logger.info('Checking input bam file type', status='run')
    mode = {"sam": "r", "bam": "rb", "cram": "rc"}
    try:
        filetype = args.input.split(".")[-1]
        mode = mode[filetype]
    except:
        logger.error(f"Unable to determine file type for {args.input}")
        sys.exit()

    # Check file is bwa mem or minimap2
    is_minimap2 = False
    is_bwa = False
    read_count = 0
    present_refs = set()
    with pysam.AlignmentFile(args.input, mode, threads=process) as input_file:

        for ref_stat in input_file.get_index_statistics():
            refname = ref_stat[0]
            mapped_reads = ref_stat[1]
            if mapped_reads > 0:
                present_refs.add(refname)

        for read in input_file:
            read_count += 1
            # 检查是否存在目标标签
            if read.has_tag("NM") and read.has_tag("AS"):
                is_bwa = True
                break
            if read.has_tag("de") and read.has_tag("ms"):
                is_minimap2 = True
                break
            # if didnt find type in first 100 reads, exit
            if read_count >= 100:
                logger.error(f"Unable to support for {args.input}")
                sys.exit()

    if args.check_conserved:
        logger.info('Checking for conserved regions', status='run')
        if process == 1:
            cons_dict = dict()
            for ref in present_refs:
                try:
                    cons_dict.update(get_conserved_regions(args.input, mode, ref))
                except Exception as e:
                    logger.error(f"An error occurred while checking for conserved regions: {e}")
                    sys.exit()

    # Loading taxonomy database
    logger.info('Loading taxonomy database', status='run')
    try:
        taxdb = taxopy.TaxDb(nodes_dmp=args.nodes,names_dmp=args.names)
        logger.info('Successfully loading taxonomy database', status='complete')
    except (ValueError, KeyError) as e:
        logger.error(f"An error occurred while loading taxonomy database: {e}")
        sys.exit()

    # Loading refernce seq taxid map
    logger.info('Loading reference sequences taxid map tsv', status='run')
    seqid_taxid_df = pd.read_csv(args.seqid_taxid_tsv, delimiter="\t")
    # Get sequence id to taxid map
    ## Init acc2tax dict
    acc2tax = dict()
    ## Iterate over each accession
    for acc in present_refs:
        try:
            taxid = seqid_taxid_df.loc[seqid_taxid_df['accession.version'] == acc, 'taxid'].values[0].astype(int)
            if taxid != 0:
                acc2tax[acc] = taxopy.Taxon(taxid, taxdb)
        # Catch errors
        except (TypeError, TaxidError) as e:
            logger.error(f"An error occurred while parsing {args.seqid_taxid_tsv}: {e}")
            sys.exit()
    logger.info(f"Loaded {len(acc2tax)} reference sequences", status='complete')

    
    # Read the alignment file    
    total_reads = int(pysam.view("-c", f"-@ {process}",args.input).rstrip())
    read_count = 0
    use_count = 0
    read_info = defaultdict(list)
    read_seq = dict()
    with pysam.AlignmentFile(args.input, mode, threads=process) as input_file:
        for read in input_file:
            read_count += 1
            
            # Output progress every 5% of reads processed
            if read_count % (total_reads // 20) == 0:
                progress = read_count / total_reads * 100
                logger.info(f"Processed {progress:.2f}% of file reads", status='run')
            
            if is_bwa:
                if read.has_tag("NM") and not read.is_unmapped:
                    if args.check_conserved:
                        try:
                            if not read.is_secondary:
                                read_seq[read.query_name] = read.query_sequence
                            is_conserved = is_in_conserved(
                                read, cons_dict[read.reference_name]
                            )
                            identity = ((read.query_alignment_length - read.get_tag("NM")) / read.infer_read_length())
                            if not is_conserved and read.query_alignment_length >= minlength and identity > 0.51:
                                read_info[read.query_name].append((read.reference_name, # reference name
                                                                    read.get_tag("NM"), # mistach
                                                                    read.query_alignment_length, # query alignment length
                                                                    read.infer_read_length(), # infer read length
                                                                    read.is_secondary,  # secondary alignment
                                                                    read.get_tag("AS"), # alignment score
                                                                    calc_alignment_start(read),  # AlignmentStart
                                                                    calc_alignment_end(read),  # AlignmentEnd
                                                                    ))
                                use_count += 1

                        except Exception as e:
                            logger.error(f"An error occurred while parsing {args.input}: {e}")
                            sys.exit()

                    elif read.query_alignment_length >= minlength:
                        try:
                            read_info[read.query_name].append((read.reference_name, # reference name
                                    read.get_tag("NM"), # mistach
                                    read.query_alignment_length, # query alignment length
                                    read.infer_read_length(), # infer read length
                                    read.is_secondary,  # secondary alignment
                                    read.get_tag("AS"), # alignment score
                                    calc_alignment_start(read),  # AlignmentStart
                                    calc_alignment_end(read),  # AlignmentEnd
                                    ))
                            use_count += 1
                            if not read.is_secondary:
                                read_seq[read.query_name] = read.query_sequence
                        except Exception as e:
                            logger.error(f"An error occurred while parsing {args.input}: {e}")
                            sys.exit()

            if is_minimap2:
                if read.has_tag("de") and not read.is_unmapped:
                    
                    # Check if read is in conserved region
                    if args.check_conserved:
                        try:
                            if not read.is_secondary:
                                read_seq[read.query_name] = read.query_sequence
                            is_conserved = is_in_conserved(
                                read, cons_dict[read.reference_name]
                            )
                            identity = (1- read.get_tag("de"))
                            if not is_conserved and read.query_alignment_length >= minlength and identity > 0.51:
                                read_info[read.query_name].append((read.reference_name, # reference name
                                                                    read.get_tag("de"), # divergence
                                                                    read.query_alignment_length, # query alignment length
                                                                    read.infer_read_length(), # infer read length
                                                                    read.is_secondary,  # secondary alignment
                                                                    read.get_tag("ms"), # alignment score
                                                                    calc_alignment_start(read),  # AlignmentStart
                                                                    calc_alignment_end(read),  # AlignmentEnd
                                                                    ))
                                use_count += 1
                        except Exception as e:
                            logger.error(f"An error occurred while parsing {args.input}: {e}")
                            sys.exit()
                    elif read.query_alignment_length >= minlength:
                        try:
                            read_info[read.query_name].append((read.reference_name, # reference name
                                    read.get_tag("de"), # divergence
                                    read.query_alignment_length, # query alignment length
                                    read.infer_read_length(), # infer read length
                                    read.is_secondary,  # secondary alignment
                                    read.get_tag("ms"), # alignment score
                                    calc_alignment_start(read),  # AlignmentStart
                                    calc_alignment_end(read),  # AlignmentEnd
                                    ))
                            use_count += 1
                            if not read.is_secondary:
                                read_seq[read.query_name] = read.query_sequence
                        except Exception as e:
                            logger.error(f"An error occurred while parsing {args.input}: {e}")
                            sys.exit()

    logger.info(f"Processed {read_count} reads", status='complete')
    logger.info(f"Used {use_count} reads", status='complete')
    logger.info(f"Found {len(read_info)} query reads", status='complete')
    
    # Aggregate the read info
    logger.info('Aggregating read info', status='run')
    read_ref_aggr_dict = defaultdict(lambda: {'taxons': [], 'weights': []})
    read_max_align_values = defaultdict(lambda: defaultdict(float))
    for query_name, info in read_info.items():
        if is_bwa:
            # Get the query alignment length
            query_alignment_length = info[0][2]
            # Get the query length
            query_length = info[0][3]
            # Get the alignment score
            alignment_score = info[0][5]
            # Get the mismatch
            mismatch = info[0][1]
            # Get the reference name
            reference_name = info[0][0]

            identity = 1 - (mismatch / query_alignment_length)
            align_value = ((query_alignment_length - mismatch) / query_length)
            weight =  align_value * align_value * alignment_score
        
        if is_minimap2:
            # Get the query alignment length
            query_alignment_length = info[0][2]
            # Get the query length
            query_length = info[0][3]
            # Get the alignment score
            alignment_score = info[0][6]
            # Get the divergence
            divergence = info[0][1]
            # Get the reference name
            reference_name = info[0][0]

            identity = 1 - divergence
            align_value = query_alignment_length
            weight = identity * align_value * alignment_score

        # Get the reference taxid
        try:
            reference_taxon = acc2tax[reference_name]
              
        except KeyError:
            reference_taxon = taxopy.Taxon(12908, taxdb)
            logger.error(f"Unable to find taxid for {reference_name}")
        
        # Add taxon and weight to read_ref_dict
        read_ref_aggr_dict[query_name]['taxons'].append(reference_taxon)
        read_ref_aggr_dict[query_name]['weights'].append(weight)

        if read_max_align_values[query_name][reference_taxon.taxid]:
            orgin_value = read_max_align_values[query_name][reference_taxon.taxid]
            if align_value > orgin_value:
                read_max_align_values[query_name][reference_taxon.taxid] = align_value
        else:
            read_max_align_values[query_name][reference_taxon.taxid] = align_value
    # computa lca for each read
    logger.info('Computing LCA for each read', status='run')
    read_taxid_dict = dict()

    for query_name, data_dict in read_ref_aggr_dict.items():
        taxids = data_dict['taxons']
        weights = data_dict['weights']
        lca_taxid = taxids_to_majority_lca(taxids, weights, taxdb)
        lca_taxon = taxopy.Taxon(lca_taxid, taxdb)
        try:
            if lca_taxid in read_max_align_values[query_name]:
                align_value = read_max_align_values[query_name][lca_taxid]
                lca_rank = lca_taxon.rank
                # Check if subspeces
                if lca_rank == "no rank" and lca_taxon.rank_name_dictionary["species"]:
                    lca_rank = "subspecies"
                elif not lca_taxon.rank_name_dictionary["species"] and lca_taxon.rank_name_dictionary["genus"]:
                    lca_rank = "subgenus"
                elif lca_rank == "forma specialis" or lca_rank == "serotype":
                    lca_rank = "species"
                for threshold_rank, vote_percent_threshold in ranks.items():
                    if threshold_rank != lca_rank:
                        continue

                    if align_value > vote_percent_threshold:
                        final_taxid = lca_taxid
                    else:
                        lca_taxid = taxdb.taxid2parent[lca_taxid]
                        lca_rank = taxdb.taxid2rank[lca_taxid]
                        final_taxid = lca_taxid
            
            elif lca_taxon.rank_name_dictionary["species"] in read_max_align_values[query_name]:
                align_value = read_max_align_values[query_name][lca_taxon.rank_name_dictionary["species"]]
                lca_rank = lca_taxon.rank
                threshold_rank = ranks[lca_rank]
                for threshold_rank, vote_percent_threshold in ranks.items():
                    if threshold_rank != lca_rank:
                        continue

                    if align_value > vote_percent_threshold:
                        final_taxid = lca_taxid
                    else:
                        lca_taxid = taxdb.taxid2parent[lca_taxid]
                        lca_rank = taxdb.taxid2rank[lca_taxid]
                        final_taxid = lca_taxid
            elif lca_taxon.rank_name_dictionary["strain"] in read_max_align_values[query_name]:
                align_value = read_max_align_values[query_name][lca_taxon.rank_name_dictionary["strain"]]
                lca_rank = lca_taxon.rank
                threshold_rank = ranks[lca_rank]
                for threshold_rank, vote_percent_threshold in ranks.items():
                    if threshold_rank != lca_rank:
                        continue

                    if align_value > vote_percent_threshold:
                        final_taxid = lca_taxid
                    else:
                        lca_taxid = taxdb.taxid2parent[lca_taxid]
                        lca_rank = taxdb.taxid2rank[lca_taxid]
                        final_taxid = lca_taxid
            else:
                logger.error(f"Unable to find taxid for {lca_taxid}")
            # Give the final taxid
            read_taxid_dict[query_name] = final_taxid
        except Exception as e:
            logger.error(f"An error occurred while computing LCA: {e}")
            print(lca_taxon.name)
            print(lca_taxon.rank)
            sys.exit()

    # Del entropy < 1.2
    to_delete = []    
    for query_name, final_taxid in read_taxid_dict.items():
        sequence = read_seq[query_name]
        sequence_entropy = compute_entropy(sequence)
        if sequence_entropy < 1.2:
            to_delete.append(query_name)
    
    for query_name in to_delete:
        del read_taxid_dict[query_name]


    taxid_counts = dict(Counter(read_taxid_dict.values()))
    taxid_info_dict = dict()

    read_taxid_dict_reassign = dict() 
    read_taxid_dict_reassign = reassign_count_lineage(taxid_counts, read_taxid_dict_reassign, taxdb)
    for taxid, count in taxid_counts.items():
        try:
            taxon = taxopy.Taxon(int(taxid), taxdb)
            taxid_info_dict[taxid] = {'taxid': taxon.taxid,
                                        'name': taxon.name,
                                        "rank": taxon.rank,
                                        'count_taxon': read_taxid_dict_reassign[taxid][0],
                                        'count_descendant': read_taxid_dict_reassign[taxid][1],
                                        'lineage': taxon}
        except TaxidError:
            logger.error(f"Unable to find taxid for {taxid}")
            sys.exit()

    if args.output_bam:
        # write output bam
        logger.info('Writing output bam with lca species tag', status='run')
        with pysam.AlignmentFile(args.input, mode, threads=process) as input_file:
            with pysam.AlignmentFile(args.output_bam, "wb", template=input_file) as output_file:
                for read in input_file:
                    if read.is_unmapped or read.is_secondary:
                        continue

                    if read.query_name in read_taxid_dict:
                        read_taxid = read_taxid_dict[read.query_name]

                        read.set_tag("XT", taxid_info_dict[read_taxid]['taxid'], "i")
                        read.set_tag(
                            "XN",
                            taxid_info_dict[read_taxid]["name"],
                            "Z",
                        )
                        read.set_tag(
                            "XR",
                            taxid_info_dict[read_taxid]["rank"],
                            "Z",
                        )
                        output_file.write(read)

        logger.info('Successfully writing output bam', status='complete')

    if args.output_tsv:

        taxid_info_df = pd.DataFrame(taxid_info_dict).transpose()
        taxid_info_df.sort_values("count_descendant", inplace=True, ascending=False)
        # write output tsv
        logger.info('Writing read output tsv', status='run')
        taxid_info_df.to_csv(args.output_tsv, sep="\t")
        logger.info('Successfully writing output tsv', status='complete')

if __name__ == "__main__":
    main()