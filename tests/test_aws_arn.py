import pytest

from simple_arn import parse_arn, MalformedArnError


def test__definition():
    arn = parse_arn('arn:partition:service:region:account-id:resource')
    assert arn.partition == 'partition'
    assert arn.service == 'service'
    assert arn.region == 'region'
    assert arn.account_id == 'account-id'
    assert arn.resource_type is None
    assert arn.resource == 'resource'
    assert str(arn) == 'arn:partition:service:region:account-id:resource'

    arn = parse_arn('arn:partition:service:region:account-id:resourcetype/resource')
    assert arn.partition == 'partition'
    assert arn.service == 'service'
    assert arn.region == 'region'
    assert arn.account_id == 'account-id'
    assert arn.resource_type == 'resourcetype'
    assert arn.resource_id == 'resource'
    assert arn.resource == 'resourcetype/resource'
    assert str(arn) == 'arn:partition:service:region:account-id:resourcetype/resource'

    arn = parse_arn('arn:partition:service:region:account-id:resourcetype/resource/qualifier')
    assert arn.partition == 'partition'
    assert arn.service == 'service'
    assert arn.region == 'region'
    assert arn.account_id == 'account-id'
    assert arn.resource_type == 'resourcetype'
    assert arn.resource_id == 'resource/qualifier'
    assert arn.resource == 'resourcetype/resource/qualifier'
    assert str(arn) == 'arn:partition:service:region:account-id:resourcetype/resource/qualifier'

    arn = parse_arn('arn:partition:service:region:account-id:resourcetype/resource:qualifier')
    assert arn.partition == 'partition'
    assert arn.service == 'service'
    assert arn.region == 'region'
    assert arn.account_id == 'account-id'
    assert arn.resource_type == 'resourcetype'
    assert arn.resource_id == 'resource:qualifier'
    assert arn.resource == 'resourcetype/resource:qualifier'
    assert str(arn) == 'arn:partition:service:region:account-id:resourcetype/resource:qualifier'

    arn = parse_arn('arn:partition:service:region:account-id:resourcetype:resource')
    assert arn.partition == 'partition'
    assert arn.service == 'service'
    assert arn.region == 'region'
    assert arn.account_id == 'account-id'
    assert arn.resource_type == 'resourcetype'
    assert arn.resource_id == 'resource'
    assert arn.resource == 'resourcetype:resource'
    assert str(arn) == 'arn:partition:service:region:account-id:resourcetype:resource'

    arn = parse_arn('arn:partition:service:region:account-id:resourcetype:resource:qualifier')
    assert arn.partition == 'partition'
    assert arn.service == 'service'
    assert arn.region == 'region'
    assert arn.account_id == 'account-id'
    assert arn.resource_type == 'resourcetype'
    assert arn.resource_id == 'resource:qualifier'
    assert arn.resource == 'resourcetype:resource:qualifier'
    assert str(arn) == 'arn:partition:service:region:account-id:resourcetype:resource:qualifier'


def test__arn_clone():
    arn_str = 'arn:partition:service:region:account-id:resourcetype/resource:qualifier'
    arn = parse_arn(arn_str)
    arn2 = arn.clone(
        partition='partition2',
        service='service2',
        region='region2',
        account_id='account-id2',
        resource="resourcetype2/account-id2",
    )
    assert arn2.partition == 'partition2'
    assert arn2.service == 'service2'
    assert arn2.region == 'region2'
    assert arn2.account_id == 'account-id2'
    assert arn2.resource_type == 'resourcetype2'


def test__parse_arn__resource_type_with_slash():
    arn_str = 'arn:aws:ec2:us-east-1:123456789012:vpc/vpc-fd580e98'

    arn = parse_arn(arn_str)

    assert arn.partition == 'aws'
    assert arn.service == 'ec2'
    assert arn.region == 'us-east-1'
    assert arn.account_id == '123456789012'
    assert arn.resource_type == 'vpc'
    assert arn.resource_id == 'vpc-fd580e98'
    assert arn.resource == 'vpc/vpc-fd580e98'


def test__parse_arn__resource_type_with_colon():
    arn_str = 'arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo'

    arn = parse_arn(arn_str)

    assert arn.partition == 'aws'
    assert arn.service == 'codecommit'
    assert arn.region == 'us-east-1'
    assert arn.account_id == '123456789012'
    assert arn.resource_type is None
    assert arn.resource_id == 'MyDemoRepo'
    assert arn.resource == 'MyDemoRepo'


def test__parse_arn__resource_type_with_multiple_colons():
    arn_str = 'arn:aws:logs:us-east-1:123456789012:log-group:my-log-group*:log-stream:my-log-stream*'

    arn = parse_arn(arn_str)

    assert arn.partition == 'aws'
    assert arn.service == 'logs'
    assert arn.region == 'us-east-1'
    assert arn.account_id == '123456789012'
    assert arn.resource_type == 'log-group'
    assert arn.resource_id == 'my-log-group*:log-stream:my-log-stream*'
    assert arn.resource == 'log-group:my-log-group*:log-stream:my-log-stream*'


def test__parse_arn__no_resource_type():
    arn_str = 'arn:aws:cloudwatch:us-east-1:123456789012:alarm:MyAlarmName'

    arn = parse_arn(arn_str)

    assert arn.partition == 'aws'
    assert arn.service == 'cloudwatch'
    assert arn.region == 'us-east-1'
    assert arn.account_id == '123456789012'
    assert arn.resource_type == 'alarm'
    assert arn.resource_id == 'MyAlarmName'
    assert arn.resource == 'alarm:MyAlarmName'


def test__parse_arn__resource_with_single_slash():
    arn_str = 'arn:aws:kinesisvideo:us-east-1:123456789012:stream/example-stream-name/0123456789012'

    arn = parse_arn(arn_str)

    assert arn.partition == 'aws'
    assert arn.service == 'kinesisvideo'
    assert arn.region == 'us-east-1'
    assert arn.account_id == '123456789012'
    assert arn.resource_type == 'stream'
    assert arn.resource_id == 'example-stream-name/0123456789012'
    assert arn.resource == 'stream/example-stream-name/0123456789012'


def test__parse_arn__resource_with_multiple_slashes():
    arn_str = 'arn:aws:macie:us-east-1:123456789012:trigger/abc123/alert/abc123'

    arn = parse_arn(arn_str)

    assert arn.partition == 'aws'
    assert arn.service == 'macie'
    assert arn.region == 'us-east-1'
    assert arn.account_id == '123456789012'
    assert arn.resource_type == 'trigger'
    assert arn.resource_id == 'abc123/alert/abc123'
    assert arn.resource == 'trigger/abc123/alert/abc123'


def test__parse_arn__no_region__no_acount_id():
    arn_str = 'arn:aws:s3:::my_corporate_bucket'

    arn = parse_arn(arn_str)

    assert arn.partition == 'aws'
    assert arn.service == 's3'
    assert arn.region is None
    assert arn.account_id is None
    assert arn.resource_type is None
    assert arn.resource == 'my_corporate_bucket'


def test__parse_arn__double_wildcard():
    arn_str = 'arn:aws:events:us-east-1:*:*'

    arn = parse_arn(arn_str)

    assert arn.partition == 'aws'
    assert arn.service == 'events'
    assert arn.region == 'us-east-1'
    assert arn.account_id == '*'
    assert arn.resource_id == '*'
    assert arn.resource_type is None
    assert arn.resource == '*'


def test__malformed_arn__no_arn_prefix():
    arn_str = 'something:aws:s3:::my_corporate_bucket'
    with pytest.raises(MalformedArnError) as exc_info:
        parse_arn(arn_str)

    assert exc_info.value.arn_str == arn_str


def test__malformed_arn__empty_string():
    arn_str = ''
    with pytest.raises(MalformedArnError) as exc_info:
        parse_arn(arn_str)

    assert exc_info.value.arn_str == arn_str
