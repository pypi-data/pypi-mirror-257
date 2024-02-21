import argparse

from compspec.plugin import Plugin


class ExtractorPlugin(Plugin):
    """
    The IOR extractor plugin
    """

    description = "IOR parallel I/O benchmarks"

    def add_arguments(self, subparser):
        """
        Add arguments for the plugin to show up in argparse
        """
        ior = subparser.add_parser(
            self.name,
            formatter_class=argparse.RawTextHelpFormatter,
            description=self.description,
        )
        ior.add_argument(
            "args",
            help="Arguments for IOR (defaults to reasonable set if not defined)",
            nargs="?",
        )

    def run(self, args):
        """
        Run IOR and map metadata into compspec schema.
        """
        # TODO
        print(args)
        print("RUN IOR HERE - choose defaults if")
        import IPython

        IPython.embed()
