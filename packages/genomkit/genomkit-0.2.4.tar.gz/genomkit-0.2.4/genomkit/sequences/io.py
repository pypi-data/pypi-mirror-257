###########################################################################
# IO functions
###########################################################################
def load_FASTA(file):
    if isinstance(file, str):  # If file is a filename
        with open(file, 'r') as f:
            return load_FASTA_from_file(f)
    else:  # If file is a file object
        return load_FASTA_from_file(file)


def load_FASTA_from_file(file):
    from genomkit import GSequence, GSequences
    res = GSequences()
    current_sequence_id = None
    current_sequence = ""
    for line in file:
        line = line.strip()
        if line.startswith("#"):
            continue
        elif line.startswith(">"):
            # If there was a previously stored sequence, store it
            if current_sequence_id is not None:
                infos = current_sequence_id.split()
                name = infos[0]
                data = infos[1:]
                res.add(GSequence(sequence=current_sequence,
                                  name=name, data=data))
            # Extract the sequence ID
            current_sequence_id = line[1:]
            # Start a new sequence
            current_sequence = ""
        else:  # Sequence line
            # Append the sequence line to the current sequence
            current_sequence += line
    # Store the last sequence
    if current_sequence_id is not None:
        infos = current_sequence_id.split()
        name = infos[0]
        data = infos[1:]
        res.add(GSequence(sequence=current_sequence,
                          name=name, data=data))
    return res


def load_FASTQ(file):
    if isinstance(file, str):  # If file is a filename
        with open(file, 'r') as f:
            return load_FASTQ_from_file(f)
    else:  # If file is a file object
        return load_FASTQ_from_file(file)


def load_FASTQ_from_file(file):
    from genomkit import GSequence, GSequences
    res = GSequences()
    current_sequence_id = None
    current_sequence = ""
    current_quality = ""
    for line in file:
        line = line.strip()
        if line.startswith("#"):
            continue
        elif line.startswith("@"):  # FASTQ header line
            # If there was a previously stored sequence, store it
            if current_sequence_id is not None:
                if len(current_sequence) != len(current_quality):
                    raise ValueError("Invalid FASTQ file: Sequence and "
                                     "quality lines do not match.")
                elif len(current_quality) == len(current_sequence):
                    infos = current_sequence_id.split()
                    name = infos[0]
                    data = infos[1:]
                    res.add(GSequence(sequence=current_sequence,
                                      quality=current_quality,
                                      name=name, data=data))
            # Extract the sequence ID
            current_sequence_id = line[1:]
            # Start new sequence and quality strings
            current_sequence = ""
            current_quality = ""
        elif current_sequence_id and not current_sequence:
            current_sequence = line
        elif line.startswith("+"):  # FASTQ quality header line
            continue
        elif current_sequence_id and current_sequence and \
                not current_quality:
            current_quality = line
    # Store the last sequence
    if current_sequence_id is not None:
        if len(current_sequence) != len(current_quality):
            raise ValueError("Invalid FASTQ file: Sequence and quality "
                             "lines do not match.")
        elif len(current_quality) == len(current_sequence):
            infos = current_sequence_id.split()
            name = infos[0]
            data = infos[1:]
            res.add(GSequence(sequence=current_sequence,
                              quality=current_quality,
                              name=name, data=data))
    return res
