"""
IMPORTANT: to debug these tests with pytest from the command line
as specfifed from conftest.py, the general exception handling block
of the tested function must be surpressed
"""

import shutil

from edge_containers_cli.autocomplete import (
    all_svc,
    avail_services,
    avail_versions,
    running_svc,
)
from tests.conftest import TMPDIR


def test_all_iocs(mock_run, autocomplete, ctx):
    mock_run.set_seq(autocomplete.all_iocs)

    ctx.parent.parent.params["namespace"] = ""  # use env variable
    result = mock_run.call(all_svc, ctx)
    assert result == ["bl45p-ea-ioc-01"]


def test_all_iocs_local(mock_run, mocker, autocomplete, ctx):
    mocker.patch(
        "edge_containers_cli.globals.EC_K8S_NAMESPACE",
        "local",
    )
    mocker.patch(
        "edge_containers_cli.globals.EC_SERVICES_REPO",
        "https://github.com/epics-containers/bl01t",
    )
    mock_run.set_seq(autocomplete.all_iocs_local)

    ctx.parent.parent.params["namespace"] = ""  # use env variable
    result = mock_run.call(all_svc, ctx)
    assert result == ["bl45p-ea-ioc-01"]


def test_avail_IOCs(mock_run, data, autocomplete, ctx):
    mock_run.set_seq(autocomplete.avail_IOCs)
    shutil.copytree(data / "services", TMPDIR / "services")

    ctx.parent.parent.params["repo"] = ""  # use env variable
    result = mock_run.call(avail_services, ctx)
    assert result == ["bl45p-ea-ioc-01"]


def test_avail_versions(mock_run, data, autocomplete, ctx):
    mock_run.set_seq(autocomplete.avail_versions)
    # shutil.copytree(data / "services", TMPDIR / "services") already exists

    ctx.parent.parent.params["repo"] = ""  # use env variable
    ctx.parent.parent.params["service_name"] = "bl45p-ea-ioc-01"
    result = mock_run.call(avail_versions, ctx)
    assert result == ["2.0"]


def test_running_iocs(mock_run, autocomplete, ctx):
    mock_run.set_seq(autocomplete.running_iocs)

    ctx.parent.parent.params["namespace"] = ""  # use env variable
    result = mock_run.call(running_svc, ctx)
    assert result == ["bl45p-ea-ioc-01"]


def test_running_iocs_local(mock_run, mocker, autocomplete, ctx):
    mocker.patch(
        "edge_containers_cli.globals.EC_K8S_NAMESPACE",
        "local",
    )
    mocker.patch(
        "edge_containers_cli.globals.EC_SERVICES_REPO",
        "https://github.com/epics-containers/bl01t",
    )
    mock_run.set_seq(autocomplete.running_iocs_local)

    ctx.parent.parent.params["namespace"] = ""  # use env variable
    result = mock_run.call(running_svc, ctx)
    assert result == ["bl45p-ea-ioc-01"]
