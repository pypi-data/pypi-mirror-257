import unittest
import numpy as np
from MyQRPackage.QRDecomposition.qr_decomposition import qr_decomposition


class TestQRDecomposition(unittest.TestCase):
    def test_qr_decomposition(self):
        """Test that QR decomposition returns the correct Q and R matrices."""
        # Create a random matrix A of size 4x4
        A = np.random.rand(4, 4)
        Q, R = qr_decomposition(A)

        # Check that Q*R is close to A
        np.testing.assert_array_almost_equal(np.dot(Q, R), A)

        # Check that Q is orthogonal: Q.T * Q is close to the identity matrix
        np.testing.assert_array_almost_equal(np.dot(Q.T, Q), np.eye(Q.shape[0]))

        # Check that R is upper triangular
        self.assertTrue(np.allclose(R, np.triu(R)), "Matrix R is not upper triangular.")

    def test_qr_square_matrix(self):
        """Test QR decomposition on a square matrix."""
        # Create a square matrix A of size 3x3
        A = np.random.rand(3, 3)
        Q, R = qr_decomposition(A)

        # Verify the decomposition
        np.testing.assert_array_almost_equal(np.dot(Q, R), A)
        np.testing.assert_array_almost_equal(np.dot(Q.T, Q), np.eye(Q.shape[0]))
        self.assertTrue(np.allclose(R, np.triu(R)), "Matrix R is not upper triangular.")

    def test_qr_non_square_matrix(self):
        """Test QR decomposition on a non-square matrix."""
        # Create a non-square matrix A of size 3x2
        A = np.random.rand(3, 2)
        Q, R = qr_decomposition(A)

        # Verify the decomposition
        np.testing.assert_array_almost_equal(np.dot(Q, R), A)
        np.testing.assert_array_almost_equal(np.dot(Q.T, Q), np.eye(Q.shape[0]))
        self.assertTrue(np.allclose(R[:2, :], np.triu(R[:2, :])), "Matrix R is not upper triangular.")

if __name__ == '__main__':
    unittest.main()
