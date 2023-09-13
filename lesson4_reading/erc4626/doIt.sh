for file in ./src/certora/conf/*.conf

echo "Using git commit " >> results.out
git rev-parse HEAD >> results.out
git git status --short >> results.out
do
  echo  "Results for $file can be found at:" >> results.out
  certoraRun "$file" | sed -n 's/.*\(https:\/\/prover.certora.com\/output\/\)/\1/p' >> results.out
done