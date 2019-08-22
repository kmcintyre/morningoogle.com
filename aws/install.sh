#!/bin/bash
. ./env.sh
cmd=create
#array=(role codepipeline)
array=(codebuild)
for a in "${array[@]}"; do
  for file in $(ls cloudformation | grep .yml$ | grep ^$a); do
    sn=${file##$a\_}
    sn=${sn::-4}
    vars=$(env | grep ${a^^}_)
    parameters=
    for var in $vars; do
      key=$(echo $var | cut -d'=' -f 1 | cut -d'_' -f 2)
      value=$(echo $var | cut -d'=' -f 2)
      parameters="$parameters ParameterKey=$key,ParameterValue=$value"
    done;
    aws cloudformation $cmd-stack --stack-name $a-$sn --template-body file://cloudformation/$file \
      --capabilities CAPABILITY_IAM \
      --parameters $parameters
    aws cloudformation wait stack-$cmd-complete --stack-name $a-$sn
  done;
done;
