# script to run simulation with 1% contamination on a set of multiple contaminants

# usage: bash prepare_simulations.sh <REFERENCE.fasta> <CONTAMINANT1.fasta CONTAMINANT2.fasta ...  CONTAMINANTN.fasta>
# REFERENCE.fasta and CONTAMINANT1.fasta CONTAMINANT2.fasta ...  CONTAMINANTN.fasta files must be bwa indexed

target=$1
contaminants="${@:2}"
#seed=145367
nreps=10

# 250000 reads, 1% contamination
ref_count=247500
cont_count=2500

# generate base reads
art_illumina -c $ref_count -l 200 -m 250 -s 10 -ss MSv3 -i $target -na -o `basename $target` --id ___`basename $target`___ -qL 20 #--rndSeed $seed
# outptus are `basename $target`1.fq and `basename $target`2.fq

echo -e "Target\tContaminant\tTP\tTN\tFP\tFN" > output_decont_simulation.log

for contaminant in $contaminants
do
    for i in {1..10}
    do 
        # generate contaminant reads
        art_illumina -c $cont_count -l 200 -m 250 -s 10 -ss MSv3 -i $contaminant -na -o `basename $contaminant` --id ___`basename $contaminant`___ -qL 20 #--rndSeed $seed
        cat `basename $target`1.fq `basename $contaminant`1.fq > temp_concat1.fq
        cat `basename $target`2.fq `basename $contaminant`2.fq > temp_concat2.fq 

        wgalp decontaminate \
            --fastq-fwd temp_concat1.fq \
            --fastq-rev temp_concat2.fq \
            --references $target \
            --contaminants $contaminant \
            --output `basename $target`_VS_`basename $contaminant`

        out_fwd=`basename $target`_VS_`basename $contaminant`/decontaminated_fwd.fastq
        out_rev=`basename $target`_VS_`basename $contaminant`/decontaminated_rev.fastq
        discarded_fwd=`basename $target`_VS_`basename $contaminant`/discarded_reads_fwd.fastq
        discarded_rev=`basename $target`_VS_`basename $contaminant`/discarded_reads_rev.fastq

        target_ID=___`basename $target`___
        contaminant_ID=___`basename $contaminant`___

        TP=$((`grep $target_ID $out_fwd | wc -l`+`grep $target_ID $out_rev | wc -l`))
        TN=$((`grep $contaminant_ID $discarded_fwd | wc -l`+`grep $contaminant_ID $discarded_rev | wc -l`))
        FP=$((`grep $contaminant_ID $out_fwd | wc -l`+`grep $contaminant_ID $out_rev | wc -l`))
        FN=$((`grep $target_ID $discarded_fwd | wc -l`+`grep $target_ID $discarded_rev | wc -l`))
        # ---
        #PRECISION=$(($TP/($TP+$FP)))
        #RECALL=$(($TP/($TP+$FN)))
        #F1=$(((2*$PRECISION*$RECALL)/($PRECISION+$RECALL)))
        
        echo -e "`basename $target`\t`basename $contaminant`\t$TP\t$TN\t$FP\t$FN" >> output_decont_simulation.log 

        # cleanup
        rm temp_concat1.fq
        rm temp_concat2.fq
        rm `basename $contaminant`1.fq
        rm `basename $contaminant`2.fq
        rm -rf `basename $target`_VS_`basename $contaminant`
    done
done
