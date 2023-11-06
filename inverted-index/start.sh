bucket_name="search-engine-bd"

echo echo "[ Computing Inverted Index ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file mapper.py \
        -mapper "python mapper.py" \
        -file reducer.py  \
        -reducer "python reducer.py" \
        -input s3://$bucket_name/corpus/txt \
        -output s3://$bucket_name/output


echo "[ Generating Results ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -Dmapred.reduce.tasks=1 \
        -input s3://$bucket_name/output \
        -output s3://$bucket_name/result \
        -mapper cat \
        -reducer cat