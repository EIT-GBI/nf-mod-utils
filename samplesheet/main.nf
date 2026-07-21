// Samplesheet builders, shared by short-read and long-read pipelines
// should run contianer-less using the host python3

// Short read: paired-end FASTQ (R1/R2)
process PREPARE_SAMPLESHEET_SHORT {
    tag "${input_dir}"

    publishDir "${params.outdir}/samplesheet", mode: 'copy'

    input:
    path input_dir
    val reference

    output:
    path "samplesheet.csv", emit: csv

    script:
    """
    python3 ${moduleDir}/generate_samplesheet_short.py \
        --input_dir ${input_dir} \
        --reference ${reference} \
        --output samplesheet.csv
    """

    stub:
    """
    touch samplesheet.csv
    """
}

process PREPARE_SAMPLESHEET_LONG{
    tag "${input_dir}"

    publishDir "${params.outdir}/samplesheet", mode: 'copy'

    input:
    path input_dir
    val reference

    output:
    path "samplesheet.csv", emit: csv

    script:
    """
    python3 ${moduleDir}/generate_samplesheet_long.py \
        --input_dir ${input_dir} \
        --reference ${reference} \
        --output samplesheet.csv
    """

    stub:
    """
    touch samplesheet.csv
    """
}