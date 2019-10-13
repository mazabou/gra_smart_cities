FILE=data/processed/darknet/obj.data
if [ -f "$FILE" ]; then
  rm $FILE && touch $FILE
fi
echo "classes=$1" >> $FILE
echo "train  = data/train.txt" >> $FILE
echo "valid  = data/test.txt" >> $FILE
echo "names = data/obj.names.$1" >> $FILE
echo "backup = backup/" >>$FILE

cd data/processed/darknet/obj
ln -fs ../obj.$1/* ./
cd -