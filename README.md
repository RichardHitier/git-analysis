# Git repo analysis for various usages


### generate data

    cd $repo_dir

    git log --pretty="format:%as" --author="Richard Hitier" >  ../git-analysis/data/ltt.txt

    git log --pretty="format:%at" --author="Richard Hitier" > ../git-analysis/data/timestamps.txt
