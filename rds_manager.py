import boto3
import pyinputplus as pyip
import traceback


class RDSManager:
    def __init__(self, region_name="us-east-1"):
        self.rds = boto3.client("rds", region_name=region_name)

    def change_region(self) -> None:
        regions = [
            region["RegionName"]
            for region in self.rds.describe_source_regions()["SourceRegions"]
        ]
        selected_region = pyip.inputMenu(regions, lettered=False, numbered=True)
        self.rds = boto3.client("rds", region_name=selected_region)

    def get_databases(self) -> list:
        try:
            return self.rds.describe_db_instances()["DBInstances"]
        except Exception:
            print("[ERROR] - ", traceback.format_exc())
            return []

    def get_database(self, name: str) -> dict:
        try:
            return self.rds.describe_db_instances(DBInstanceIdentifier=name)
        except Exception:
            print("[ERROR] - ", traceback.format_exc())
            return None

    def get_snapshots(self, database_name: str) -> list:
        try:
            resp = self.rds.describe_db_snapshots(DBInstanceIdentifier=database_name)[
                "DBSnapshots"
            ]
            return [snap["DBSnapshotIdentifier"] for snap in resp]
        except Exception:
            print("[ERROR] - ", traceback.format_exc())
            return []

    def restore_database_from_snapshot(
        self, snapshot: str, target: str, source: dict
    ) -> None:
        params = {
            "DBInstanceIdentifier": target,
            "DBParameterGroupName": source["DBParameterGroups"][0][
                "DBParameterGroupName"
            ],
            "DBSnapshotIdentifier": snapshot,
            "DBSubnetGroupName": source["DBSubnetGroup"]["DBSubnetGroupName"],
            "MultiAZ": source["MultiAZ"],
            "VpcSecurityGroupIds": [
                group["VpcSecurityGroupId"]
                for group in source["VpcSecurityGroups"]
                if group["Status"] == "active"
            ],
        }
        if "DomainMemberships" in source and source["DomainMemberships"]:
            params["Domain"] = source["DomainMemberships"][0]["Domain"]
            params["DomainIAMRoleName"] = source["DomainMemberships"][0]["IAMRoleName"]

        try:
            self.rds.restore_db_instance_from_db_snapshot(**params)
            print(f"Create {target}: request sent!\n")
        except Exception as e:
            print(f"[ERROR] - {e}\n")
