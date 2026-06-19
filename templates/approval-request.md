# HARNESS V2 Approval Request 템플릿

status: template / not_approval / not_permission / not_execution

```text
Approve <work unit>:
<root> 아래에서 아래 path만 만들거나 수정:
<path list>
verification only로 허용할 local command:
<command list>
package metadata, package build, install, publish, deploy, release, git,
dependency install, secret access, external network mutation, destructive operation 금지.
```

이 템플릿은 user response가 아니며, 자체로 approval을 묶지 않습니다.
