#!/bin/bash
s3=$(aws s3 ls | grep codepipeline | cut -d' ' -f3)
if [[ ! -z "$s3" ]]; then
  echo s3=$s3
  aws s3 rm s3://$s3/ --recursive
fi
array=(codepipeline role)
for a in "${array[@]}"; do
  for file in $(ls cloudformation | grep ^$a); do
    sn=${file##$a\_}
    sn=${sn::-4}
    echo file=$file
    aws cloudformation delete-stack --stack-name $a-$sn
    aws cloudformation wait stack-delete-complete --stack-name $a-$sn
  done;
done;
