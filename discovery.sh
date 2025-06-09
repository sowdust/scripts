# script che esegue i gobuster su una lista di targets
# salva in due cartelle separate i risultati, come nofile il target
# una cartella con solo i path relativi, l'altra quelli assoluti

sanitize_filename() { echo "$1" | sed 's/[^A-Za-z0-9._-]/_/g'; }
while IFS="" read -r p || [ -n "$p" ]
do
  safe_name=$(sanitize_filename "$p")
  out_file="/path/to/${safe_name}.txt"
  full_file="/path/to/full/${safe_name}.txt"
  printf "[*] Scanning %s\n" "$p"
  cmd=$(printf 'gobuster dir -k -w /path/to/wordlist.txt --exclude-length 0 -u %s -o %s\n' "$p" "$out_file")
  $cmd
  sed "s|^|$p|" "$out_file" > "$full_file"
done < /path/to/targets.txt