if test -f darknet/build/darknet/x64/darknet53.conv.74; then
	wget https://pjreddie.com/media/files/darknet53.conv.74 -o darknet/build/darknet/x64/darknet53.conv.74
fi

./darknet detector train data/obj.data yolo-obj.cfg darknet/build/darknet/x64/darknet53.conv.74 -map -dont_show 2>&1 | tee log/yolo-obj.log