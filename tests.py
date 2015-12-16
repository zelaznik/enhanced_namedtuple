from __future__ import absolute_import

import unittest
from abc import ABCMeta
from enhanced_namedtuple import namedtuple

class test_namedtuple_setup(unittest.TestCase):
    # Because when we subclass 'namedtuple' we return a subclass of tuple
    # We want to make sure that 'namedtuple' itself evaluates as a sublcass of tuple.
    def test_namedtuple_isinstance_ABCMeta(self):
        assert isinstance(namedtuple, ABCMeta)

    def test_namedtuple_is_not_subclass_of_type(self):
        assert not issubclass(namedtuple, type)

    def test_namedtuple__name__is_namedtuple(self):
        self.assertEqual(namedtuple.__name__, 'namedtuple')

    def test_namedtuple_is_subclass_of_tuple(self):
        assert issubclass(namedtuple, tuple)

    def test_namedtuple_is_instance_of_tuple(self):
        assert not isinstance(namedtuple, tuple)

class test_namedtuple_invokation(unittest.TestCase):
    def setUp(self):
        # Check the new implementation and the backward compatible one.
        class Vector(namedtuple):
            _fields = ('x', 'y')
            def __abs__(self):
                return (self.x **2 + self.y **2) ** 0.5
        Point = namedtuple('Point',('x','y'))

        self.Vector = Vector
        self.Point = Point
        self.p = Point(3,4)
        self.v = Vector(3,4)

    def tearDown(self):
        del self.Point, self.Vector
        del self.v, self.p

    def test_no_extraeous_parent_classes_in_mro(self):
        Point, Vector = self.Point, self.Vector
        self.assertEqual(Point.__mro__, (Point, tuple, object))
        self.assertEqual(Vector.__mro__, (Vector, tuple, object))

    def test_subclass_should_still_show_up_as_named_tuples(self):
        Point, Vector = self.Point, self.Vector
        self.assertTrue(issubclass(Point, namedtuple))
        self.assertTrue(issubclass(Vector, namedtuple))

    # 'verbose' and 'rename' should be treated like normal attributes
    # Only raise errors when the field names are inconsistent.
    def test_verbose_treated_like_normal_attr_with_true(self):
        class TryVerboseTrue(namedtuple):
            _fields = ('a','b','c')
            verbose = True
        self.assertEqual(TryVerboseTrue.verbose, True)

    def test_verbose_treated_like_normal_attr_with_false(self):
        class TryVerboseFalse(namedtuple):
            _fields = ('a','b','c')
            verbose = False
        self.assertEqual(TryVerboseFalse.verbose, False)

    def test_rename_treated_like_normal_attr_with_true(self):
        class TryRenameTrue(namedtuple):
            _fields = ('a','b','c')
            rename = True
        self.assertEqual(TryRenameTrue.rename, True)

    def test_rename_treated_like_normal_attr_with_false(self):
        class TryRenameFalse(namedtuple):
            _fields = ('a','b','c')
            rename = False
        self.assertEqual(TryRenameFalse.rename, False)

    def test_error_raised_with_rename_True_and_invalid_field_name(self):
        def block():
            class Vector1(namedtuple):
                _fields = ('name', 'class','age','gender')
                rename = True
        self.assertRaises(ValueError, block)


    def test_field_name_duplicates_raises_error_without_rename_flag(self):
        def block():
            class Vector2(namedtuple):
                _fields = ('name', 'age','gender','age')
                verbose = True
        self.assertRaises(ValueError, block)

    def test_Point_3_4_dot_x_equals_3(self):
        self.assertEqual(self.p.x, 3)

    def test_Point_3_4_dot_y_equals_4(self):
        self.assertEqual(self.p.y, 4)

    def test_abs_Point_3_4_does_not_exist(self):
        def block():
            abs(self.p)
        self.assertRaises(TypeError, block)

    def test_repr_Point_3_4(self):
        self.assertEqual(repr(self.p), 'Point(x=3, y=4)')


    def test_Point_3_4_attribute_a_getter_does_not_exist(self):
        p = self.p
        def block():
            return p.a
        self.assertRaises(AttributeError, block)

    def test_Point_3_4_attribute_a_setter_does_not_exist(self):
        p = self.p
        def block():
            p.a = 5
        self.assertRaises(AttributeError, block)

    def test_Vector_3_4_attribute_x_equals_3(self):
        self.assertEqual(self.v.x, 3)

    def test_Vector_3_4_attribute_y_equals_4(self):
        self.assertEqual(self.v.y, 4)

    def test_abs_Vector_3_4_attribute_equals_5(self):
        self.assertEqual(abs(self.v), 5)

    def test_Vector_3_4_attribute_a_getter_does_not_exist(self):
        v = self.p
        def block():
            return v.a
        self.assertRaises(AttributeError, block)

    def test_Point_3_4_is_a_namedtuple(self):
        self.assertTrue(isinstance(self.p, namedtuple))

    def test_Vector_3_4_is_a_namedtuple(self):
        self.assertTrue(isinstance(self.v, namedtuple))

class test_namedtuple_backward_compatibility(unittest.TestCase):
    def test_rename_flag_handles_name_equals_class(self):
        WithRenameA = namedtuple('WithRenameA', ('x','class','y'), False, True)
        self.assertEqual(WithRenameA._fields, ('x', '_1', 'y'))

    def test_rename_flag_handles_duplicate_names(self):
        WithRenameB = namedtuple('WithRenameB', ('x','y','x'), False, True)
        self.assertEqual(WithRenameB._fields, ('x','y','_2'))

    def test_field_name_of_class_raises_error_without_rename_flag(self):
        def block():
            namedtuple('WithoutRenameA', ('x','class','y'), False, False)
        self.assertRaises(ValueError, block)

    def test_field_name_duplicates_raises_error_without_rename_flag(self):
        def block():
            namedtuple('WithoutRenameB', ('x','y','x'), False, False)
        self.assertRaises(ValueError, block)

class test_attributes_of_namedtuple_instances(unittest.TestCase):
    def test_subclass_overrides_the_correct_attributes(self):
        class Position(namedtuple):
            _fields = ('x','y','z')
            @property
            def z(self):
                return str(self[2])
        s = Position(3,4,5)
        self.assertEqual(s.z, '5')

class test_namedtuple_conventions_strictly_enforced(unittest.TestCase):
    def test_namedutple_subclass_fails_on_multiple_inheritance(self):
        def block():
            class Blah(namedtuple, object):
                _fields = ('x','y')
        self.assertRaises(TypeError, block)

    def test_namedtuple_subclass_prohibited_without_fields_defined(self):
        def block():
            class Blah2(namedtuple):
                pass
        self.assertRaises(TypeError, block)

    def test_empty_fields_still_works(self):
        class Empty(namedtuple):
            _fields = ()
        self.assertEqual(Empty(), ())

    def test_non_empty_slots_is_prohibited(self):
        def block():
            class Blah3(namedtuple):
                __slots__ = ('abs',)
                _fields = ('x','y')
        self.assertRaises(TypeError, block)


if __name__ == '__main__':
    unittest.main()
