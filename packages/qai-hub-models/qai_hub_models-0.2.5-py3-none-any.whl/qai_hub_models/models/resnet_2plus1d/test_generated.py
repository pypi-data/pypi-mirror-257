# THIS FILE WAS AUTO-GENERATED. DO NOT EDIT MANUALLY.

import os
from unittest import mock

import pytest
import qai_hub as hub
import yaml

from qai_hub_models.models.resnet_2plus1d.export import export_model


@pytest.mark.compile
def test_compile_tflite():
    results = export_model(
        skip_downloading=True,
        skip_profiling=True,
        skip_inferencing=True,
        dst_runtime="TFLITE",
    )
    compile_job = results[0]
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["COMPILE_JOBS_FILE"], "a") as f:
            f.write(f"resnet_2plus1d_TFLITE: {compile_job.job_id}\n")
    else:
        result = compile_job.wait()
        assert result.success


@pytest.mark.skip(
    reason="Compilation fails https://dev.aihub.qualcomm.com/jobs/jz5w4x23g"
)
@pytest.mark.compile
def test_compile_qnn():
    results = export_model(
        skip_downloading=True,
        skip_profiling=True,
        skip_inferencing=True,
        dst_runtime="QNN",
    )
    compile_job = results[0]
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["COMPILE_JOBS_FILE"], "a") as f:
            f.write(f"resnet_2plus1d_QNN: {compile_job.job_id}\n")
    else:
        result = compile_job.wait()
        assert result.success


@pytest.mark.profile
def test_profile_tflite():
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["COMPILE_JOBS_FILE"], "r") as f:
            job_ids = yaml.safe_load(f.read())
            hub.submit_compile_job = mock.Mock(
                return_value=hub.get_job(job_ids["resnet_2plus1d_TFLITE"])
            )
    results = export_model(
        skip_downloading=True,
        skip_profiling=False,
        skip_inferencing=True,
        skip_summary=True,
        dst_runtime="TFLITE",
    )
    profile_job = results[1]
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["PROFILE_JOBS_FILE"], "a") as f:
            f.write(f"resnet_2plus1d_TFLITE: {profile_job.job_id}\n")
    else:
        result = profile_job.wait()
        assert result.success


@pytest.mark.skip(
    reason="Compilation fails https://dev.aihub.qualcomm.com/jobs/jz5w4x23g"
)
@pytest.mark.profile
def test_profile_qnn():
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["COMPILE_JOBS_FILE"], "r") as f:
            job_ids = yaml.safe_load(f.read())
            hub.submit_compile_job = mock.Mock(
                return_value=hub.get_job(job_ids["resnet_2plus1d_QNN"])
            )
    results = export_model(
        skip_downloading=True,
        skip_profiling=False,
        skip_inferencing=True,
        skip_summary=True,
        dst_runtime="QNN",
    )
    profile_job = results[1]
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["PROFILE_JOBS_FILE"], "a") as f:
            f.write(f"resnet_2plus1d_QNN: {profile_job.job_id}\n")
    else:
        result = profile_job.wait()
        assert result.success
