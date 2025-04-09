submit_job --gpu 1 --tasks_per_node 1 --nodes 1 -n experiment --image /home/zhidingy/workspace/dockers/openwebui.sqsh \
        --logroot workdir_lasting_demo_short \
        --email_mode never \
        --partition adlr_services \
        --duration 0 \
        --dependent_clones 0 \
        --host batch-block1-0030 \
        -c "cd /home/zhidingy/workspace/libs/open-webui-video; bash start.sh"


