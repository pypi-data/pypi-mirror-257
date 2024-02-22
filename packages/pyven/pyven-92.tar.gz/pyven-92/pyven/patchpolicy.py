# Copyright 2013, 2014, 2015, 2016, 2017, 2020, 2022 Andrzej Cichocki

# This file is part of pyven.
#
# pyven is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyven is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyven.  If not, see <http://www.gnu.org/licenses/>.

from itertools import chain
import glob, json

policyglobs = [
    '/opt/_internal/*/lib/python3.7/site-packages/auditwheel/policy/policy.json',
    '/opt/_internal/pipx/venvs/auditwheel/lib/python3.10/site-packages/auditwheel/policy/manylinux-policy.json',
]
syslibs = 'libasound.so.2', 'libjack.so.0', 'libportaudio.so.2'

def main():
    policypath, = chain(*map(glob.iglob, policyglobs))
    with open(policypath) as f:
        policy = json.load(f)
    for edition in policy:
        if edition['name'].startswith('manylinux'):
            edition['lib_whitelist'].extend(syslibs)
    with open(policypath, 'w') as f:
        json.dump(policy, f)

if ('__main__' == __name__):
    main()
