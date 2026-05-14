import os
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from string import Template
from unittest import mock

import boto3
import pytest
from moto import mock_aws

from lib.app_menu import AppMenu
from lib.database_manager import DatabaseManager
from lib.rds_manager import RDSManager


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
    AppMenu(rds_manager)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""


def test_AppMenu_divider(capsys):
    rds_manager = RDSManager()
    app_menu = AppMenu(rds_manager)
    app_menu.divider()
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert captured_stdout == "---------------------------------------------\n"


def test_AppMenu_option_menu(capsys):
    with mock.patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "Quit"
        rds_manager = RDSManager()
        app_menu = AppMenu(rds_manager)
        app_menu.option_menu()
        captured_stdout, captured_stderr = capsys.readouterr()
        assert captured_stderr == ""
        assert "Default region: us-east-1" in captured_stdout
        assert "Bye" in captured_stdout


####################################################################
#
# RDSManager Tests
#
####################################################################
def test_RDSManager(capsys):
    rds_manager = RDSManager()
    AppMenu(rds_manager)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""


def test_RDSManager_change_region(capsys, aws_credentials):
    rds_manager = RDSManager()
    assert rds_manager.rds.meta.region_name == "us-east-1"

    fake_regions = {
        "SourceRegions": [
            {"RegionName": r} for r in ["us-east-1", "us-east-2", "sa-east-1"]
        ]
    }

    with mock.patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "us-east-2"
        with mock.patch.object(
            rds_manager.rds, "describe_source_regions", return_value=fake_regions
        ):
            rds_manager.change_region()
        assert rds_manager.rds.meta.region_name == "us-east-2"

        mock_select.return_value.ask.return_value = "sa-east-1"
        with mock.patch.object(
            rds_manager.rds, "describe_source_regions", return_value=fake_regions
        ):
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
    rds_manager = RDSManager()
    database = rds_manager.get_database(name="test")
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert len(database["DBInstances"]) == 1
    assert database["DBInstances"][0]["DBInstanceIdentifier"] == "test"
    assert database["DBInstances"][0]["DBName"] == "testing"


def test_RDSManager_get_snapshots(capsys, db1, rds_client):
    rds_client.stop_db_instance(
        DBInstanceIdentifier="test",
        DBSnapshotIdentifier="test-rds-snap",
    )
    rds_manager = RDSManager()
    captured_stdout, captured_stderr = capsys.readouterr()
    snapshots = rds_manager.get_snapshots(database_name="test")
    assert captured_stderr == ""
    # moto also creates an automated snapshot on stop; assert our manual one is present
    assert any(s["id"] == "test-rds-snap" for s in snapshots)
    manual = next(s for s in snapshots if s["id"] == "test-rds-snap")
    assert manual["create_time"] == datetime.now(timezone.utc).strftime("%x %X")


def test_RDSManager_snapshots_by_create_time(
    capsys, db1, rds_client, unsorted_snapshots
):
    rds_manager = RDSManager()
    captured_stdout, captured_stderr = capsys.readouterr()
    snapshots = rds_manager.snapshots_by_create_time(
        unsorted_snapshots=unsorted_snapshots
    )
    assert captured_stderr == ""
    # newest first after sort + reverse
    assert snapshots == [
        {
            "id": "test-rds-snap",
            "create_time": datetime.now(timezone.utc).strftime("%x %X"),
        },
        {
            "id": "test-rds-snap2",
            "create_time": (datetime.now(timezone.utc) - timedelta(days=2)).strftime(
                "%x %X"
            ),
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
    DatabaseManager(rds_manager)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stderr == ""
    assert captured_stdout == ""


def test_DatabaseManager_choose_database(capsys, db1, db2):
    with mock.patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "test"
        rds_manager = RDSManager()
        db_manager = DatabaseManager(rds_manager)
        result = db_manager.choose_database()
        captured_stdout, captured_stderr = capsys.readouterr()
        assert captured_stderr == ""
        assert result is not None
        assert result["DBInstanceIdentifier"] == "test"
        # verify both databases were offered as choices
        choices = mock_select.call_args[1]["choices"]
        assert "test" in choices
        assert "test2" in choices


def test_DatabaseManager_choose_snapshot(capsys, rds_client, db1):
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
    with mock.patch("questionary.select") as mock_select:
        mock_select.return_value.ask.return_value = "test-rds-snap2"
        rds_manager = RDSManager()
        db_manager = DatabaseManager(rds_manager)
        db_manager.choose_snapshot(database_name="test")
        captured_stdout, captured_stderr = capsys.readouterr()
        assert captured_stderr == ""
        # verify both snapshots were offered as choices
        choices = mock_select.call_args[1]["choices"]
        assert any("test-rds-snap" in c for c in choices)
        assert any("test-rds-snap2" in c for c in choices)


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


def test_DatabaseManager_create_database_from_snapshot(capsys, db1, db2):
    with (
        mock.patch("questionary.select") as mock_select,
        mock.patch("questionary.text") as mock_text,
        mock.patch("questionary.confirm") as mock_confirm,
    ):
        # first ask() -> choose database; second (if snapshots exist) -> choose snapshot
        mock_select.return_value.ask.side_effect = ["test", "some-snap  2026-01-01"]
        mock_text.return_value.ask.return_value = "test44"
        mock_confirm.return_value.ask.return_value = False
        rds_manager = RDSManager()
        db_manager = DatabaseManager(rds_manager)
        db_manager.create_database_from_snapshot()
        captured_stdout, captured_stderr = capsys.readouterr()
        assert captured_stderr == ""
