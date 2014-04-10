python deploy.py \
restart \
platform1 \
/home/func_local/tmp \
/home/func_remote/local \
app.tar.gz \
"cd /home/func_remote/local/app && \`pwd\`/cmd arg1 arg2" \
"cmd arg1 arg2"

python deploy.py \
stop \
platform1 \
"cmd arg1 arg2"
