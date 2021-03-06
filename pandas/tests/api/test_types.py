# -*- coding: utf-8 -*-

import numpy as np

from pandas.core import common as com
from pandas.api import types
from pandas.util import testing as tm

from .test_api import Base


class TestTypes(Base, tm.TestCase):

    allowed = ['is_any_int_dtype', 'is_bool', 'is_bool_dtype',
               'is_categorical', 'is_categorical_dtype', 'is_complex',
               'is_complex_dtype', 'is_datetime64_any_dtype',
               'is_datetime64_dtype', 'is_datetime64_ns_dtype',
               'is_datetime64tz_dtype', 'is_datetimetz', 'is_dtype_equal',
               'is_extension_type', 'is_float', 'is_float_dtype',
               'is_floating_dtype', 'is_int64_dtype', 'is_integer',
               'is_integer_dtype', 'is_number', 'is_numeric_dtype',
               'is_object_dtype', 'is_scalar', 'is_sparse',
               'is_string_dtype', 'is_signed_integer_dtype',
               'is_timedelta64_dtype', 'is_timedelta64_ns_dtype',
               'is_unsigned_integer_dtype', 'is_period',
               'is_period_dtype', 'is_re', 'is_re_compilable',
               'is_dict_like', 'is_iterator', 'is_file_like',
               'is_list_like', 'is_hashable',
               'is_named_tuple', 'is_sequence',
               'pandas_dtype']

    def test_types(self):

        self.check(types, self.allowed)

    def check_deprecation(self, fold, fnew):
        with tm.assert_produces_warning(DeprecationWarning):
            try:
                result = fold('foo')
                expected = fnew('foo')
                self.assertEqual(result, expected)
            except TypeError:
                self.assertRaises(TypeError,
                                  lambda: fnew('foo'))
            except AttributeError:
                self.assertRaises(AttributeError,
                                  lambda: fnew('foo'))

    def test_deprecation_core_common(self):

        # test that we are in fact deprecating
        # the pandas.core.common introspectors
        for t in self.allowed:
            self.check_deprecation(getattr(com, t), getattr(types, t))

    def test_deprecation_core_common_array_equivalent(self):

        with tm.assert_produces_warning(DeprecationWarning):
            com.array_equivalent(np.array([1, 2]), np.array([1, 2]))

    def test_deprecation_core_common_moved(self):

        # these are in pandas.types.common
        l = ['is_datetime_arraylike',
             'is_datetime_or_timedelta_dtype',
             'is_datetimelike',
             'is_datetimelike_v_numeric',
             'is_datetimelike_v_object',
             'is_datetimetz',
             'is_int_or_datetime_dtype',
             'is_period_arraylike',
             'is_string_like',
             'is_string_like_dtype']

        from pandas.types import common as c
        for t in l:
            self.check_deprecation(getattr(com, t), getattr(c, t))

    def test_removed_from_core_common(self):

        for t in ['is_null_datelike_scalar',
                  'ensure_float']:
            self.assertRaises(AttributeError, lambda: getattr(com, t))
