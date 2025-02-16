certoraOutput=$(certoraRun "$@")

echo "$certoraOutput"

if [[ ${certoraOutput} != *"ERROR"* ]];then

  certoraURL=$(echo $certoraOutput | sed -n 's/.*\(https:\/\/prover.certora.com\/output\/\)/\1/p')

  git add -A

  git commit -m "Results for run: $certoraURL with arguments $@"
  echo $certoraURL
fi