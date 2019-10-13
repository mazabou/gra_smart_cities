FILE=data/processed/darknet/obj.names
rm $FILE && touch $FILE
echo "classes=$1" >> $FILE
echo "train  = data/train.txt" >> $FILE
echo "valid  = data/test.txt" >> $FILE
echo "names = data/obj.names.$1" >> $FILE
echo "backup = backup/" >>$FILE

cd data/processed/darknet/obj
ln -fs ../obj.$1/* ./
cd -