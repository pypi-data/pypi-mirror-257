import datetime
import io
import json
import numpy as np
import pytest
from typing import Any, Dict, List, Tuple
import uuid
import zipfile

from titanq import Model, Vtype, errors, Target
from titanq._client import  api_model
from titanq._storage.s3_storage import S3Storage
from titanq._storage.managed_storage import ManagedStorage

from .mock import TitanQClientMock, S3StorageMock

from collections import namedtuple


def file_in_filename_list(filename: str, filename_list: List[str]) -> bool:
    return any(filename in s for s in filename_list)


@pytest.fixture
def model_s3_client() -> Model:
    return Model(
        api_key="test_api_key",
        storage_client=S3Storage(
            access_key="aws_access_key",
            secret_key="aws_secret_access_key",
            bucket_name="bucket_name",
        )
    )

MockGroup = namedtuple("MockGroup", ["model", "expected_result", "expected_metrics", "storage", "client"])
@pytest.fixture
def mock_group() -> MockGroup:
    # expected npy result file content
    expected_result = np.random.rand(10).astype(np.float32)
    expected_result_buffer = io.BytesIO()
    np.save(expected_result_buffer, expected_result)

    # expected metrics file content
    expected_metrics = {"metrics1": 1, "metrics2": "value2"}

    # set mock client with mock values
    buff = io.BytesIO()
    with zipfile.ZipFile(buff, 'w') as file:
        file.writestr("result.npy", expected_result_buffer.getvalue())
        file.writestr("metrics.json", json.dumps(expected_metrics).encode())

    storage_mock = S3StorageMock([buff.getvalue()])
    client_mock = TitanQClientMock(
        api_model.SolveResponse(computation_id=str(uuid.uuid4()), status="Queued", message="test_queued")
    )

    model = Model(
        api_key="test_api_key",
        storage_client=storage_mock,
    )
    model._titanq_client = client_mock

    return MockGroup(
        model,
        expected_result,
        expected_metrics,
        storage_mock,
        client_mock
    )


@pytest.fixture
def constant_datetime(monkeypatch):
    constant_datetime = datetime.datetime(2024,1,1,8,0,0)
    class MockDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return constant_datetime

    monkeypatch.setattr(datetime, 'datetime', MockDatetime)
    return constant_datetime

@pytest.mark.parametrize("api_key, storage_client ,expected_storage_class", [
    ("api_key", S3Storage(access_key="aws_access_key", secret_key="aws_secret_access_key", bucket_name="bucket_name"), S3Storage),
    ("api_key", ManagedStorage(TitanQClientMock()), ManagedStorage),
])
def test_selected_storage(api_key, storage_client, expected_storage_class):
    model = Model(api_key=api_key, storage_client=storage_client)
    assert isinstance(model._storage_client, expected_storage_class)


@pytest.mark.parametrize("name, size, vtype, error", [
    ('x', 1, Vtype.BINARY, None),
    ('x', 47, Vtype.BINARY, None),
    ('x', -1, Vtype.BINARY, ValueError),
    ('x', 0, Vtype.BINARY, ValueError)
])
def test_new_variable(model_s3_client, name, size, vtype, error):
    if error:
        with pytest.raises(error):
            model_s3_client.add_variable_vector(name, size, vtype)
    else:
        model_s3_client.add_variable_vector(name, size, vtype)


def test_multiple_variable(model_s3_client):
    model_s3_client.add_variable_vector('x', 1, Vtype.BINARY)

    with pytest.raises(errors.MaximumVariableLimitError):
        model_s3_client.add_variable_vector('y', 2, Vtype.BINARY)


@pytest.mark.parametrize("weights_shape, bias_shape, objective, error", [
    ((10, 10), (10,), Target.MINIMIZE, None),
    ((11, 10), (10,), Target.MINIMIZE, ValueError),
    ((10, 11), (10,), Target.MINIMIZE, ValueError),
    ((11, 11), (10,), Target.MINIMIZE, ValueError),
    ((10, 10, 10), (10,), Target.MINIMIZE, ValueError),
    ((10,), (10,), Target.MINIMIZE, ValueError),
    ((10,10), (9,), Target.MINIMIZE, ValueError),
    ((10,10), (10,1), Target.MINIMIZE, ValueError),
    ((10,10), (10,2), Target.MINIMIZE, ValueError),
])
def test_set_objective(model_s3_client, weights_shape, bias_shape, objective, error):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    weights = np.random.rand(*weights_shape).astype(np.float32)
    bias = np.random.rand(*bias_shape).astype(np.float32)

    if error:
        with pytest.raises(error):
            model_s3_client.set_objective_matrices(weights, bias, objective)
    else:
        model_s3_client.set_objective_matrices(weights, bias, objective)

@pytest.mark.parametrize("weights_data_type, bias_data_type, error", [
    (np.float32, np.float32, None),
    (np.float64, np.float32, ValueError),
    (np.float32, np.float64, ValueError),
    (np.int32, np.float32, ValueError),
    (np.float32, np.int32, ValueError),
    (np.bool_, np.float32, ValueError),
    (np.float32, np.bool_, ValueError),
    (np.byte, np.float32, ValueError),
    (np.float32, np.byte, ValueError),
    (np.short, np.float32, ValueError),
    (np.float32, np.short, ValueError),
])
def test_objective_matrices_data_type(model_s3_client, weights_data_type, bias_data_type, error):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    weights = np.random.rand(10, 10).astype(weights_data_type)
    bias = np.random.rand(10).astype(bias_data_type)

    if error:
        with pytest.raises(error):
            model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)
    else:
        model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)


def test_set_objective_without_variable(model_s3_client):
    weights = np.random.rand(10, 10)
    bias = np.random.rand(10)

    with pytest.raises(errors.MissingVariableError):
        model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)


def test_set_2_objective(model_s3_client):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    weights = np.random.rand(10, 10).astype(np.float32)
    bias = np.random.rand(10).astype(np.float32)

    model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)

    with pytest.raises(errors.ObjectiveAlreadySetError):
        model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)


def test_optimize_no_variable(model_s3_client):
    with pytest.raises(errors.MissingVariableError):
        model_s3_client.optimize()


def test_optimize_no_objective(model_s3_client):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    with pytest.raises(errors.MissingObjectiveError):
        model_s3_client.optimize()


def test_optimize(mock_group, constant_datetime):
    model = mock_group.model
    expected_result = mock_group.expected_result
    expected_metrics = mock_group.expected_metrics
    mock_storage = mock_group.storage

    # optimize using sdk
    weights = np.random.rand(10, 10).astype(np.float32)
    bias = np.random.rand(10).astype(np.float32)

    model.add_variable_vector('x', 10, Vtype.BINARY)
    model.set_objective_matrices(weights, bias)

    response = model.optimize()

    assert np.array_equal(response.x, expected_result)
    assert response.metrics() == expected_metrics

    # check that needed files has been uploaded
    assert file_in_filename_list("weights.npy", mock_storage.object_uploaded)
    assert file_in_filename_list("bias.npy", mock_storage.object_uploaded)

    # check that cleanup has been made
    assert file_in_filename_list(f"titanq_sdk_output/result_{constant_datetime.isoformat()}.zip", mock_storage.object_deleted)
    assert file_in_filename_list("weights.npy", mock_storage.object_deleted)
    assert file_in_filename_list("bias.npy", mock_storage.object_deleted)

    # check that result files have been downloaded
    assert file_in_filename_list(f"titanq_sdk_output/result_{constant_datetime.isoformat()}.zip", mock_storage.object_downloaded)

@pytest.mark.parametrize("vtype", [
    Vtype.BINARY, Vtype.BIPOLAR,
])
def test_vtype_sent(mock_group, vtype):
    model = mock_group.model
    mock_client = mock_group.client

    # optimize using sdk
    weights = np.random.rand(10, 10).astype(np.float32)
    bias = np.random.rand(10).astype(np.float32)

    model.add_variable_vector('x', 10, vtype)
    model.set_objective_matrices(weights, bias)

    model.optimize()

    assert mock_client.request_sent.parameters.variables_format == str(vtype)