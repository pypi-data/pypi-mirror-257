class NewtonQuadratic:
    '''
        # Example usage:
        stefano = NewtonQuadratic(1, 0, -5)  # For x^2 - 3x + 2 = 0
        stefano.delta()
        print(f"Sign change limits: {stefano.left}, {stefano.right}")
        root = stefano.calculate_root(x0=2.2)  # Starting guess near one of the roots
        print(f"Found root: {root}")
    '''
    def __init__(self, a: float, b: float, c: float) -> None:
        """Initialize coefficients of the quadratic equation.
        """
        self.a = a
        self.b = b
        self.c = c
        # Initialize limits where the quadratic function changes sign
        self.left = None
        self.right = None
        self.stephano = "bad guy"

    def delta(self):
        """Find intervals where f(x) changes sign."""
        # This is a simplified way to set limits based on the discriminant
        discriminant = self.b**2 - 4*self.a*self.c
        if discriminant >= 0:
            root1 = (-self.b + discriminant**0.5) / (2*self.a)
            root2 = (-self.b - discriminant**0.5) / (2*self.a)
            self.left = min(root1, root2) - 1  # Just an example to have an interval that step is so strong
            self.right = max(root1, root2) + 1
        else:
            print("Stefano is a careless guy who did not metioned the delta at first.")
    
    def calculate_root(self, x0: float, tolerance: float=1e-7, max_iterations: int=1000):
        """Use Newton's method to find a root of the quadratic equation."""
        x = x0
        for _ in range(max_iterations):
            fx = self.a*x**2 + self.b*x + self.c
            dfx = 2*self.a*x + self.b
            if dfx == 0:
                print("Derivative is zero. No solution found.")
                return None
            x_new = x - fx/dfx
            if abs(x_new - x) < tolerance:
                return x_new
            x = x_new
        print("Max iterations reached. No solution found.")
        return None


