import unittest
import numpy as np
from MyQRPackage.QRDecomposition.household import householder_reflection

class TestHouseholderReflection(unittest.TestCase):
    def test_identity(self):
        """The Householder reflection of an identity vector should negate the first component."""
        v = np.array([1, 0, 0])
        H = householder_reflection(v)
        v_reflected = np.dot(H, v)
        expected_reflected = np.array([-1, 0, 0])  # The reflection should negate the first component
        np.testing.assert_array_almost_equal(v_reflected, expected_reflected)


    def test_orthogonal(self):
        """The Householder matrix should be orthogonal."""
        v = np.random.rand(3)
        H = householder_reflection(v)
        np.testing.assert_array_almost_equal(np.dot(H, H.T), np.eye(3))

    def test_reflection(self):
        """The reflection of v by its Householder matrix should produce a vector parallel to the first standard basis vector e1."""
        v = np.random.rand(3)
        # Normalize v to ensure it's not the zero vector
        v /= np.linalg.norm(v)
        H = householder_reflection(v)
        v_reflected = np.dot(H, v)
        
        # The reflected vector should be a scalar multiple of the first standard basis vector e1
        e1 = np.array([1, 0, 0])
        
        # Check if v_reflected is parallel to e1 by seeing if their cross product is close to the zero vector
        np.testing.assert_array_almost_equal(np.cross(v_reflected, e1), np.zeros(3))
        
        # Also check if the magnitude of v_reflected is close to 1, since Householder reflections preserve vector norms
        np.testing.assert_almost_equal(np.linalg.norm(v_reflected), 1)



if __name__ == '__main__':
    unittest.main()
