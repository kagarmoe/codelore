from codelore.models import (
    ArtifactRecord,
    ArtifactType,
    ChangeWindow,
    EvidencePack,
    LocatorType,
    Project,
    WindowType,
)


def test_evidence_pack_accepts_minimal_window_and_artifact() -> None:
    project = Project(project_id="project:gastown", name="gastown")
    window = ChangeWindow(
        window_id="window:gastown:v1.1.0..v1.2.0",
        window_type=WindowType.RELEASE,
        label="gastown v1.1.0 -> v1.2.0",
        project_id=project.project_id,
        start_ref="v1.1.0",
        end_ref="v1.2.0",
    )
    artifact = ArtifactRecord(
        artifact_record_id="artifact:commit:abc123",
        artifact_type=ArtifactType.COMMIT,
        locator_type=LocatorType.GIT_COMMIT,
        source_locator="abc123",
        window_ids=(window.window_id,),
    )

    pack = EvidencePack(project=project, window=window, artifacts=(artifact,))

    assert pack.window.window_type == WindowType.RELEASE
    assert pack.artifacts[0].scope_type == "window"
