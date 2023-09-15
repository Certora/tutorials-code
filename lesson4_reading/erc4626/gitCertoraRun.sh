certoraURL=$(certoraRun "$@" | sed -n 's/.*\(https:\/\/prover.certora.com\/output\/\)/\1/p')

git add -A

git commit -m "Results for run: $certoraURL"
echo $certoraURL