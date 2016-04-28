cat temp.json | head -2 | xargs -d\\n -L1 -I% sh -c 'echo '\''%'\'' |sed "s/\\\\\\\\/\\\\\\\\\\\\/g"| python -m json.tool'
