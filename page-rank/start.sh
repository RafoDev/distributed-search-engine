bucket_name="search-engine-bd"

echo "[ Computing pagerank ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file pagerank_mapper.py \
        -mapper "python pagerank_mapper.py" \
        -file pagerank_reducer.py  \
        -reducer "python pagerank_reducer.py" \
        -input s3://$bucket_name/page-rank \
        -output s3://$bucket_name/output


echo "[ Generating Partials ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -Dmapred.reduce.tasks=1 \
        -input s3://$bucket_name/output/ \
        -output s3://$bucket_name/partials \
        -mapper cat \
        -reducer cat

echo "[ Generating Partials1 ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file rank_map.py \
        -mapper "python rank_map.py" \
        -input s3://$bucket_name/partials/ \
        -output s3://$bucket_name/partials1

echo "[ Generating Results ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -Dmapred.reduce.tasks=1 \
        -input s3://$bucket_name/partials1 \
        -output s3://$bucket_name/result \
        -mapper cat \
        -reducer cat