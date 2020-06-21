filename="moves.txt"

for d in */; do
	while read move; do
		mkdir "$d/$move"
	done < moves.txt
done