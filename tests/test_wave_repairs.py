"""Behavioral controls for the proposed wave repair, before canonical landing."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def skill(root, name, body='---\nname: example\n---\n'):
    path = root / '.claude' / 'skills' / name / 'SKILL.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    return path


def test_absence_is_not_pass_and_warning_survives_summary(tmp_path):
    hc = load('health_check')
    skill(tmp_path, hc.D71_STRUCTURAL_SKILLS[0])
    data = hc.run_housekeeping(tmp_path)
    check = next(c for c in data['checks'] if c['name'] == 'structural_skill_frontmatter')
    assert check['skipped'] and check['severity'] == 'warning'
    # D-prime: boolean, and False for an absent subject. `skipped` is the only
    # discriminator between this row and a real failure.
    assert check['passed'] is False
    assert all('skipped' in c for c in data['checks']), 'skipped is mandatory on every row'
    assert data['summary']['passed'] == sum(bool(c['passed']) and not c['skipped'] for c in data['checks'])
    assert data['summary']['warnings'] == sum(
        c['severity'] == 'warning' and not c['passed'] for c in data['checks'])
    assert sum(data['summary'][key] for key in ('passed', 'failed', 'skipped')) == data['summary']['total']
    assert data['status'] != 'healthy'
    assert 'Skipped:' in hc.format_human_output(data)


def test_advisory_pass_cannot_manufacture_a_permanent_warning(tmp_path):
    """F2: severity counters stay gated on the verdict.

    A check may pass AND carry severity='warning' (an advisory note on a healthy
    subject). Counting severity unconditionally makes that row increment
    `warnings` on every future run, so status never returns to healthy and exit 1
    becomes a floor no repair can clear.
    """
    hc = load('health_check')
    hc.check_sessions_directory = lambda path: hc.CheckResult(
        'sessions_directory', True, 'fine, with a note', severity='warning')
    data = hc.run_housekeeping(tmp_path)
    advisory = next(c for c in data['checks'] if c['name'] == 'sessions_directory')
    assert advisory['passed'] is True and advisory['severity'] == 'warning'
    # The falsifier: warnings counted WITHOUT this row must equal warnings
    # counted WITH it. Ungate the counter and this goes off by one.
    others = [c for c in data['checks'] if c['name'] != 'sessions_directory']
    assert data['summary']['warnings'] == sum(
        c['severity'] == 'warning' and not c['passed'] for c in others)


def test_zero_verified_run_warns_and_never_reports_healthy(tmp_path):
    """Point 5: the zero-verified guard lands on WARNING/exit 1, not a new code."""
    hc = load('health_check')
    for name in [fn for fn in dir(hc) if fn.startswith('check_')]:
        setattr(hc, name, lambda path, _n=name: hc.CheckResult(
            _n, False, 'absent', severity='info', skipped=True))
    data = hc.run_housekeeping(tmp_path)
    assert data['summary']['passed'] == 0 and data['summary']['skipped'] > 0
    assert data['summary']['warnings'] == 0, 'guard must not need a warning row'
    # Zero verified is not healthy, and it is WARNING — not a fourth token.
    assert data['status'] == 'warning'
    text = hc.format_human_output(data)
    assert 'Checks: 0/0 passed' in text
    assert f"Skipped: {data['summary']['skipped']} (not verified)" in text
    assert '[SKIP]' in text


def test_absent_permission_file_is_a_verified_pass_not_a_skip(tmp_path):
    """SITE 8: absence is dispositive here — zero permissions cannot exceed a cap."""
    result = load('health_check').check_permission_accumulation(tmp_path)
    assert result.passed is True and result.skipped is False
    assert 'no .claude/settings*.json present' in result.message


def test_reliance_wiring_gap_is_unverified_not_failed(tmp_path):
    """F6: a manifest with no validator is a skip+warning, like its twin."""
    hc = load('health_check')
    (tmp_path / '.aget').mkdir()
    (tmp_path / '.aget' / 'skill_reliance_manifest.yaml').write_text('skills: []\n')
    result = hc.check_reliance_manifest(tmp_path)
    assert result.skipped and result.severity == 'warning' and result.passed is False
    assert 'not verified' in result.message
    # And with no manifest at all the absence is lawful, so info.
    (tmp_path / '.aget' / 'skill_reliance_manifest.yaml').unlink()
    absent = hc.check_reliance_manifest(tmp_path)
    assert absent.skipped and absent.severity == 'info'


def test_full_inventory_passes_and_local_extension_is_not_required(tmp_path):
    hc = load('health_check')
    for name in hc.D71_STRUCTURAL_SKILLS:
        skill(tmp_path, name)
    result = hc.check_structural_skill_frontmatter(tmp_path)
    assert result.passed and not result.skipped
    skill(tmp_path, 'aget-check-facts', '---\ndisable-model-invocation: true\n---\n')
    assert hc.check_structural_skill_frontmatter(tmp_path).passed


def test_real_violation_is_not_hidden_by_other_missing_skills(tmp_path):
    hc = load('health_check')
    skill(tmp_path, hc.D71_STRUCTURAL_SKILLS[0], '---\ndisable-model-invocation: true\n---\n')
    result = hc.check_structural_skill_frontmatter(tmp_path)
    assert not result.passed and not result.skipped and result.severity == 'error'


def test_unreadable_skill_cannot_pass(tmp_path):
    hc = load('health_check')
    for name in hc.D71_STRUCTURAL_SKILLS:
        skill(tmp_path, name)
    skill(tmp_path, hc.D71_STRUCTURAL_SKILLS[0]).write_bytes(b'\xff')
    result = hc.check_structural_skill_frontmatter(tmp_path)
    assert result.skipped and result.severity == 'warning' and result.passed is False
    assert 'UNREADABLE:' in result.message


def test_no_skill_subject_is_distinct_from_verified(tmp_path):
    result = load('health_check').check_structural_skill_frontmatter(tmp_path)
    assert result.skipped and result.severity == 'info' and result.passed is False


def test_missing_checker_counts_only_actual_documents(tmp_path):
    hc = load('health_check')
    specs = tmp_path / 'specs'
    specs.mkdir()
    (specs / 'one.md').write_text('claim')
    (specs / 'directory.md').mkdir()
    result = hc.check_spec_enforcement_truthfulness(tmp_path)
    assert result.skipped and result.severity == 'warning' and result.passed is False
    assert '1 spec document(s)' in result.message


def test_legacy_output_without_skipped_key_still_renders():
    hc = load('health_check')
    result = hc.format_human_output({'status': 'healthy', 'summary': {
        'total': 1, 'passed': 1, 'warnings': 0, 'errors': 0, 'fixable': 0},
        'checks': [{'name': 'legacy', 'passed': True, 'message': 'ok', 'severity': 'info'}]})
    assert '1/1 passed' in result


def test_candidates_cover_local_and_both_canonical_layouts(tmp_path):
    ga = load('ground_artifact')
    repo = tmp_path / 'seat'
    paths = [repo / 'ontology' / 'ONTOLOGY_worker.yaml',
             tmp_path / 'aget' / 'ontology' / 'ONTOLOGY_canonical.yaml',
             tmp_path / 'aget-framework' / 'aget' / 'ontology' / 'ONTOLOGY_nested.yaml']
    for path in paths:
        path.parent.mkdir(parents=True)
        path.write_text('')
    assert ga._ontology_candidates(repo) == paths


def test_worker_dialect_and_altlabels_coexist(tmp_path):
    ga = load('ground_artifact')
    onto = tmp_path / 'ontology.yaml'
    onto.write_text('- id: WRK-001\n  uri: aget:archetype/worker/Task\n'
                    '  prefLabel: Task\n  altLabel:\n    - Work Assignment\n'
                    '- id: C123\n  uri: aget:concept/Scope\n  prefLabel: Scope\n')
    concepts = ga.load_ontology(onto)
    assert [c['id'] for c in concepts] == ['WRK-001', 'C123']
    assert ('Work Assignment', 'altLabel') in list(ga.concept_labels(concepts[0]))


def test_absent_ontology_is_empty(tmp_path):
    assert load('ground_artifact')._ontology_candidates(tmp_path / 'seat') == []


def test_portfolio_resolution_does_not_descend_into_another_seat(tmp_path, monkeypatch):
    st = load('study_topic')
    monkeypatch.delenv(st.CANONICAL_ROOT_ENV, raising=False)
    agent = tmp_path / 'github' / 'portfolio' / 'seat'
    agent.mkdir(parents=True)
    canonical = tmp_path / 'github' / 'aget-framework' / 'aget' / 'specs'
    decoy = tmp_path / 'github' / 'other-portfolio' / 'other-seat' / 'aget' / 'specs'
    for path in (canonical, decoy):
        path.mkdir(parents=True)
        (path / 'AGET_SESSION_SPEC.md').write_text('marker')
        (path.parent / 'docs' / 'patterns').mkdir(parents=True)
    assert st.find_canonical_spec_roots(agent) == [canonical]
    assert st.find_canonical_pattern_roots(agent) == [canonical.parent / 'docs' / 'patterns']


def test_unmounted_portfolio_does_not_resolve_nested_foreign_tree(tmp_path, monkeypatch):
    st = load('study_topic')
    monkeypatch.delenv(st.CANONICAL_ROOT_ENV, raising=False)
    agent = tmp_path / 'portfolio' / 'seat'
    agent.mkdir(parents=True)
    foreign = tmp_path / 'other' / 'foreign-seat' / 'aget' / 'specs'
    foreign.mkdir(parents=True)
    (foreign / 'AGET_SESSION_SPEC.md').write_text('marker')
    assert st.find_canonical_spec_roots(agent) == []
    st.refresh_canonical_spec_surface(agent)
    assert any('UNAVAILABLE' in row for row in st.SURFACES_SEARCHED)


def test_explicit_root_selects_authority_without_appending_decoys(tmp_path, monkeypatch):
    st = load('study_topic')
    agent = tmp_path / 'portfolio' / 'seat'
    agent.mkdir(parents=True)
    selected = tmp_path / 'declared' / 'specs'
    sibling = agent.parent / 'decoy' / 'specs'
    for path in (selected, sibling):
        path.mkdir(parents=True)
        (path / 'AGET_SESSION_SPEC.md').write_text('marker')
    monkeypatch.setenv(st.CANONICAL_ROOT_ENV, str(selected.parent))
    assert st.find_canonical_spec_roots(agent) == [selected]
    assert not any('siblings' in x for x in st.canonical_search_scope())


def test_nested_relative_config_is_resolved_from_seat(tmp_path, monkeypatch):
    import json
    st = load('study_topic')
    monkeypatch.delenv(st.CANONICAL_ROOT_ENV, raising=False)
    agent = tmp_path / 'seat'
    (agent / '.aget').mkdir(parents=True)
    specs = tmp_path / 'declared' / 'specs'
    specs.mkdir(parents=True)
    (specs / 'AGET_SESSION_SPEC.md').write_text('marker')
    (agent / '.aget' / 'config.json').write_text(json.dumps({
        'study_topic': {'canonical_root': '../declared'}}))
    assert [p.resolve() for p in st.find_canonical_spec_roots(agent)] == [specs.resolve()]


def test_release_gate_derives_framework_membership_from_health_owner():
    spec = importlib.util.spec_from_file_location(
        'release_gate', ROOT / 'verification' / 'validate_release_gate.py')
    release_gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(release_gate)
    expected = ('aget-create-project', 'aget-close-project',
                'aget-create-initiative', 'aget-file-issue')
    assert load('health_check').D71_STRUCTURAL_SKILLS == expected
    assert release_gate.D71_STRUCTURAL_SKILLS == expected


def test_health_logger_preserves_all_verdicts_and_warning_severity():
    logger = load('health_logger')
    data = {'checks': [
        {'name': 'clean', 'passed': True, 'severity': 'info', 'message': 'ok'},
        # D-prime shape: boolean False + skipped. This is the row that a
        # verdict-blind ladder would log as a failure.
        {'name': 'absent', 'passed': False, 'skipped': True, 'severity': 'warning', 'message': 'missing'},
        {'name': 'broken', 'passed': False, 'severity': 'error', 'message': 'bad'},
        {'name': 'legacy', 'status': 'OK', 'details': 'old shape'},
        # An advisory PASS must not be logged as a warning (F2, one layer out).
        {'name': 'advisory', 'passed': True, 'severity': 'warning', 'message': 'noted'},
        # Records written by the rejected nullable arm still deserialise as skips.
        {'name': 'legacy_null', 'passed': None, 'skipped': True, 'severity': 'info', 'message': 'old'},
    ]}
    result = logger.create_health_record(data, 'test')
    assert [c['status'] for c in result['checks']] == [
        'OK', 'SKIP', 'CRITICAL', 'OK', 'OK', 'SKIP']
    assert result['summary'] == {'ok': 3, 'warn': 1, 'critical': 1, 'skipped': 2}
    assert result['checks'][1]['details'] == 'missing'


def test_health_logger_reads_error_json_and_still_rejects_exit_three(tmp_path, monkeypatch):
    """F5: exit 2 carries a real report. Exit 3 means the script did not run.

    Pre-existing defect, independent of the skip work: the accept-list was
    (0, 1), so every error run's JSON was discarded and scraped as text.
    """
    import json
    from types import SimpleNamespace
    logger = load('health_logger')
    path = tmp_path / 'scripts' / 'health_check.py'
    path.parent.mkdir(); path.write_text('')
    for code, status in [(0, 'healthy'), (1, 'warning'), (2, 'error')]:
        expected = {'status': status, 'checks': [{'passed': False, 'skipped': True}]}
        monkeypatch.setattr(logger.subprocess, 'run', lambda *args, **kwargs:
                            SimpleNamespace(returncode=code, stdout=json.dumps(expected), stderr=''))
        assert logger.run_healthcheck(tmp_path) == expected
    # Exit 3 is a configuration/runtime failure: no report exists to trust.
    monkeypatch.setattr(logger.subprocess, 'run', lambda *args, **kwargs:
                        SimpleNamespace(returncode=3, stdout='{"status": "error"}', stderr=''))
    assert logger.run_healthcheck(tmp_path) != {'status': 'error'}


def test_health_skip_marker_survives_validation_logger(tmp_path):
    hc = load('health_check')
    logger = load('validation_logger')
    text = hc.format_human_output({'status': 'warning', 'summary': {
        'total': 1, 'passed': 0, 'skipped': 1, 'warnings': 0, 'errors': 0, 'fixable': 0},
        'checks': [hc.CheckResult('absent', False, 'not available', skipped=True).to_dict()]})
    assert '[SKIP]' in text
    assert logger.parse_script_output(text, '') == [{'name': 'Absent', 'status': 'skip'}]
    # Legacy negative markers retain their existing meaning.
    assert logger.parse_script_output('[-] broken: failure', '')[0]['status'] == 'fail'
    assert logger.parse_script_output('[+] clean: done', '')[0]['status'] == 'pass'


def test_wind_down_preserves_verified_denominator_and_skips(tmp_path, monkeypatch):
    import json
    from types import SimpleNamespace
    wd = load('wind_down')
    path = tmp_path / 'scripts' / 'health_check.py'
    path.parent.mkdir(); path.write_text('')
    payload = {'status': 'warning', 'summary': {'total': 4, 'passed': 2,
               'skipped': 1, 'warnings': 1, 'errors': 0}}
    monkeypatch.setattr(wd.subprocess, 'run', lambda *args, **kwargs:
                        SimpleNamespace(returncode=1, stdout=json.dumps(payload), stderr=''))
    result = wd.run_health_check(tmp_path)
    assert result['checks_total'] == 3 and result['checks_passed'] == 2
    assert result['checks_skipped'] == 1 and result['status'] == 'warning'



def test_persisted_skip_cannot_manufacture_improving_trend(tmp_path):
    import json
    logger = load('health_logger')
    prior = logger.create_health_record({'status': 'warning', 'checks': [
        {'name': 'subject', 'passed': False, 'skipped': False, 'severity': 'warning'}]}, 'before')
    current = logger.create_health_record({'status': 'warning', 'checks': [
        {'name': 'subject', 'passed': False, 'skipped': True, 'severity': 'info'}]}, 'after')
    log = tmp_path / 'health.jsonl'
    log.write_text(json.dumps(current) + '\n')
    restored = logger.read_prior_record(log)
    assert restored['checks'][0]['status'] == 'SKIP'
    # The subject left the verified population, so no direction can be claimed.
    assert logger.compute_trend(restored, prior) == 'unknown'
    assert logger.detect_regressions(restored, prior) == []


def test_trend_still_reports_when_the_same_checks_stay_skipped():
    """F4: the predicate is a CHANGED verified population, not the mere existence
    of skips. Keying on existence goes dark permanently at any seat carrying one
    standing skip, which is most of them.
    """
    logger = load('health_logger')
    prior = logger.create_health_record({'status': 'warning', 'checks': [
        {'name': 'subject', 'passed': False, 'skipped': False, 'severity': 'warning'},
        {'name': 'absent', 'passed': False, 'skipped': True, 'severity': 'info'}]}, 'before')
    current = logger.create_health_record({'status': 'healthy', 'checks': [
        {'name': 'subject', 'passed': True, 'skipped': False, 'severity': 'info'},
        {'name': 'absent', 'passed': False, 'skipped': True, 'severity': 'info'}]}, 'after')
    assert current['summary']['skipped'] == 1 and prior['summary']['skipped'] == 1
    assert logger.compute_trend(current, prior) == 'improved'


def test_verified_logger_trend_still_reports_real_improvement():
    logger = load('health_logger')
    prior = logger.create_health_record({'status': 'warning', 'checks': [
        {'name': 'subject', 'passed': False, 'severity': 'warning'}]}, 'before')
    current = logger.create_health_record({'status': 'healthy', 'checks': [
        {'name': 'subject', 'passed': True, 'severity': 'info'}]}, 'after')
    assert logger.compute_trend(current, prior) == 'improved'


def test_release_gate_observes_owner_change_instead_of_duplicate_constant(tmp_path):
    import shutil
    (tmp_path / 'scripts').mkdir()
    (tmp_path / 'verification').mkdir()
    (tmp_path / 'scripts' / 'health_check.py').write_text(
        "D71_STRUCTURAL_SKILLS = ('sentinel-owned-route',)\n")
    gate = tmp_path / 'verification' / 'validate_release_gate.py'
    shutil.copyfile(ROOT / 'verification' / 'validate_release_gate.py', gate)
    spec = importlib.util.spec_from_file_location('release_gate_fixture', gate)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.D71_STRUCTURAL_SKILLS == ('sentinel-owned-route',)



def test_wind_down_serializes_pending_work_as_distinct_markdown_items(tmp_path):
    wd = load('wind_down')
    pending = ['PROJECT_PLAN_ALPHA.md', 'PROJECT_PLAN_BETA.md']
    rel = wd.create_session_file(tmp_path, {'pending_work': pending}, mandatory=True)
    text = (tmp_path / rel).read_text()
    assert '## Pending Work\n\n- PROJECT_PLAN_ALPHA.md\n- PROJECT_PLAN_BETA.md' in text
    assert str(pending) not in text


def test_wind_down_empty_pending_work_is_explicit_prose(tmp_path):
    wd = load('wind_down')
    rel = wd.create_session_file(tmp_path, {'pending_work': []})
    text = (tmp_path / rel).read_text()
    assert '## Pending Work\n\nNone.' in text
    assert '\n[]\n' not in text


def test_structural_success_names_only_framework_population(tmp_path):
    """A clean framework population makes no claim about a seat's extra routes."""
    hc = load('health_check')
    for name in hc.D71_STRUCTURAL_SKILLS:
        skill(tmp_path, name)
    # A local route is deliberately outside this canonical check's population.
    skill(tmp_path, 'aget-check-facts', '---\ndisable-model-invocation: true\n---\n')
    result = hc.check_structural_skill_frontmatter(tmp_path)
    assert result.passed is True
    assert result.severity == 'info'
    assert result.message == (
        'All 4 framework artifact-lifecycle routes present + carry no '
        'disable-model-invocation; local additions require checks by the seat extension')
