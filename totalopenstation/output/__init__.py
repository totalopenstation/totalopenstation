#! /usr/bin/env python

__all__ = ["tops_csv", "tops_dxf", "tops_dat", "tops_sql", "tops_txt", "tops_geojson", "tops_landxml", "tops_kml"]


class OutputOption:
    """Defines an option for an output format.

    This class describes a configurable option that can be used to customize
    the output of a format builder.

    Args:
        name (str): Internal name of the option (used as keyword argument).
        label (str): Human-readable label for the option.
        option_type (str): Type of option - 'bool', 'choice', 'text', 'number'.
        default: Default value for the option.
        choices (list): For 'choice' type, list of valid choices.
        description (str): Detailed description of what the option does.
    """

    def __init__(self, name, label, option_type='bool', default=None,
                 choices=None, description=''):
        self.name = name
        self.label = label
        self.option_type = option_type
        self.default = default
        self.choices = choices or []
        self.description = description

    def validate(self, value):
        """Validate a value for this option.

        Args:
            value: The value to validate.

        Returns:
            The validated (and possibly converted) value.

        Raises:
            ValueError: If the value is invalid.
        """
        if self.option_type == 'bool':
            return bool(value)
        elif self.option_type == 'choice':
            if value not in self.choices:
                raise ValueError(f"Invalid choice '{value}'. Must be one of: {self.choices}")
            return value
        elif self.option_type == 'number':
            return float(value)
        elif self.option_type == 'text':
            return str(value)
        return value


class Builder:
    """Base class for output format builders.

    This class provides the foundation for creating output format builders.
    Subclasses should override the `process` method and optionally define
    `OPTIONS` as a class attribute to declare configurable options.

    Class Attributes:
        OPTIONS (list): List of OutputOption objects defining available options.

    Args:
        data: A list of Feature objects to export.
        **options: Keyword arguments for format-specific options.
    """

    # Subclasses can override this to define their options
    OPTIONS = []

    def __init__(self, data, **options):
        """Init method which **must** be overridden in the child class
        to have a working builder.

        Args:
            data (:class:`formats.Parser`): A list of :class:`formats.Feature`
            **options: Format-specific options as keyword arguments.
        """
        self.data = data
        self._options = {}

        # Apply options with defaults and validation
        for opt in self.OPTIONS:
            if opt.name in options:
                self._options[opt.name] = opt.validate(options[opt.name])
            else:
                self._options[opt.name] = opt.default

    def get_option(self, name):
        """Get the value of an option.

        Args:
            name (str): The option name.

        Returns:
            The option value, or None if not found.
        """
        return self._options.get(name)

    @classmethod
    def get_options(cls):
        """Get the list of available options for this format.

        Returns:
            list: List of OutputOption objects.
        """
        return cls.OPTIONS

    def process(self):
        """Action for building the output string.

        This method **must** be overridden in the child class
        to have a working builder.

        Process the input data (processing data).
        This is because we want to keep the generation of output separated from
        saving it to disk.

        Return:
            str: A string representing the value to output.
        """
        pass


BUILTIN_OUTPUT_FORMATS = {
    'dxf': ('tops_dxf', 'OutputFormat', 'DXF'),
    'csv': ('tops_csv', 'OutputFormat', 'CSV'),
    'sql': ('tops_sql', 'OutputFormat', 'OGC-SQL'),
    'dat': ('tops_dat', 'OutputFormat', 'DAT'),
    'txt': ('tops_txt', 'OutputFormat', 'Text'),
    'geojson': ('tops_geojson', 'OutputFormat', 'GeoJSON'),
    'landxml': ('tops_landxml', 'OutputFormat', 'LandXML'),
    'kml': ('tops_kml', 'OutputFormat', 'KML'),
    'trimblecsv': ('tops_csv', 'TrimbleOutputFormat', 'Trimble CSV')
    }
