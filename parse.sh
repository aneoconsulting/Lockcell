workdir="$1"
run="$2"

cd "$workdir" || exit 1
mkdir -p ref

unset VERROU_SOURCE
export VERROU_GEN_SOURCE="./lines.source"

"./${run}" "./ref"
unset VERROU_GEN_SOURCE