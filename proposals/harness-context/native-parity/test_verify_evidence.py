"""Negative controls for false certificates; all use saved evidence, no model calls."""
import copy
from contextlib import redirect_stdout
import io
import json
import unittest
from unittest.mock import patch

import verify_evidence as V


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.audit = V.read(V.HERE / 'paired-trace-review.json')
        self.result = V.read(V.HERE / 'claude-paid/child-result.json')

    def review(self, result=None, review=None):
        return V.review_result(result or self.result,
                               review or self.audit['claude']['semantic_review'], V.ROOT, [])

    def test_actual_four_traces_are_checked_without_certifying_behavior(self):
        receipt = V.verify()
        self.assertEqual(len(receipt['parity_traces_available']), 4)
        self.assertEqual(receipt['checks_failed'], 0)
        self.assertEqual(receipt['behavior_verdict'], 'fail')
        self.assertFalse(receipt['cross_client_goal_complete'])
        self.assertEqual(receipt['broader_runtime_certification']['checks'], receipt['behavior_checks'])
        self.assertEqual(receipt['native_task_result']['verdict'], 'fail')
        self.assertNotIn('complete', receipt['native_task_result'])
        self.assertEqual(receipt['completion_scope']['session_goal_completion'], 'not_assessed')
        self.assertFalse(receipt['completion_scope']['required_authority_gap']['in_frozen_packet'])
        added = receipt['additional_evidence']
        self.assertFalse(added['compact_codex']['runtime_parity_certified'])
        self.assertEqual(added['compact_codex']['child_callbacks']['completed'], 32)
        self.assertFalse(added['claude_native_refusal']['native_pass'])

    def test_require_parity_still_fails_with_additional_evidence(self):
        with patch.object(V.sys, 'argv', ['verify_evidence.py', '--require-parity']), \
                patch.object(V.Path, 'write_text') as writer, redirect_stdout(io.StringIO()):
            self.assertEqual(V.main(), 1)
        receipt = json.loads(writer.call_args.args[0])
        self.assertEqual(receipt['behavior_verdict'], 'fail')
        self.assertFalse(receipt['cross_client_goal_complete'])
        self.assertIn('compact_codex', receipt['additional_evidence'])

    def test_changed_answer_cannot_reuse_semantic_review(self):
        changed = copy.deepcopy(self.result)
        changed['causal_chain'][8] = 'Another function caused the refusal.'
        with self.assertRaisesRegex(AssertionError, 'review binds causal_chain'):
            self.review(result=changed)

    def test_missing_claim_review_is_not_exhaustive(self):
        changed = copy.deepcopy(self.audit['claude']['semantic_review'])
        changed['items'].pop()
        with self.assertRaisesRegex(AssertionError, 'every result field'):
            self.review(review=changed)

    def test_duplicate_review_cannot_hide_omitted_claim(self):
        changed = copy.deepcopy(self.audit['claude']['semantic_review'])
        changed['items'][-1] = copy.deepcopy(changed['items'][0])
        with self.assertRaisesRegex(AssertionError, 'every result field'):
            self.review(review=changed)

    def test_source_quote_must_match_frozen_lines(self):
        changed = copy.deepcopy(self.audit['claude']['semantic_review'])
        changed['items'][0]['sources'][0]['quote'] = 'A different source line'
        with self.assertRaisesRegex(AssertionError, 'exact source excerpt'):
            self.review(review=changed)

    def test_summary_pass_cannot_hide_incorrect_claims(self):
        changed = copy.deepcopy(self.audit['claude']['semantic_review'])
        changed['verdict'] = 'pass'
        with self.assertRaisesRegex(AssertionError, 'cannot hide'):
            self.review(review=changed)

    def test_changed_native_record_invalidates_complete_trace_binding(self):
        changed = dict(self.audit['codex']['traces']['child'])
        changed['sha256'] = '0' * 64
        with self.assertRaisesRegex(AssertionError, 'full trace digest'):
            V.trace(changed, [])

    def test_missing_tool_result_is_detected_from_actual_events(self):
        original = V.events

        def remove_result(rows, client):
            observed = original(rows, client)
            if client == 'codex':
                observed['outputs'].pop(next(iter(observed['outputs'])))
            return observed

        with patch.object(V, 'events', side_effect=remove_result):
            with self.assertRaisesRegex(AssertionError, 'exact reviewed calls and outputs'):
                V.verify()

    def test_role_echo_in_wrong_message_role_is_not_delivery(self):
        original = V.trace

        def change_role(ref, checks):
            rows = original(ref, checks)
            if ref == self.audit['codex']['traces']['child']:
                rows = copy.deepcopy(rows)
                for r in rows:
                    p = r.get('payload', {})
                    if r.get('type') == 'response_item' and p.get('role') == 'developer':
                        p['role'] = 'assistant'
            return rows

        with patch.object(V, 'trace', side_effect=change_role):
            with self.assertRaisesRegex(AssertionError, 'Codex exact role delivered'):
                V.verify()

    def test_changed_actual_parent_prompt_is_detected(self):
        original = V.trace

        def change_prompt(ref, checks):
            rows = original(ref, checks)
            if ref == self.audit['codex']['traces']['parent']:
                rows = copy.deepcopy(rows)
                prompt = (V.HERE / 'parent-prompt.txt').read_text().strip()
                for r in rows:
                    p = r.get('payload', {})
                    if p.get('role') == 'user' and V.collector.text_content(p.get('content')).strip() == prompt:
                        p['content'] = [{'type': 'input_text', 'text': 'Investigate another task.'}]
            return rows

        with patch.object(V, 'trace', side_effect=change_prompt):
            with self.assertRaisesRegex(AssertionError, 'actual parent received saved prompt'):
                V.verify()

    def test_cipher_echo_does_not_substitute_for_child_delivery(self):
        original = V.trace

        def change_envelope(ref, checks):
            rows = original(ref, checks)
            if ref == self.audit['codex']['traces']['child']:
                rows = copy.deepcopy(rows)
                for r in rows:
                    p = r.get('payload', {})
                    if p.get('type') == 'agent_message':
                        p['type'] = 'message'
                        p['role'] = 'assistant'
            return rows

        with patch.object(V, 'trace', side_effect=change_envelope):
            with self.assertRaisesRegex(AssertionError, 'encrypted delegation transport'):
                V.verify()

    def test_claude_streaming_usage_is_deduplicated(self):
        rows = [{'type': 'assistant', 'message': {'id': 'generation1', 'model': 'native',
                 'usage': {'input_tokens': 10, 'cache_creation_input_tokens': 20,
                           'cache_read_input_tokens': 30, 'output_tokens': n}}} for n in (1, 7)]
        observed = V.usage(rows, 'claude')
        self.assertEqual(observed['generations'], 1)
        self.assertEqual(observed['first_input_including_cache'], 60)
        self.assertEqual(observed['total']['output_tokens'], 7)

    def test_json_prefix_and_schema_are_not_literal_json_proof(self):
        semantics = {'codex': {'counts': {'incorrect': 0}, 'verdict': 'pass'},
                     'claude': {'counts': {'incorrect': 0}, 'verdict': 'pass'}}
        verdict = V.behavior(semantics, self.audit['derived_usage'], '{broken JSON')
        check = next(c for c in verdict['checks'] if c['requirement'] == 'Literal JSON-only output')
        self.assertEqual(check['claude'], 'fail')

    def test_all_correct_answers_do_not_prove_missing_runtime_controls(self):
        semantics = {'codex': {'counts': {'incorrect': 0}, 'verdict': 'pass'},
                     'claude': {'counts': {'incorrect': 0}, 'verdict': 'pass'}}
        usage = copy.deepcopy(self.audit['derived_usage'])
        usage['codex']['child']['first']['input_tokens'] = 1
        verdict = V.behavior(semantics, usage, '{}')
        self.assertEqual(verdict['verdict'], 'inconclusive')
        self.assertFalse(verdict['complete'])

    def test_ideal_task_outputs_can_pass_without_broader_runtime_certification(self):
        semantics = {c: {'counts': {'incorrect': 0}, 'verdict': 'pass'} for c in ('claude', 'codex')}
        task = V.native_task_result(semantics, {'claude': '{}', 'codex': '{}'})
        self.assertEqual(task['verdict'], 'pass')
        self.assertNotIn('complete', task)
        for smaller in (True, False):
            usage = copy.deepcopy(self.audit['derived_usage'])
            usage['codex']['child']['first']['input_tokens'] = (
                1 if smaller else usage['codex']['parent']['first']['input_tokens'] + 1)
            runtime = V.behavior(semantics, usage, '{}')
            self.assertEqual(runtime['verdict'], 'inconclusive' if smaller else 'fail')
            self.assertFalse(runtime['complete'])

    def test_native_task_source_errors_fail_even_with_claimed_pass_summary(self):
        for client in ('claude', 'codex'):
            semantics = {c: {'counts': {'incorrect': 0}, 'verdict': 'pass'} for c in ('claude', 'codex')}
            semantics[client]['counts']['incorrect'] = 1
            with self.subTest(client=client):
                self.assertEqual(V.native_task_result(semantics, {'claude': '{}', 'codex': '{}'})['verdict'], 'fail')

    def test_native_task_json_fences_fail_in_either_client(self):
        semantics = {c: {'counts': {'incorrect': 0}, 'verdict': 'pass'} for c in ('claude', 'codex')}
        for client in ('claude', 'codex'):
            raw = {'claude': '{}', 'codex': '{}'}
            raw[client] = '```json\n{}\n```'
            with self.subTest(client=client):
                self.assertEqual(V.native_task_result(semantics, raw)['verdict'], 'fail')

    def test_native_task_qualified_sources_do_not_become_pass(self):
        semantics = {c: {'counts': {'incorrect': 0}, 'verdict': 'inconclusive'} for c in ('claude', 'codex')}
        self.assertEqual(V.native_task_result(semantics, {'claude': '{}', 'codex': '{}'})['verdict'], 'inconclusive')

    def test_native_task_cannot_omit_one_client(self):
        with self.assertRaisesRegex(AssertionError, 'requires both clients'):
            V.native_task_result({'codex': {'counts': {'incorrect': 0}, 'verdict': 'pass'}}, {'codex': '{}'})

    def compact(self, record=None):
        record = record if record is not None else V.read(V.HERE / 'compact-codex-proof.json')
        old = V.trace(self.audit['codex']['traces']['child'], [])
        model = next(r['payload']['model'] for r in old if r.get('type') == 'turn_context')
        schema = V.read(V.Path.home() / 'code/agent-skills/contracts/specialists/development-investigation-result.v1.schema.json')
        return V.verify_compact_codex(record, V.read(V.HERE / 'input/task.json'), schema, [],
                                      (old[0]['payload']['id'], V.usage(old, 'codex'), model))

    def alter_compact_trace(self, kind, change):
        original = V.trace
        ref = V.read(V.HERE / 'compact-codex-proof.json')['traces'][kind]

        def altered(candidate, checks):
            rows = original(candidate, checks)
            if candidate == ref:
                rows = copy.deepcopy(rows)
                change(rows)
            return rows

        return patch.object(V, 'trace', side_effect=altered)

    def refusal(self, record=None):
        return V.verify_claude_refusal(
            record if record is not None else V.read(V.HERE / 'claude-native-refusal.json'),
            V.read(V.HERE / 'input/task.json'), [])

    def test_compact_coalesced_developer_prefix_is_actual_delivery(self):
        record = V.read(V.HERE / 'compact-codex-proof.json')
        rows = V.trace(record['traces']['child'], [])
        role = V.tomllib.loads((V.Path.home() / '.codex/agents/development-investigator.toml').read_text())[
            'developer_instructions'].strip()
        texts = [V.collector.text_content(r['payload'].get('content', [])) for r in rows
                 if r.get('type') == 'response_item' and r['payload'].get('role') == 'developer']
        self.assertTrue(any(t.startswith(role + '\n') and len(t) > len(role) for t in texts))
        self.assertFalse(self.compact()['runtime_parity_certified'])

    def test_compact_role_echo_in_user_or_assistant_cannot_substitute(self):
        for wrong_role in ('user', 'assistant'):
            def change(rows):
                for r in rows:
                    if r.get('type') == 'response_item' and r['payload'].get('role') == 'developer':
                        r['payload']['role'] = wrong_role
            with self.subTest(role=wrong_role), self.alter_compact_trace('child', change):
                with self.assertRaisesRegex(AssertionError, 'actual developer role prefix'):
                    self.compact()

    def test_compact_changed_role_and_preamble_are_rejected(self):
        for prefix in ('Changed instruction.\n', ' '):
            def change(rows):
                for r in rows:
                    p = r.get('payload', {})
                    if r.get('type') == 'response_item' and p.get('role') == 'developer':
                        for b in p.get('content', []):
                            if 'text' in b:
                                b['text'] = prefix + b['text'].replace('development-investigator', 'another-role', 1)
            with self.subTest(prefix=prefix), self.alter_compact_trace('child', change):
                with self.assertRaisesRegex(AssertionError, 'actual developer role prefix'):
                    self.compact()

    def test_compact_native_lineage_change_is_rejected(self):
        def change(rows):
            rows[0]['payload']['source']['subagent']['thread_spawn']['parent_thread_id'] = 'another-parent'
        with self.alter_compact_trace('child', change):
            with self.assertRaisesRegex(AssertionError, 'native source lineage'):
                self.compact()

    def test_compact_spawn_result_must_identify_actual_child(self):
        def change(rows):
            spawn_ids = {r['payload']['call_id'] for r in rows if r.get('type') == 'response_item'
                         and r['payload'].get('name') == 'spawn_agent'}
            for r in rows:
                p = r.get('payload', {})
                if p.get('type') == 'function_call_output' and p.get('call_id') in spawn_ids:
                    p['output'] = json.dumps({'task_name': '/another-child'})
        with self.alter_compact_trace('parent', change):
            with self.assertRaisesRegex(AssertionError, 'spawn result identifies child path'):
                self.compact()

    def test_compact_actual_parent_packet_cannot_be_replaced(self):
        def change(rows):
            for r in rows:
                if r.get('type') == 'response_item' and r['payload'].get('role') == 'user':
                    r['payload']['content'] = [{'type': 'input_text', 'text': 'Another task: {}'}]
        with self.alter_compact_trace('parent', change):
            with self.assertRaisesRegex(AssertionError, 'actual parent received frozen packet'):
                self.compact()

    def test_compact_fork_history_change_is_rejected(self):
        def change(rows):
            for r in rows:
                if r.get('type') == 'response_item' and r['payload'].get('name') == 'spawn_agent':
                    args = json.loads(r['payload']['arguments'])
                    args['fork_turns'] = 'all'
                    r['payload']['arguments'] = json.dumps(args)
        with self.alter_compact_trace('parent', change):
            with self.assertRaisesRegex(AssertionError, 'fresh-history dispatch'):
                self.compact()

    def test_compact_cipher_echo_cannot_substitute_for_child_inbound(self):
        def change(rows):
            for r in rows:
                if r.get('type') == 'response_item' and r['payload'].get('type') == 'agent_message':
                    r['payload']['recipient'] = '/another-child'
        with self.alter_compact_trace('child', change):
            with self.assertRaisesRegex(AssertionError, 'delegation continuity'):
                self.compact()

    def test_compact_parent_forwarding_must_be_raw_identical_json(self):
        def change(rows):
            for r in rows:
                p = r.get('payload', {})
                if p.get('role') == 'assistant' and p.get('phase') == 'final_answer':
                    p['content'] = [{'type': 'output_text', 'text': '{}'}]
        with self.alter_compact_trace('parent', change):
            with self.assertRaisesRegex(AssertionError, 'raw JSON result and parent forwarding'):
                self.compact()

    def test_compact_missing_tool_output_is_not_a_completed_trace(self):
        def change(rows):
            rows[:] = [r for r in rows if r.get('payload', {}).get('type') != 'custom_tool_call_output']
        with self.alter_compact_trace('child', change):
            with self.assertRaisesRegex(AssertionError, 'complete attributed calls and outputs'):
                self.compact()

    def test_compact_claimed_usage_must_match_native_events(self):
        record = V.read(V.HERE / 'compact-codex-proof.json')
        record['derived_usage']['child']['first']['input_tokens'] += 1
        with self.assertRaisesRegex(AssertionError, 'actual native token usage'):
            self.compact(record)

    def test_compact_trace_role_and_task_hashes_are_bound(self):
        for field, expected in [('trace', 'full trace digest'), ('role', 'pinned role body'),
                                ('task', 'same frozen task')]:
            record = V.read(V.HERE / 'compact-codex-proof.json')
            if field == 'trace':
                record['traces']['child']['sha256'] = '0' * 64
            else:
                record[{'role': 'role_body_sha256', 'task': 'task_sha256'}[field]] = '0' * 64
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, expected):
                self.compact(record)

    def test_compact_review_cannot_omit_a_result_field(self):
        record = V.read(V.HERE / 'compact-codex-proof.json')
        record['semantic_review']['items'].pop()
        with self.assertRaisesRegex(AssertionError, 'every result field'):
            self.compact(record)

    def test_compact_permission_assertion_cannot_replace_actual_scope(self):
        record = V.read(V.HERE / 'compact-codex-proof.json')
        record['effective_permissions'][0]['permission_profile']['network'] = 'enabled'
        with self.assertRaisesRegex(AssertionError, 'actual complete effective permission contexts'):
            self.compact(record)

    def test_compact_receipt_omission_duplicate_and_edit_are_rejected(self):
        for action in ('omit', 'duplicate', 'edit'):
            record = V.read(V.HERE / 'compact-codex-proof.json')
            members = record['child_callbacks']['completed_members']
            if action == 'omit':
                members.pop()
            elif action == 'duplicate':
                members[-1] = copy.deepcopy(members[0])
            else:
                members[0]['receipt']['hook_run_id'] = 'another-turn'
            with self.subTest(action=action), self.assertRaisesRegex(AssertionError, 'exact journal membership'):
                self.compact(record)

    def test_compact_per_tool_identity_is_not_promoted_from_turn_receipts(self):
        record = V.read(V.HERE / 'compact-codex-proof.json')
        record['child_callbacks']['per_tool_identity_proven'] = True
        with self.assertRaisesRegex(AssertionError, 'per-tool identity remains unproved'):
            self.compact(record)

    def test_compact_context_comparison_cannot_change_baseline(self):
        record = V.read(V.HERE / 'compact-codex-proof.json')
        record['measured_comparison']['baseline_first_input_tokens'] += 1
        with self.assertRaisesRegex(AssertionError, 'comparison derived from native traces'):
            self.compact(record)

    def test_actual_refusal_success_subtype_is_not_a_successful_run(self):
        observed = self.refusal()
        self.assertEqual(observed['raw_result_subtype'], 'success')
        self.assertTrue(observed['raw_result_is_error'])
        self.assertEqual(observed['native_exit_status'], 1)
        self.assertFalse(observed['native_pass'])

    def test_refusal_false_success_assertion_is_rejected(self):
        record = V.read(V.HERE / 'claude-native-refusal.json')
        record['native_pass'] = True
        with self.assertRaisesRegex(AssertionError, 'public disposition binds native outcome'):
            self.refusal(record)

    def test_refusal_edited_raw_or_canonical_source_digest_is_rejected(self):
        for key in ('raw_line_sha256', 'record_sha256'):
            record = V.read(V.HERE / 'claude-native-refusal.json')
            record['outcome_source'][key] = '0' * 64
            with self.subTest(key=key), self.assertRaisesRegex(AssertionError, 'operational source digests'):
                self.refusal(record)

    def test_refusal_nonerror_result_or_zero_exit_is_not_refusal(self):
        original = V.source_record
        for change in ('error', 'exit', 'children'):
            def altered(ref, checks):
                row = copy.deepcopy(original(ref, checks))
                if 'row' in row and change == 'error':
                    row['row']['is_error'] = False
                elif 'row' in row and change == 'children':
                    row['row']['subagent_stats']['spawned'] = 1
                elif change == 'exit' and 'exit_status' in row:
                    row['exit_status'] = 0
                return row
            expected = 'no native tool dispatch' if change == 'children' else 'actual error flags'
            with self.subTest(change=change), patch.object(V, 'source_record', side_effect=altered):
                with self.assertRaisesRegex(AssertionError, expected):
                    self.refusal()

    def test_refusal_native_error_record_must_actually_exist(self):
        original = V.trace
        ref = V.read(V.HERE / 'claude-native-refusal.json')['parent_trace']

        def altered(candidate, checks):
            rows = original(candidate, checks)
            return [r for r in rows if not r.get('isApiErrorMessage')] if candidate == ref else rows

        with patch.object(V, 'trace', side_effect=altered):
            with self.assertRaisesRegex(AssertionError, 'actual API error record'):
                self.refusal()

    def test_refusal_result_must_match_the_native_error(self):
        original = V.source_record

        def altered(ref, checks):
            row = copy.deepcopy(original(ref, checks))
            if 'row' in row:
                row['row']['result'] = 'An unrelated operational error.'
            return row

        with patch.object(V, 'source_record', side_effect=altered):
            with self.assertRaisesRegex(AssertionError, 'exact native error message'):
                self.refusal()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EvidenceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({'passed': result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
                      'failed': len(result.failures), 'errored': len(result.errors),
                      'skipped': len(result.skipped), 'exit_status': 0 if result.wasSuccessful() else 1}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
