#!/usr/bin/env bash

echo loading config
source ./package.conf

script_path=$PWD;
dd="${script_path}/${dependencies_dir}"

for dep in ${python}
do
    echo "installing ${dep} python dependency"
    pip install --upgrade --force-reinstall ${dep}
done

# clear vendor directory
# rm -rf ./${dependencies_dir} && mkdir -p ./${dependencies_dir}

echo "installing repo dependencies in ${dd}"
mkdir $dd || true;
for dep in ${git}
do
    cd $dd
    git_repo_name=$(basename -- "$dep")
    repo_dir="${dd}/${git_repo_name%.*}"

    if [ -d "$repo_dir" ]; then
        echo "updating \"${git_repo_name%.*}\""
        cd $repo_dir && git pull;
    else
        echo "installing \"${git_repo_name%.*}\""
        echo "cloning ${dep} dependency in ${repo_dir}"
        git clone --depth=1 ${dep} --branch ${odoo_version}
    fi
    modules_root="${modules_root},${repo_dir}"
done


echo "

installation completed, add following dirs to your modules dir configuration:
----
${modules_root}
----

"
