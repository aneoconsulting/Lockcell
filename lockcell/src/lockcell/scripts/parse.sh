workdir="$1"
run="$2"

cd "$workdir" || exit 1
mkdir -p ref

unset VERROU_SOURCE
export VERROU_GEN_SOURCE="./lines.source"


"./${run}" "./ref" 
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "DD_RUN failed with status ${exit_code}" >&2
    exit $exit_code
fi

unset VERROU_GEN_SOURCE
exit 0
