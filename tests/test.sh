rm exercise2.sqlite
python emanual.py --ea name=name1,purpose=100
python emanual.py --ea name=name2,purpose=200
python emanual.py --ea name=name3,purpose=300
python emanual.py --ga name1,name2 gname1
python emanual.py --ga name3,name2 gname2

echo "\n==== name ====\n"
python emanual.py --schedule -n name1 2011030810
python emanual.py --schedule -g gname1 20110308
python emanual.py --schedule -g gname1 20110305
python emanual.py --schedule -n name2 today
#echo "\n\n=========================="
#echo "========== Error Part================"

#python emanual.py --schedule -n errorname 2011030810


python emanual.py --record -n name1 10
python emanual.py --record -n name2 20
python emanual.py --record -n name3 30

python emanual.py --list group
