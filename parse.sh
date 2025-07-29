workdir="$1"
run="$2"

cd "$workdir" || exit 1
mkdir -p ref

unset VERROU_SOURCE
export VERROU_GEN_SOURCE="${workdir}/lines.source"

"${workdir}/${run}" "$workdir/ref"