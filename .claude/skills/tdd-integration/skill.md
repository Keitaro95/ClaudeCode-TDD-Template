.claude/skills/tdd-integration/skill.md
https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/#the-tdd-skill 

このdescriptionフィールドにはトリガーフレーズが含まれている。
新しいfeatureやfunctionを実装するように指示すると、クロードは自動的にこのスキルを起動します。

```sh
次の3つのphaseに従って新しい機能を実装してください。
フェーズをスキップしないでください
🔴 RED PHASE: Delegating to tdd-test-writer...
Invoke the `tdd-test-writer` subagent with: tdd-test-writerサブエージェントを起動

**Do NOT proceed to Green phase until test failure is confirmed.**

🟢 GREEN PHASE: Delegating to tdd-implementer...
Invoke the `tdd-implementer` subagent with:　tdd-implementerサブエージェントを起動

**Do NOT proceed to Refactor phase until test passes.**

🔵 REFACTOR PHASE: Delegating to tdd-refactorer...
Invoke the `tdd-refactorer` subagent with:　tdd-refactorerサブエージェントを起動

**Cycle complete when refactor phase returns.**
```

各フェーズには「…まで先に進まないでください」という明確なゲートがある。
🔴🟢🔵の絵文字のおかげで、出力で進捗状況を簡単に把握できます。
