class Operations:
    def addition(self, numbers):
        """
        Add numbers in the list.

        :param numbers: List of numbers to add.
        :type numbers: list of float or int

        :return: The sum of the numbers.
        :rtype: float or int
        """
        return sum(numbers)

    def multiplication(self, numbers):
        """
        Multiply numbers in the list.

        :param numbers: List of numbers to multiply.
        :type numbers: list of float or int

        :return: The product of the numbers.
        :rtype: float or int
        """
        product = 1
        for num in numbers:
            product *= num
        return product
