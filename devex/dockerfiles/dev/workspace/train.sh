cd ~/workspace 
git clone https://github.com/daniel-vainsencher/DeepSpeedExamples.git -b pf_coach
cd DeepSpeedExamples/applications/DeepSpeed-Chat/ && pip install -r requirements.txt && cd ~/workspace
git config --global credential.helper store

export HF_TOKEN=<YOUR TOKEN>
huggingface-cli login --token ${HF_TOKEN} --add-to-git-credential
cd DeepSpeedExamples/applications/DeepSpeed-Chat/training/step1_supervised_finetuning/ && \
    /usr/bin/python -u -m deepspeed.launcher.launch --world_info=eyJsb2NhbGhvc3QiOiBbMF19 \
    --master_addr=127.0.0.1 --master_port=29500 --enable_each_rank_log=None \
    main.py --model_name_or_path facebook/opt-1.3b --target_model_name danielv835/PF_Coach_sft_1.3b \
    --data_split 2,4,4 --per_device_train_batch_size 8 --per_device_eval_batch_size 8 --max_seq_len 512 \
    --learning_rate 9.65e-6 --weight_decay 0. --num_train_epochs 3 --lr_scheduler_type cosine \
    --num_warmup_steps 0 --gradient_accumulation_steps 1 --gradient_checkpoint \
    --zero_stage 2 --deepspeed \
    --output_dir /DeepSpeedExamples/applications/DeepSpeed-Chat/output/actor-models/1.3b \
    --data_path danielv835/personal_finance_v0.2 Dahoas/rm-static Dahoas/full-hh-rlhf \
    Dahoas/synthetic-instruct-gptj-pairwise yitingxie/rlhf-reward-datasets stanfordnlp/SHP,