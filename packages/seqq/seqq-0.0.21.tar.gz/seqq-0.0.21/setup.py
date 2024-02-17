# -*- coding: utf-8 -*-
# Copyright 2023 jjti
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import io
import os
import re

import setuptools # type: ignore

package_root = os.path.abspath(os.path.dirname(__file__))

name = 'seqq'


description = "Seqq client library"

version = None

with open(os.path.join(package_root, 'seqq/api/gapic_version.py')) as fp:
    version_candidates = re.findall(r"(?<=\")\d+.\d+.\d+(?=\")", fp.read())
    assert (len(version_candidates) == 1)
    version = version_candidates[0]

if version[0] == "0":
    release_status = "Development Status :: 4 - Beta"
else:
    release_status = "Development Status :: 5 - Production/Stable"

dependencies = [
    "google-api-core[grpc] >= 1.34.0, <3.0.0dev,!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,!=2.10.*",
    "google-auth >= 2.14.1, <3.0.0dev",
    "proto-plus >= 1.22.3, <2.0.0dev",
    "protobuf>=3.19.5,<5.0.0dev,!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5",
]
url = "https://github.com/googleapis/google-cloud-python/tree/main/packages/seqq"

package_root = os.path.abspath(os.path.dirname(__file__))


packages = [
    package
    for package in setuptools.find_namespace_packages()
    if package.startswith("seqq")
]

setuptools.setup(
    name=name,
    version=version,
    description=description,
    author="jjti",
    author_email="joshuatimmons1@gmail.com",
    license="Apache 2.0",
    url=url,
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Internet",
    ],
    platforms="Posix; MacOS X; Windows",
    packages=packages,
    python_requires=">=3.7",
    install_requires=dependencies,
    include_package_data=True,
    zip_safe=False,
)
