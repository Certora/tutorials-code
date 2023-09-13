for file in ./src/certora/conf/*.conf
do
  echo -e "Results for $file can be found at:" >> results.out
  certoraRun "$file" | sed -n 's/.*\(https:\/\/prover.certora.com\/output\/\)/\1/p' >> results.out
done