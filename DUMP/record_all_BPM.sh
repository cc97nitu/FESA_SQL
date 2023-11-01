#!/usr/env/bash

killbg() {
        for p in "${pids[@]}" ; do
                kill "$p";
        done
}

trap killbg EXIT

pids=()

python psql_bpm_individual.py --bpm 1 &
pids+=($!)
python psql_bpm_individual.py --bpm 2 &
pids+=($!)
python psql_bpm_individual.py --bpm 3 &
pids+=($!)
python psql_bpm_individual.py --bpm 4 &
pids+=($!)
python psql_bpm_individual.py --bpm 5 &
pids+=($!)
python psql_bpm_individual.py --bpm 6 &
pids+=($!)
python psql_bpm_individual.py --bpm 7 &
pids+=($!)
python psql_bpm_individual.py --bpm 8 &
pids+=($!)
python psql_bpm_individual.py --bpm 9 &
pids+=($!)
python psql_bpm_individual.py --bpm 10 &
pids+=($!)
python psql_bpm_individual.py --bpm 11 &
pids+=($!)
python psql_bpm_individual.py --bpm 12 &
pids+=($!)

wait
