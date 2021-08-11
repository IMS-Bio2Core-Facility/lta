# -*- coding: utf-8 -*-
"""Custom types for controlling argparse selections."""


class FloatRange:
    """A custom range that supports floating point numbers.

    This does **not** implement all the features of the default `range`.
    Namely, it doesn't support an interval as this does not makes sense
    in the context of floats, as they are an infinitely sub-dividable set.

    Its principle use is to provide a custom container to argparse to restrict
    the values a float might be.
    """

    def __init__(self, start: float, end: float) -> None:
        """Initialise the object.

        Parameters
        ----------
        start : float
            The start of the range, inclusive.
        end : float
            The end of the range, inclusive.
        """
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        """Return the representation of the object.

        Returns
        -------
        str
            The FloatRange representation.
        """
        return f"[{self.start}, {self.end}]"

    def __contains__(self, x: float) -> bool:
        """Test if the FloatRange contains a value.

        Parameters
        ----------
        x : float
            The value to check.

        Returns
        -------
        bool
            True if x in FloatRange, False otherwise.
        """
        return self.start <= x <= self.end

    def __iter__(self) -> "FloatRange":  # type: ignore
        """Iterate over the object.

        This is a bit of cheeky magic to force argparse to recognise the container,
        which is why the typing is ignored.
        It is not designed to actually be iterated over,
        as it will perpetually yield self.

        Yields
        ------
        FloatRange
            Self, yielded indefinitely.
        """
        yield self
