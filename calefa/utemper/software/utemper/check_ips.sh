fping -g 192.168.1.0 192.168.1.255 >/dev/null 2>/dev/null
arp -an >/dev/null 2>/dev/null
echo "-------------------------------------------------"
cat /proc/net/arp |\
    # remove space from column headers
    sed 's/\([^ ]\)[ ]\([^ ]\)/\1_\2/g' |\
    # find HW_address column number and/or print that column
    awk '{
        if ( !column ) {
            for (i = 1; i <= NF; i++ ) {
                if ( $i ~ /HW_address/ ) { column=i }
            };
            print $column
         }
         else {
            print $column
         }
    }'

