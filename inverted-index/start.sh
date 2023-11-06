
echo echo "[ Computing Inverted Index ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file mapper.py \
        -mapper "python mapper.py" \
        -file reducer.py  \
        -reducer "python reducer.py" \
        -input s3://search-engine-bd/corpus/txt \
        -output s3://search-engine-bd/output


echo "[ Generating Results ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -Dmapred.reduce.tasks=1 \
        -input s3://search-engine-bd/output \
        -output s3://search-engine-bd/result \
        -mapper cat \
        -reducer cat