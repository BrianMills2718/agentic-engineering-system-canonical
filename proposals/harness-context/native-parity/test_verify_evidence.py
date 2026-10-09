"""Negative controls for false certificates; all use saved evidence, no model calls."""
import copy
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


if __name__ == '__main__':
    import json
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EvidenceTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({'passed': result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped),
                      'failed': len(result.failures), 'errored': len(result.errors),
                      'skipped': len(result.skipped), 'exit_status': 0 if result.wasSuccessful() else 1}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
