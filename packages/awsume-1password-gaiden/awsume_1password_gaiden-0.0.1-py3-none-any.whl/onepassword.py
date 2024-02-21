from subprocess import run
from json import loads

from awsume.awsumepy import hookimpl
from awsume.awsumepy.lib.logger import logger

def get_op_item(vault, item):
  out_str = run(
    [
      "op",
      "item",
      "get",
      "--format", "json",
      "--vault", vault,
      item
    ],
    capture_output=True
  ).stdout
  return loads(out_str.decode("utf-8").strip())

def get_op_value(item, key):
  for field in item["fields"]:
    if field["label"] == key:
      return field["value"]

def get_op_otp(vault, item):
  out = run(
    [
      "op",
      "item",
      "get",
      "--vault", vault,
      item,
      "--otp"
    ], capture_output=True).stdout
  return out.decode("utf-8").strip()

@hookimpl
def collect_aws_profiles(config, arguments, credentials_file, config_file):
  op_config = config.get("onepassword")
  if op_config == None:
    logger.error("onepassword config is missing")
    return {}
  vault = op_config.get("vault")
  item = op_config.get("item")

  op_item = get_op_item(vault, item)

  access_key_id = get_op_value(op_item, "access key id")
  secret_access_key = get_op_value(op_item, "secret access key")
  mfa_serial = get_op_value(op_item, "mfa serial")

  logger.debug(f"got data from op, access key id is {access_key_id}")

  profiles = {
    "default": {
      "aws_access_key_id": access_key_id,
      "aws_secret_access_key": secret_access_key,
      "mfa_serial": mfa_serial
    }
  }
  return profiles

@hookimpl
def pre_get_credentials(config, arguments, profiles):
  op_config = config.get("onepassword")

  if op_config == None:
    logger.error("onepassword config is missing")
    return

  vault = op_config.get("vault")
  item = op_config.get("item")

  otp = get_op_otp(vault, item)

  logger.debug(f"otp is {otp}")

  arguments.mfa_token = otp
