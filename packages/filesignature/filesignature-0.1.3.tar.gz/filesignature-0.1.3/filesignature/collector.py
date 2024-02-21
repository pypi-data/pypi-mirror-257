# -*- coding: utf-8 -*-
"""
Class in charge of obtaining file signatures data using
`filesignaturecollectors` package.
"""

from filesignaturecollectors import CollectorController


class CollectorData:
    def get(
        self,
        dest: str
    ) -> None:
        c = CollectorController()
        data1 = c.get_data_wiki()
        data2 = c.get_data_gck()
        c.consolidate_data(data1, data2)
        data_formatted = c.get_dict_data()
        c.to_file(data=data_formatted, path=dest)
