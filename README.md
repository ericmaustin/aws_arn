# simple-arn

[![PyPI version](https://badge.fury.io/py/simple-arn.svg)](https://badge.fury.io/py/simple-arn)

A simple AWS ARN parsing and serialization package.

Supports python 3.7+ or 3.6 with the dataclasses backport.

## Motivation

Other AWS ARN parsing libraries provide parsing functionality but
lack the ability to serialize the parsed ARN back into a string.

Sometimes it is necessary to swap parts of arn strings in the case of 
resource migration automation and this package provides a simple way to do this:

```python
from simple_arn import AwsArn

arn = AwsArn.parse("arn:aws:iam::123456789012:user/MyUserName")\
    .clone(resource="MyOtherUserName")

print(str(arn)) # prints: arn:aws:iam::123456789012:user/MyOtherUserName
```

## Installation
install from PyPI: `pip install simple-arn`

## Usage

This package provides the functionality to parse AWS ARNs into a dataclass `AwsArn`
and `AwsArn` objects can be serialized back into arn strings by simply calling the 
object's `__str__` method.

`AwsArn` objects expose a `clone` method allowing for copies of `AwsArn` objects
with modified attributes.

Example:
```python
from simple_arn import AwsArn

arn = AwsArn.parse("arn:aws:iam::123456789012:user/MyUserName")
print(str(arn)) # prints: arn:aws:iam::123456789012:user/MyUserName

# clone the arn with a different resource
arn2 = arn.clone(resource="MyOtherUserName")
print(str(arn2)) # prints: arn:aws:iam::123456789012:user/MyOtherUserName
```