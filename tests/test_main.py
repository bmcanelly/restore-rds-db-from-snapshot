import boto3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import json
from io import StringIO
import json
from moto import mock_aws
import os
import pytest
from string import Template
import sys
from unittest import mock

# custom
from lib.database_manager import DatabaseManager
from lib.rds_manager import RDSManager
from lib.app_menu import AppMenu
import main as Main


####################################################################
#
# Fixtures
#
####################################################################
@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_REGION"] = "pytest"
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="function")
def vpc(aws_credentials):
    with mock_aws():
        yield boto3.client("ec2", region_name="us-east-1").create_vpc(
            CidrBlock="10.20.30.0/24",
        )


@pytest.fixture(scope="function")
def vpc_subnet(aws_credentials, vpc):
    with mock_aws():
        yield boto3.client("ec2", region_name="us-east-1").create_subnet(
            VpcId=vpc["Vpc"]["VpcId"], CidrBlock="10.20.30.0/27"
        )

@pytest.fixture(scope="function")
def db1(aws_credentials, vpc_subnet):
    with mock_aws():
        boto3.client("rds", region_name="us-east-1").create_db_subnet_group(
            DBSubnetGroupName="subnet-group-1",
            DBSubnetGroupDescription="pytest",
            SubnetIds=[
                vpc_subnet["Subnet"]["SubnetId"],
            ],
        )
        yield boto3.client("rds", region_name="us-east-1").create_db_instance(
            DBInstanceIdentifier="test",
            AllocatedStorage=10,
            Engine="postgres",
            DBName="testing",
            DBInstanceClass="db.m1.small",
            LicenseModel="license-included",
            MasterUsername="postgres",
            MasterUserPassword="postgres",
            Port=5432,
            DBSecurityGroups=["my_sg"],
            VpcSecurityGroupIds=["sg-123456"],
            EnableCloudwatchLogsExports=["audit", "error"],
            DBSubnetGroupName="subnet-group-1",
            CACertificateIdentifier="some-cert",
        )


@pytest.fixture(scope="function")
def db2(aws_credentials, vpc_subnet):
    with mock_aws():
        yield boto3.client("rds", region_name="us-east-1").create_db_instance(
            DBInstanceIdentifier="test2",
            AllocatedStorage=10,
            Engine="postgres",
            DBName="testing",
            DBInstanceClass="db.m1.small",
            LicenseModel="license-included",
            MasterUsername="postgres",
            MasterUserPassword="postgres",
            Port=5432,
            DBSecurityGroups=["my_sg"],
            VpcSecurityGroupIds=["sg-123456"],
            EnableCloudwatchLogsExports=["audit", "error"],
            DBSubnetGroupName="subnet-group-1",
            CACertificateIdentifier="some-cert",
        )


@pytest.fixture
def rds_client(aws_credentials):
    with mock_aws():
        conn = boto3.client("rds", region_name="us-east-1")
        yield conn


@pytest.fixture(scope="function")
def unsorted_snapshots():
    return [
        {
            "DBSnapshotIdentifier": "test-rds-snap",
            "SnapshotCreateTime": datetime.now(timezone.utc),
        },
        {
            "DBSnapshotIdentifier": "test-rds-snap2",
            "SnapshotCreateTime": (datetime.now(timezone.utc) - timedelta(days=2)),
        },
    ]


@contextmanager
def create_database(rds_client):
    rds_client.create_db_instance(
        DBInstanceIdentifier="test2",
        AllocatedStorage=10,
        Engine="postgres",
        DBName="testing",
        DBInstanceClass="db.m1.small",
        LicenseModel="license-included",
        MasterUsername="postgres",
        MasterUserPassword="postgres",
        Port=5432,
        DBSecurityGroups=["my_sg"],
        VpcSecurityGroupIds=["sg-123456"],
        EnableCloudwatchLogsExports=["audit", "error"],
        CACertificateIdentifier="some-cert",
    )
    yield


####################################################################
#
# AppMenu Tests
#
####################################################################
def test_AppMenu(capsys):
    rds_manager = RDSManager()
    app_menu = AppMenu(rds_manager)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""


def test_AppMenu_divider(capsys):
    rds_manager = RDSManager()
    app_menu = AppMenu(rds_manager)
    app_menu.divider()
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert captured_stdout == "---------------------------------------------\n"


def test_AppMenu_option_menu(capsys, monkeypatch):
    monkeypatch.setattr("sys.stdin", StringIO("4\n"))
    rds_manager = RDSManager()
    app_menu = AppMenu(rds_manager)
    app_menu.option_menu()
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert (
        captured_stdout
        == """Default region: us-east-1
---------------------------------------------
Please select one of the following:
1. Change region
2. List databases
3. Create database from snapshot
4. Quit
Bye\n"""
    )


####################################################################
#
# RDSManager Tests
#
####################################################################
def test_RDSManager(capsys):
    rds_manager = RDSManager()
    app_menu = AppMenu(rds_manager)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""


def test_RDSManager_change_region(capsys, monkeypatch, aws_credentials):
    rds_manager = RDSManager()
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""

    # check default of us-east-1
    assert rds_manager.rds.meta.region_name == "us-east-1"

    # check us-east-2 (currently #28 in dynamic regions list)
    monkeypatch.setattr("sys.stdin", StringIO("28\n"))
    rds_manager.change_region()
    assert rds_manager.rds.meta.region_name == "us-east-2"

    # check sa-east-1 (currently #26 in dynamic regions list)
    monkeypatch.setattr("sys.stdin", StringIO("26\n"))
    rds_manager.change_region()
    assert rds_manager.rds.meta.region_name == "sa-east-1"


@mock_aws
def test_RDSManager_get_databases(capsys, rds_client):
    with create_database(rds_client):
        rds_manager = RDSManager()
        captured_stdout, captured_stderr = capsys.readouterr()
        databases = rds_manager.get_databases()
        assert captured_stderr == ""
        assert len(databases) == 1


@mock_aws
def test_RDSManager_get_database(capsys, db1, rds_client):
    response = rds_client.describe_db_instances(
        DBInstanceIdentifier=db1["DBInstance"]["DBInstanceIdentifier"]
    )
    rds_manager = RDSManager()
    database = rds_manager.get_database(name="test")
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert len(database["DBInstances"]) == 1
    assert len(response["DBInstances"]) == 1
    assert response["DBInstances"][0] == database["DBInstances"][0]


def test_RDSManager_get_snapshots(capsys, db1, rds_client):
    rds_client.stop_db_instance(
        DBInstanceIdentifier="test",
        DBSnapshotIdentifier="test-rds-snap",
    )
    rds_manager = RDSManager()
    captured_stdout, captured_stderr = capsys.readouterr()
    snapshot = rds_manager.get_snapshots(database_name="test")
    assert captured_stderr == ""
    assert snapshot == [
        {
            "id": "test-rds-snap",
            "create_time": datetime.now(timezone.utc).strftime("%x %X"),
        }
    ]


def test_RDSManager_snapshots_by_create_time(
    capsys, db1, rds_client, unsorted_snapshots
):
    rds_manager = RDSManager()
    captured_stdout, captured_stderr = capsys.readouterr()
    snapshots = rds_manager.snapshots_by_create_time(
        unsorted_snapshots=unsorted_snapshots
    )
    assert captured_stderr == ""
    assert snapshots == [
        {
            "id": "test-rds-snap2",
            "create_time": (datetime.now(timezone.utc) - timedelta(days=2)).strftime(
                "%x %X"
            ),
        },
        {
            "id": "test-rds-snap",
            "create_time": datetime.now(timezone.utc).strftime("%x %X"),
        },
    ]


def test_RDSManager_restore_database_from_snapshot(capsys, db1, rds_client):
    rds_client.stop_db_instance(
        DBInstanceIdentifier="test",
        DBSnapshotIdentifier="test-rds-snap",
    )
    rds_manager = RDSManager()

    # ignore the KeyError for CACertificateIdentifier
    # since moto doesn't have support for it (current 5.0.20)
    try:
        rds_manager.restore_database_from_snapshot(
            snapshot="test-rds-snap", target="test-restore-1", source=db1["DBInstance"]
        )
    except KeyError as e:
        assert str(e) == "'CACertificateIdentifier'"
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""


####################################################################
#
# DatabaseManager Tests
#
####################################################################
def test_DatabaseManager(capsys):
    rds_manager = RDSManager()
    db_manager = DatabaseManager(rds_manager)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert captured_stdout == ""


def test_DatabaseManager_choose_database(capsys, monkeypatch, db1, db2):
    monkeypatch.setattr("sys.stdin", StringIO("1\n"))
    rds_manager = RDSManager()
    db_manager = DatabaseManager(rds_manager)
    db_manager.choose_database()
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert "test" in captured_stdout
    assert "test2" in captured_stdout


def test_DatabaseManager_choose_snapshot(capsys, monkeypatch, rds_client, db1):
    rds_client.stop_db_instance(
        DBInstanceIdentifier="test",
        DBSnapshotIdentifier="test-rds-snap",
    )
    rds_client.start_db_instance(
        DBInstanceIdentifier="test",
    )
    rds_client.stop_db_instance(
        DBInstanceIdentifier="test",
        DBSnapshotIdentifier="test-rds-snap2",
    )
    monkeypatch.setattr("sys.stdin", StringIO("1\n"))
    rds_manager = RDSManager()
    db_manager = DatabaseManager(rds_manager)
    db_manager.choose_snapshot(database_name="test")
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert "test-rds-snap" in captured_stdout
    assert "test-rds-snap2" in captured_stdout


def test_DatabaseManager_get_template(capsys):
    rds_manager = RDSManager()
    db_manager = DatabaseManager(rds_manager)
    template_data = db_manager.get_template(path="templates/database.tpl")
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert (
        template_data
        == """
---------------------------------------------
You've chosen:

source  : $source
snapshot: $snapshot
target  : $target
---------------------------------------------
"""
    )

    template = Template(template_data)
    tpl = template.substitute(source="test", snapshot="test-snap", target="newdb")
    assert (
        tpl
        == """
---------------------------------------------
You've chosen:

source  : test
snapshot: test-snap
target  : newdb
---------------------------------------------
"""
    )


def test_DatabaseManager_create_database_from_snapshot(capsys, monkeypatch, db1, db2):
    monkeypatch.setattr("sys.stdin", StringIO("1\n1\ntest44\ny\n"))
    rds_manager = RDSManager()
    db_manager = DatabaseManager(rds_manager)
    db_manager.source_db = "test"
    db_manager.create_database_from_snapshot()
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert "test" in captured_stdout
    assert "test2" in captured_stdout
    # TODO: further checks with monkeypatch - seems to stop at first entry
