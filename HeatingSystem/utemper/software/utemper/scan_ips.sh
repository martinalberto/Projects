fping -g ${1}.0 ${1}.254 >/dev/null 2>/dev/null
arp -an >/dev/null 2>/dev/null
cat /proc/net/arp |\
    # remove space from column headers
    sed 's/\([^ ]\)[ ]\([^ ]\)/\1_\2/g' |\
    # find HW_address column number and/or print that column
    awk '{
        if ( !column ) {
            for (i = 1; i <= NF; i++ ) {
                if ( $i ~ /HW_address/ ) { column=i }
            };
         }
         else {
            print $column
         }
    }' |\
	sort |\
	uniq -u > ${2}


