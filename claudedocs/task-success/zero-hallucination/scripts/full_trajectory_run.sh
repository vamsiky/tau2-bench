#!/bin/zsh
# Run full episodes for a list of tasks with zero_hallucination retrieval.
# Tree-kills a stuck episode by save-to name so one hang can't block the batch.
# Usage: full_trajectory_run.sh <prefix> <deadline_s> task_043 task_047 ...
cd /Users/vamsiconversive/github/tau2-bench
export OPENAI_API_KEY=$(grep '^OPENAI_API_KEY=' .env | cut -d= -f2- | tr -d '"')
PREFIX=$1; DEADLINE=$2; shift 2
VARIANT=${VARIANT:-zero_hallucination}
POLICY_ARG=()
[ -n "$POLICY" ] && POLICY_ARG=(--agent-extra-instruction-file "$POLICY")

for task in "$@"; do
  name="${PREFIX}_${task#task_}"
  rm -rf "data/simulations/$name"
  echo "=== RUN $name ($VARIANT $task policy=${POLICY:-none}) $(date +%H:%M:%S) ==="
  uv run python examples/agents/claude_sdk_loop_eval.py \
    --domain banking_knowledge --task-ids $task --num-trials ${TRIALS:-1} \
    --agent-model claude-sonnet-4-6 --sdk-nl-judge --max-steps 40 \
    --retrieval-config $VARIANT --save-to $name --log-level WARNING \
    "${POLICY_ARG[@]}" &
  epid=$!
  ( sleep $DEADLINE
    if kill -0 $epid 2>/dev/null; then
      echo "!!! WATCHDOG kill $name $(date +%H:%M:%S)"
      pkill -9 -f "save-to $name"; pkill -9 -f "_bundled/claude"
    fi ) & wd=$!
  wait $epid; kill $wd 2>/dev/null; wait $wd 2>/dev/null
  r=$(python3 -c "import json;s=json.load(open('data/simulations/$name/results.json'))['simulations'];rs=[(x.get('reward_info') or {}).get('reward') for x in s];print('rewards='+str(rs)+' max='+str(max([x for x in rs if x is not None] or [None]))) if s else print('NO_SIM')" 2>/dev/null || echo "NO_RESULT")
  echo "=== DONE $name $r $(date +%H:%M:%S) ==="
done
echo "=== BATCH COMPLETE $(date +%H:%M:%S) ==="
