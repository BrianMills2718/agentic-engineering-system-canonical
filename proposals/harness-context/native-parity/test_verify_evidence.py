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
        self.assertEqual(added['authority_codex']['required_policy_delivery'], 'pass')
        self.assertEqual(added['authority_codex']['parent_forwarding_verdict'], 'fail')
        self.assertEqual(added['authority_codex']['canonical_authority_read_coverage']['verdict'], 'inconclusive')

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

    def authority(self, record=None, manifest=None):
        audit = self.audit
        child = V.trace(audit['codex']['traces']['child'], [])
        model = next(r['payload']['model'] for r in child if r['type'] == 'turn_context')
        return V.verify_compact_codex(
            record or V.read(V.HERE / 'authority-context-proof.json'), V.read(V.HERE / 'input/task.json'),
            V.read(V.Path.home() / 'code/agent-skills/contracts/specialists/development-investigation-result.v1.schema.json'),
            [], (child[0]['payload']['id'], audit['derived_usage']['codex']['child'], model),
            manifest or V.read(V.HERE / 'authority-context/manifest.json'))

    def test_authority_run_retains_real_parent_corruption(self):
        result = self.authority()
        self.assertEqual(result['semantic_summary']['counts']['supported'], 23)
        self.assertEqual(result['parent_forwarding_verdict'], 'fail')
        self.assertEqual(result['required_policy_delivery'], 'pass')
        self.assertFalse(result['runtime_parity_certified'])

    def test_authority_parent_failure_cannot_be_relabelled_pass(self):
        record = V.read(V.HERE / 'authority-context-proof.json')
        record['parent_forwarding_verdict'] = 'pass'
        with self.assertRaisesRegex(AssertionError, 'cannot hide changed answer'):
            self.authority(record)

    def test_authority_correct_child_cannot_replace_original_parent(self):
        record = V.read(V.HERE / 'authority-context-proof.json')
        record['parent_raw_final'] = record['raw_final']
        record['parent_final_sha256'] = record['final_sha256']
        with self.assertRaisesRegex(AssertionError, 'parent final bound separately'):
            self.authority(record)

    def test_authority_review_cannot_be_reused_for_parent_answer(self):
        record = V.read(V.HERE / 'authority-context-proof.json')
        with self.assertRaisesRegex(AssertionError, r'review binds evidence\[4\]'):
            V.review_result(json.loads(record['parent_raw_final']), record['semantic_review'], V.ROOT, [])

    def test_authority_different_model_counts_are_not_savings_proof(self):
        result = self.authority()
        self.assertIsNone(result['measured_comparison']['reduction_percent'])
        record = V.read(V.HERE / 'authority-context-proof.json')
        record['measured_comparison']['reduction_percent'] = 37.645
        with self.assertRaisesRegex(AssertionError, 'comparison derived'):
            self.authority(record)

    def test_authority_incomplete_read_cannot_be_relabelled_complete(self):
        record = V.read(V.HERE / 'authority-context-proof.json')
        record['canonical_authority_read_coverage']['verdict'] = 'pass'
        with self.assertRaisesRegex(AssertionError, 'cannot hide truncated lines'):
            self.authority(record)

    def test_authority_reviewed_custom_tool_output_cannot_be_omitted(self):
        record = V.read(V.HERE / 'authority-context-proof.json')
        record['tool_events']['child']['outputs'].pop(next(iter(record['tool_events']['child']['outputs'])))
        with self.assertRaisesRegex(AssertionError, 'reviewed call and return membership'):
            self.authority(record)

    def test_authority_source_revision_and_prepared_body_are_bound(self):
        manifest = V.read(V.HERE / 'authority-context/manifest.json')
        manifest['source']['revision'] = '0000000000000000000000000000000000000000'
        with self.assertRaisesRegex(AssertionError, 'required source identity'):
            self.authority(manifest=manifest)

    def test_authority_document_bytes_cannot_be_changed(self):
        manifest = V.read(V.HERE / 'authority-context/manifest.json')
        manifest['source']['sha256'] = '0' * 64
        with self.assertRaisesRegex(AssertionError, 'exact source revision bytes'):
            self.authority(manifest=manifest)

    def test_authority_echo_cannot_replace_child_developer_delivery(self):
        record = V.read(V.HERE / 'authority-context-proof.json')
        original = V.trace
        def altered(ref, checks):
            rows = original(ref, checks)
            if ref == record['traces']['child']:
                rows = copy.deepcopy(rows)
                for row in rows:
                    p = row.get('payload', {})
                    if p.get('role') == 'developer':
                        p['role'] = 'assistant'
            return rows
        with patch.object(V, 'trace', side_effect=altered):
            with self.assertRaisesRegex(AssertionError, 'actual developer role prefix'):
                self.authority(record)

    def test_authority_parent_echo_cannot_replace_developer_delivery(self):
        record = V.read(V.HERE / 'authority-context-proof.json')
        original = V.trace
        def altered(ref, checks):
            rows = original(ref, checks)
            if ref == record['traces']['parent']:
                rows = copy.deepcopy(rows)
                for row in rows:
                    p = row.get('payload', {})
                    if p.get('role') == 'developer':
                        p['role'] = 'assistant'
            return rows
        with patch.object(V, 'trace', side_effect=altered):
            with self.assertRaisesRegex(AssertionError, 'native parent developer context'):
                self.authority(record)

    def source_delivery_rows(self):
        packet = V.read(V.HERE / 'input/task.json')
        rows, calls = [], {}
        for i, path in enumerate(packet['canonical_authority_paths']):
            call = f'source-call-{i}'
            calls[path] = [call]
            command = 'nl -ba ' + path
            source = '\n'.join(f'{n:6}\t{line}' for n, line in enumerate(
                (V.ROOT / path).read_text().splitlines(), 1))
            rows.extend([
                {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'call_id': call,
                    'name': 'exec', 'input': 'const r = await tools.exec_command({cmd: ' + json.dumps(command) +
                    '}); text(r.output); text({exit_code:r.exit_code,session_id:r.session_id??null});'}},
                {'type': 'response_item', 'payload': {'type': 'custom_tool_call_output', 'call_id': call,
                    'output': [{'type': 'text', 'text': 'Script completed\nOutput:\n' + source + '\n' +
                               json.dumps({'exit_code': 0, 'session_id': None})}]}}])
        return packet, rows, calls

    def test_delivery_source_metadata_is_unwrapped_and_source_bound(self):
        packet, rows, calls = self.source_delivery_rows()
        # Native envelopes can serialize nested text JSON under the completion prefix.
        rows[1]['payload']['output'] = [{'type': 'text', 'text': json.dumps({
            'content': rows[1]['payload']['output']})}]
        result = V.derive_source_call_outcomes(rows, [])
        self.assertEqual(len(result), 2)
        self.assertEqual(result['source-call-0'], {'command': 'nl -ba ' + packet['canonical_authority_paths'][0],
                                                 'exit_code': 0, 'session_id': None, 'outcome': 'success',
                                                 'output_truncated': False})
        self.assertEqual(V.verify_authority_reads(rows, calls, packet, [], strict=True)['verdict'], 'pass')

    def test_delivery_missing_nonzero_ongoing_or_ambiguous_shell_outcome_is_rejected(self):
        for mutation in ('missing', 'nonzero', 'ongoing', 'boolean', 'duplicate'):
            _, rows, _ = self.source_delivery_rows()
            text = rows[1]['payload']['output'][0]['text']
            marker = json.dumps({'exit_code': 0, 'session_id': None})
            replacement = {'missing': '', 'nonzero': json.dumps({'exit_code': 1, 'session_id': None}),
                           'ongoing': json.dumps({'exit_code': None, 'session_id': 42}),
                           'boolean': json.dumps({'exit_code': False, 'session_id': None}),
                           'duplicate': marker + '\n' + marker}[mutation]
            rows[1]['payload']['output'][0]['text'] = text.replace(marker, replacement)
            with self.subTest(mutation=mutation), self.assertRaisesRegex(AssertionError, 'shell outcome'):
                V.derive_source_call_outcomes(rows, [])

    def test_delivery_source_outcome_cannot_come_from_another_call(self):
        _, rows, _ = self.source_delivery_rows()
        rows[1]['payload']['call_id'] = 'unrelated-call'
        with self.assertRaisesRegex(AssertionError, 'complete source-call membership'):
            V.derive_source_call_outcomes(rows, [])

    def test_delivery_duplicate_call_or_return_identity_is_ambiguous(self):
        for index in (0, 1):
            _, rows, _ = self.source_delivery_rows()
            rows.append(copy.deepcopy(rows[index]))
            with self.subTest(index=index), self.assertRaisesRegex(AssertionError, 'unique source-call and return'):
                V.derive_source_call_outcomes(rows, [])

    def test_delivery_empty_standalone_rg_no_matches_retains_exit_one(self):
        packet, rows, calls = self.source_delivery_rows()
        path = packet['canonical_authority_paths'][0]
        command = "rg -n 'absent|also_absent' " + path
        rows[0]['payload']['input'] = rows[0]['payload']['input'].replace('nl -ba ' + path, command)
        rows[1]['payload']['output'] = [
            {'type': 'input_text', 'text': 'Script completed\nWall time 1.0 seconds\nOutput:\n'},
            {'type': 'input_text', 'text': ''},
            {'type': 'input_text', 'text': json.dumps({'exit_code': 1, 'session_id': None})}]
        result = V.derive_source_call_outcomes(rows, [])
        self.assertEqual(result['source-call-0'], {'command': command, 'exit_code': 1,
                                                 'session_id': None, 'outcome': 'no_matches',
                                                 'output_truncated': False})
        with self.assertRaisesRegex(AssertionError, 'required source read has successful terminal outcome'):
            V.verify_authority_reads(rows, calls, packet, [], strict=True)

    def test_delivery_rg_errors_output_or_compound_search_cannot_be_no_matches(self):
        for command, code, output in [("rg 'absent' file", 2, ''),
                                      ("rg 'absent' file", 1, 'rg: file: Permission denied'),
                                      ("rg 'absent' file", 1, 'a returned source line'),
                                      ("rg 'absent' file | cat", 1, ''),
                                      ("rg 'absent' file; true", 1, ''),
                                      ("rg 'absent' file && true", 1, ''),
                                      ("rg 'absent' $(other)", 1, ''),
                                      ("cat file", 1, '')]:
            _, rows, _ = self.source_delivery_rows()
            rows[0]['payload']['input'] = ('const r = await tools.exec_command({cmd: ' + json.dumps(command) +
                '});text(r.output);text({exit_code:r.exit_code,session_id:r.session_id??null});')
            rows[1]['payload']['output'] = [
                {'type': 'input_text', 'text': 'Script completed\nWall time 1.0 seconds\nOutput:\n'},
                {'type': 'input_text', 'text': output},
                {'type': 'input_text', 'text': json.dumps({'exit_code': code, 'session_id': None})}]
            with self.subTest(command=command, code=code, output=output), \
                    self.assertRaisesRegex(AssertionError, 'successful shell outcome or empty standalone rg'):
                V.derive_source_call_outcomes(rows, [])

    def test_delivery_constant_metadata_echo_cannot_replace_native_outcome(self):
        for echo in ('text({exit_code:0,session_id:null});',
                     'text({exit_code:other.exit_code,session_id:other.session_id??null});'):
            _, rows, _ = self.source_delivery_rows()
            rows[0]['payload']['input'] = rows[0]['payload']['input'].replace(
                'text({exit_code:r.exit_code,session_id:r.session_id??null});', echo)
            with self.subTest(echo=echo), self.assertRaisesRegex(AssertionError, 'native outcome emission'):
                V.derive_source_call_outcomes(rows, [])

    def test_delivery_wrapper_cannot_rewrite_native_outcome_or_execute_options(self):
        for config in ('{cmd:"nl -ba file"});r.exit_code=0;const ignored=({}',
                       '{cmd:"nl -ba file",max_output_tokens:(hidden=0)}',
                       '{cmd:"nl -ba file",cmd:"other"}'):
            code = ('const r = await tools.exec_command(' + config +
                    ');text(r.output);text({exit_code:r.exit_code,session_id:r.session_id??null});')
            with self.subTest(config=config), self.assertRaisesRegex(AssertionError, 'literal source-shell command'):
                V.shell_command({'type':'custom_tool_call', 'input':code})
        command = 'rg "{literal}" file'
        code = ('const r = await tools.exec_command({cmd:' + json.dumps(command) +
                ',max_output_tokens:1000});text(r.output);text({exit_code:r.exit_code,session_id:r.session_id??null});')
        self.assertEqual(V.shell_command({'type':'custom_tool_call', 'input':code}), command)

    def test_delivery_source_command_must_be_literal_and_attributed(self):
        packet, rows, calls = self.source_delivery_rows()
        rows[0]['payload']['input'] = 'const r = await tools.exec_command({cmd: hidden});'
        with self.assertRaisesRegex(AssertionError, 'literal source-shell command'):
            V.derive_source_call_outcomes(rows, [])
        rows[0]['payload']['input'] = 'const r = await tools.exec_command({cmd: "nl -ba " + hidden});'
        with self.assertRaisesRegex(AssertionError, 'literal source-shell command'):
            V.derive_source_call_outcomes(rows, [])
        rows[0]['payload']['input'] = ('const r = await tools.exec_command({cmd: "nl -ba unrelated.md"});'
                                       'text(r.output); text({exit_code:r.exit_code,session_id:r.session_id??null});')
        with self.assertRaisesRegex(AssertionError, 'exact source-read command'):
            V.verify_authority_reads(rows, calls, packet, [], strict=True)

    def test_delivery_missing_authority_line_is_not_complete(self):
        packet, rows, calls = self.source_delivery_rows()
        path = packet['canonical_authority_paths'][0]
        line = (V.ROOT / path).read_text().splitlines()[134]
        rows[1]['payload']['output'][0]['text'] = rows[1]['payload']['output'][0]['text'].replace(
            f'{135:6}\t{line}', '')
        coverage = V.verify_authority_reads(rows, calls, packet, [], strict=True)
        self.assertEqual(coverage['verdict'], 'inconclusive')
        self.assertEqual(coverage['sources'][path]['missing_exact_lines'], [135])

    def test_delivery_authority_path_substring_or_nonread_command_is_rejected(self):
        for suffix, prefix in (('.other', 'nl -ba '), ('', 'printf '), ('; true', 'nl -ba ')):
            packet, rows, calls = self.source_delivery_rows()
            path = packet['canonical_authority_paths'][0]
            rows[0]['payload']['input'] = rows[0]['payload']['input'].replace(
                'nl -ba ' + path, prefix + path + suffix)
            with self.subTest(suffix=suffix, prefix=prefix), self.assertRaisesRegex(AssertionError, 'exact source-read command'):
                V.verify_authority_reads(rows, calls, packet, [], strict=True)

    def test_delivery_truncated_authority_can_recover_only_with_exact_missing_lines(self):
        packet, rows, calls = self.source_delivery_rows()
        path = packet['canonical_authority_paths'][0]
        source = (V.ROOT / path).read_text().splitlines()
        first = rows[1]['payload']['output'][0]
        removed = '\n'.join(f'{n:6}\t{source[n-1]}' for n in range(130, 141))
        first['text'] = first['text'].replace(removed, 'Warning: truncated output (11 tokens truncated)')
        self.assertEqual(V.verify_authority_reads(rows, calls, packet, [], strict=True)['verdict'], 'inconclusive')
        recovery = copy.deepcopy(rows[:2])
        for row in recovery:
            row['payload']['call_id'] = 'recovery-call'
        recovery[0]['payload']['input'] = 'const r = await tools.exec_command({cmd: ' + json.dumps(
            'nl -ba ' + path + " | sed -n '130,140p'") + (
                '});text(r.output);text({exit_code:r.exit_code,session_id:r.session_id??null});')
        recovery[1]['payload']['output'] = [{'type': 'text', 'text': removed + '\n' +
                                          json.dumps({'exit_code': 0, 'session_id': None})}]
        rows.extend(recovery)
        calls[path].append('recovery-call')
        coverage = V.verify_authority_reads(rows, calls, packet, [], strict=True)
        self.assertEqual(coverage['verdict'], 'pass')
        self.assertEqual(coverage['sources'][path]['truncated_call_ids'], ['source-call-0'])
        outcomes = V.derive_source_call_outcomes(rows, [])
        self.assertEqual(len(outcomes), 3)
        self.assertTrue(outcomes['source-call-0']['output_truncated'])
        self.assertFalse(outcomes['recovery-call']['output_truncated'])

    def test_delivery_collector_uses_only_exact_parent_child_index_and_native_bytes(self):
        proof = V.read(V.HERE / 'authority-context-proof.json')
        original = V.collector.enrich
        seen = []
        def inspect_index(run, index):
            seen.append(set(index))
            return original(run, index)
        with patch.object(V.collector, 'enrich', side_effect=inspect_index):
            result = V.derive_native_delivery(proof['traces']['parent'], proof['traces']['child'], [])
        self.assertEqual(result['collector_result'], proof['raw_final'])
        self.assertEqual(result['result_sha256'], proof['final_sha256'])
        self.assertEqual(result['consumer'], 'native-parity-evidence-checker')
        self.assertEqual(seen, [{result['parent_session_id'], result['child_session_id']}])

    def test_delivery_corrupted_collector_result_is_rejected(self):
        proof = V.read(V.HERE / 'authority-context-proof.json')
        original = V.collector.enrich
        def corrupt(run, index):
            original(run, index)
            run['result'] += '\n'
        with patch.object(V.collector, 'enrich', side_effect=corrupt), \
                self.assertRaisesRegex(AssertionError, 'completed native child result'):
            V.derive_native_delivery(proof['traces']['parent'], proof['traces']['child'], [])

    def test_delivery_multiple_native_final_blocks_cannot_share_a_lossy_normalization(self):
        proof = V.read(V.HERE / 'authority-context-proof.json')
        ref = proof['traces']['child']
        child = copy.deepcopy(V.trace(ref, []))
        final = next(r['payload'] for r in child if r.get('type') == 'response_item'
                     and r['payload'].get('phase') == 'final_answer')
        raw = final['content'][0]['text']
        final['content'] = [{'type': 'output_text', 'text': raw[:1]},
                            {'type': 'output_text', 'text': raw[1:]}]
        original_trace, original_rows = V.trace, V.collector.rows
        def changed_trace(candidate, checks):
            return child if candidate == ref else original_trace(candidate, checks)
        def changed_rows(path):
            return enumerate(child) if str(path) == ref['path'] else original_rows(path)
        with patch.object(V, 'trace', side_effect=changed_trace), \
                patch.object(V.collector, 'rows', side_effect=changed_rows), \
                self.assertRaisesRegex(AssertionError, 'one unambiguous native final text block'):
            V.derive_native_delivery(proof['traces']['parent'], ref, [])

    def test_delivery_ambiguous_dispatch_or_lineage_mismatch_is_rejected(self):
        proof = V.read(V.HERE / 'authority-context-proof.json')
        original = V.collector.calls
        for mutation in ('duplicate', 'parent', 'child'):
            def alter(path, client):
                runs, receipts = original(path, client)
                if mutation == 'duplicate':
                    runs.append(copy.deepcopy(runs[0]))
                else:
                    runs[0]['parent_session_id' if mutation == 'parent' else 'child_ref'] = 'wrong-native-identity'
                return runs, receipts
            with self.subTest(mutation=mutation), patch.object(V.collector, 'calls', side_effect=alter), \
                    self.assertRaisesRegex(AssertionError, 'unambiguous native dispatch|native dispatch lineage'):
                V.derive_native_delivery(proof['traces']['parent'], proof['traces']['child'], [])

    def test_delivery_native_parent_routing_receipt_cannot_be_rewritten(self):
        child = '/root/maintenance_discovery'
        receipt = {'schema_version': 'native-child-routing-receipt/v1', 'child_ref': child,
                   'delivery': 'native_collector', 'consumer': 'native-parity-evidence-checker'}
        raw = json.dumps(receipt)
        V.verify_routing_receipt(raw, receipt, child, [])
        for field in ('child_ref', 'delivery', 'consumer'):
            changed = {**receipt, field: 'rewritten'}
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, 'native parent routing receipt'):
                V.verify_routing_receipt(raw, changed, child, [])
            with self.subTest(native_field=field), self.assertRaisesRegex(AssertionError, 'native parent routing receipt'):
                V.verify_routing_receipt(json.dumps(changed), changed, child, [])

    def test_delivery_receipt_before_frozen_task_is_structural_packet_delivery(self):
        packet = V.read(V.HERE / 'input/task.json')
        receipt = {'schema_version': 'native-child-routing-receipt/v1',
                   'child_ref': '/root/maintenance_discovery', 'delivery': 'native_collector',
                   'consumer': 'native-parity-evidence-checker'}
        prompt = 'Return this receipt: ' + json.dumps(receipt) + '\nUnchanged TaskV1:\n' + json.dumps(packet)
        self.assertTrue(V.packet_in_text(prompt, packet))
        self.assertFalse(V.packet_in_text(json.dumps(receipt), packet))
        changed = {**packet, 'task_id': 'a-different-task'}
        self.assertFalse(V.packet_in_text(json.dumps(receipt) + '\n' + json.dumps(changed), packet))

    def test_delivery_duplicate_frozen_task_is_not_unambiguous_delivery(self):
        packet = V.read(V.HERE / 'input/task.json')
        self.assertFalse(V.packet_in_text(json.dumps(packet) + '\n' + json.dumps(packet), packet))

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
