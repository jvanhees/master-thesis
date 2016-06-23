#!/bin/bash
#$ -l h_rt=0:15:00
#$ -N VideoThumbnails
#$ -cwd

echo "Start - `date`"
python model.py
echo "Finish - `date`"