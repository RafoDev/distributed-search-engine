bucket_name="search-engine-bd"

chmod +x mapper.py reducer.py

echo echo "[ Computing Inverted Index ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file mapper.py \
        -mapper "python mapper.py" \
        -file reducer.py  \
        -reducer "python reducer.py" \
        -input s3://$bucket_name/corpus/txt/ \
        -output s3://$bucket_name/inverted-index/output


echo "[ Generating Results ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -Dmapred.reduce.tasks=1 \
        -input s3://$bucket_name/inverted-index/output/ \
        -output s3://$bucket_name/inverted-index/result \
        -mapper cat \
        -reducer cat