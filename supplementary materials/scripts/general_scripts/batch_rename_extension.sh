for i in $(ls *.fasta); do mv "$i" "$(basename "$i" .fasta).dssp"; done
