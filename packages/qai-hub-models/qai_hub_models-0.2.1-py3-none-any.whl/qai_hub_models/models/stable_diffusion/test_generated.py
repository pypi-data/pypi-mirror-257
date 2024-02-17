# THIS FILE WAS AUTO-GENERATED. DO NOT EDIT MANUALLY.

import os
from unittest import mock

import pytest
import qai_hub as hub
import yaml

from qai_hub_models.models.stable_diffusion.export import export_model
from qai_hub_models.utils.testing import skip_clone_repo_check


@pytest.mark.skip(reason="Consumes too much RAM and crashes CI machine.")
@pytest.mark.compile
@skip_clone_repo_check
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
                f.write(
                    f"stable_diffusion_TFLITE_{component_name}: {compile_job.job_id}\n"
                )
        else:
            result = compile_job.wait()
            assert result.success


@pytest.mark.skip(
    reason="Compilation fails https://dev.qaihub.qualcomm.com/jobs/j7gjqldv5 (VAE decoder) and https://dev.qaihub.qualcomm.com/jobs/jz5w49wmg (UNet)"
)
@pytest.mark.compile
@skip_clone_repo_check
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
                f.write(
                    f"stable_diffusion_QNN_{component_name}: {compile_job.job_id}\n"
                )
        else:
            result = compile_job.wait()
            assert result.success


@pytest.mark.skip(reason="Consumes too much RAM and crashes CI machine.")
@pytest.mark.profile
@skip_clone_repo_check
def test_profile_tflite():
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["COMPILE_JOBS_FILE"], "r") as f:
            job_ids = yaml.safe_load(f.read())
            job_list = []
            for i in job_ids.keys():
                if i.startswith("stable_diffusion_TFLITE"):
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
                f.write(
                    f"stable_diffusion_TFLITE_{component_name}: {profile_job.job_id}\n"
                )
        else:
            result = profile_job.wait()
            assert result.success


@pytest.mark.skip(
    reason="Compilation fails https://dev.qaihub.qualcomm.com/jobs/j7gjqldv5 (VAE decoder) and https://dev.qaihub.qualcomm.com/jobs/jz5w49wmg (UNet)"
)
@pytest.mark.profile
@skip_clone_repo_check
def test_profile_qnn():
    if os.environ.get("TEST_HUB_ASYNC", 0):
        with open(os.environ["COMPILE_JOBS_FILE"], "r") as f:
            job_ids = yaml.safe_load(f.read())
            job_list = []
            for i in job_ids.keys():
                if i.startswith("stable_diffusion_QNN"):
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
                f.write(
                    f"stable_diffusion_QNN_{component_name}: {profile_job.job_id}\n"
                )
        else:
            result = profile_job.wait()
            assert result.success
