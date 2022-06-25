test_cmd="python -m pytest -v "

declare -a ignore_list=(
  "test_emaily.py"
)


for ignore in "${ignore_list[@]}"
do
  test_cmd+="--ignore-glob=**/$ignore "
done

eval "$test_cmd -W ignore::ImportWarning -x testy"
