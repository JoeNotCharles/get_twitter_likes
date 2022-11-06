# Copyright 2022 Joe Mason
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

def get_dict_member(d, key, default):
    return key in d and d[key] or default
