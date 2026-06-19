# HARNESS V2 Source Control

status: package_github_surface / remaining_completion_program / source_control

이 파일은 local HARNESS V2 package와 GitHub MVP operation에서 source authority를 정의합니다.

## Source 계층

1. `F:\Folder\harness-v2` 안의 현재 product-local files. 각 파일은 자기 local operating rule에 대해서만 source가 됩니다.
2. 사용자가 특정 work unit에 대해 exact scope로 묶어 준 메시지.
3. historical gate context를 위한 active HARNESS V2 planning gate와 progress ledger.
4. design intent와 boundary language를 위한 confirmed Stage 00~05 planning artifacts.

summary, cached note, subagent report, broad approval, old progress text, registry row, log entry, route suggestion, placeholder text는 그 자체로 source authority가 아닙니다.

## Freshness

source는 자신이 명시한 scope 안에서만 fresh합니다.

target file, write surface, user objective, approval scope, permission scope, proof obligation, lifecycle state, route surface, artifact surface, regression surface, improvement surface, release boundary가 바뀌면 source는 stale이 됩니다.

## 충돌 규칙

source가 충돌하면 target surface를 명시하는 가장 좁고 현재적인 source를 사용하고, 충돌이 해결될 때까지 fail closed합니다.

product-local file이 같은 work unit에 대한 exact user approval packet과 충돌하면, user packet을 write-scope input으로 취급하고 그 packet의 target surface 안에서만 product-local file을 갱신합니다.

## Non-Source 목록

- tool availability
- prior review pass
- subagent confidence
- registry 또는 log 존재
- route suggestion
- placeholder text
- file existence alone
- heading match alone
- readback 없는 search result

이 파일은 approval, permission, proof result, lifecycle state, route permission, regression pass, improvement execution, release readiness를 만들지 않습니다.
