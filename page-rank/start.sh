echo "[ Computing pagerank ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file pagerank_mapper.py \
        -mapper "python pagerank_mapper.py" \
        -file pagerank_reducer.py  \
        -reducer "python pagerank_reducer.py" \
        -input s3://search-engine-bd/page-rank \
        -output s3://search-engine-bd/output


echo "[ Generating Partials ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -Dmapred.reduce.tasks=1 \
        -input s3://search-engine-bd/output/ \
        -output s3://search-engine-bd/partials \
        -mapper cat \
        -reducer cat

echo "[ Generating Partials1 ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file rank_map.py \
        -mapper "python rank_map.py" \
        -input s3://search-engine-bd/partials/ \
        -output s3://search-engine-bd/partials1

echo "[ Generating Results ]"
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -Dmapred.reduce.tasks=1 \
        -input s3://search-engine-bd/partials1 \
        -output s3://search-engine-bd/result \
        -mapper cat \
        -reducer cat