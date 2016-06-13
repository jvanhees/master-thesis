#!/bin/bash
#$ -l h_rt=0:15:00
#$ -N VideoThumbnails
#$ -cwd

echo "Start - `date`"
python app.py 
echo "Finish - `date`"