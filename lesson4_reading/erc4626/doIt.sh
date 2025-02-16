echo -e  "\n\n\n########### New execution ##########\n\n\n" >> results.out
echo -e  "\n\n\n########### Started on $(date)  ##########\n\n\n" >> results.out
git rev-parse HEAD >> results.out
git status --short >> results.out
for file in ./src/certora/conf-openzeppelin/*.conf
do
  echo -e  "\n\n\n" >> results.out
  echo -e  "Results for $file can be found at:" >> results.out
  certoraRun "$file" >> results.out
done