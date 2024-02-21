# THIS FILE WAS AUTO-GENERATED. DO NOT EDIT MANUALLY.

import os
from unittest import mock

import pytest
import qai_hub as hub
import yaml

from qai_hub_models.models.trocr.export import export_model


@pytest.mark.compile
def test_compile_tflite():
    results = export_model(
        skip_downloading=True,
        skip_profiling=True,
        skip_inferencing=True,
        dst_runtime="TFLITE",
    )
    for component_name, result in results.items():
        compile_job = result[0]
        if os.environ.get("TEST_HUB_ASYNC", 0):
            with open(os.environ["COMPILE_JOBS_FILE"], "a") as f:
                f.write(f"trocr_TFLITE_{component_name}: {compile_job.job_id}\n")
        else:
            result = compile_job.wait()
            assert result.success


@pytest.mark.skip(
    reason="Compilation fails https://dev.aihub.qualcomm.com/jobs/jz5790vqg"
)
@pytest.mark.compile
def test_compile_qnn():
    results = export_model(
        skip_downloading=True,
        skip_profiling=True,
        skip_inferencing=True,
        dst_runtime="QNN",
    )
    for component_name, result in results.items():
        compile_job = result[0]
        if os.environ.get("TEST_HUB_ASYNC", 0):
            with open(os.environ["COMPILE_JOBS_FILE"], "a") as f:
                f.write(f"trocr_QNN_{component_name}: {compile_job.job_id}\n")
        else:
            result = compile_job.wait()
            assert result.success


@pytest.mark.profile
def test_profile_tflite():
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["COMPILE_JOBS_FILE"], "r") as f:
            job_ids = yaml.safe_load(f.read())
            job_list = []
            for i in job_ids.keys():
                if i.startswith("trocr_TFLITE"):
                    job_list.append(hub.get_job(job_ids[i]))
            hub.submit_compile_job = mock.Mock(side_effect=job_list)
    results = export_model(
        skip_downloading=True,
        skip_profiling=False,
        skip_inferencing=True,
        skip_summary=True,
        dst_runtime="TFLITE",
    )
    for component_name, result in results.items():
        profile_job = result[1]
        if os.environ.get("TEST_HUB_ASYNC", 0):
            with open(os.environ["PROFILE_JOBS_FILE"], "a") as f:
                f.write(f"trocr_TFLITE_{component_name}: {profile_job.job_id}\n")
        else:
            result = profile_job.wait()
            assert result.success


@pytest.mark.skip(
    reason="Compilation fails https://dev.aihub.qualcomm.com/jobs/jz5790vqg"
)
@pytest.mark.profile
def test_profile_qnn():
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["COMPILE_JOBS_FILE"], "r") as f:
            job_ids = yaml.safe_load(f.read())
            job_list = []
            for i in job_ids.keys():
                if i.startswith("trocr_QNN"):
                    job_list.append(hub.get_job(job_ids[i]))
            hub.submit_compile_job = mock.Mock(side_effect=job_list)
    results = export_model(
        skip_downloading=True,
        skip_profiling=False,
        skip_inferencing=True,
        skip_summary=True,
        dst_runtime="QNN",
    )
    for component_name, result in results.items():
        profile_job = result[1]
        if os.environ.get("TEST_HUB_ASYNC", 0):
            with open(os.environ["PROFILE_JOBS_FILE"], "a") as f:
                f.write(f"trocr_QNN_{component_name}: {profile_job.job_id}\n")
        else:
            result = profile_job.wait()
            assert result.success
